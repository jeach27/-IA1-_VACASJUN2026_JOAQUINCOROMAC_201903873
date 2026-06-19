import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
from auth.utils import get_current_user
from reportes.schemas import ReporteResponse, GenerarReporteRequest, EnviarReporteRequest
from reportes.generador import generar_csv, generar_excel, generar_pdf

router = APIRouter(prefix="/reportes", tags=["Reportes"])

FORMATOS_VALIDOS = {"pdf", "excel", "csv"}


@router.post("/generar", response_model=ReporteResponse, status_code=201)
def generar_reporte(
    data: GenerarReporteRequest,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    if data.formato not in FORMATOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Formato invalido. Use: {', '.join(FORMATOS_VALIDOS)}")

    facturas = db.query(models.Factura).order_by(models.Factura.fecha_carga.desc()).all()
    if not facturas:
        raise HTTPException(status_code=404, detail="No hay facturas para incluir en el reporte")

    try:
        if data.formato == "csv":
            ruta = generar_csv(facturas)
        elif data.formato == "excel":
            ruta = generar_excel(facturas)
        else:
            ruta = generar_pdf(facturas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar reporte: {str(e)}")

    nombre_archivo = os.path.basename(ruta)
    reporte = models.Reporte(
        nombre=f"Reporte de facturas - {data.formato.upper()}",
        formato=data.formato,
        ruta_archivo=ruta,
        usuario_id=usuario.id,
    )
    db.add(reporte)
    db.commit()
    db.refresh(reporte)

    entrada_bitacora = models.Bitacora(
        usuario_id=usuario.id,
        documento_nombre=nombre_archivo,
        estado="Generado",
        resultado=f"Reporte {data.formato.upper()} generado con {len(facturas)} facturas",
    )
    db.add(entrada_bitacora)
    db.commit()

    return reporte


@router.get("/", response_model=List[ReporteResponse])
def listar_reportes(db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    return db.query(models.Reporte).order_by(models.Reporte.fecha_generacion.desc()).all()


@router.get("/{reporte_id}/descargar")
def descargar_reporte(reporte_id: int, db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    reporte = db.query(models.Reporte).filter(models.Reporte.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    if not reporte.ruta_archivo or not os.path.exists(reporte.ruta_archivo):
        raise HTTPException(status_code=404, detail="Archivo del reporte no encontrado en disco")

    tipos_media = {"pdf": "application/pdf", "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "csv": "text/csv"}
    media_type = tipos_media.get(reporte.formato, "application/octet-stream")

    return FileResponse(
        path=reporte.ruta_archivo,
        media_type=media_type,
        filename=os.path.basename(reporte.ruta_archivo),
    )


@router.post("/{reporte_id}/enviar")
def enviar_reporte(
    reporte_id: int,
    data: EnviarReporteRequest,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    reporte = db.query(models.Reporte).filter(models.Reporte.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    if not reporte.ruta_archivo or not os.path.exists(reporte.ruta_archivo):
        raise HTTPException(status_code=404, detail="Archivo del reporte no disponible")

    from correo.servicio import enviar_correo

    asunto = data.asunto or f"Reporte SmartInvoice - {reporte.nombre}"
    cuerpo = data.mensaje or f"Se adjunta el reporte generado el {reporte.fecha_generacion.strftime('%d/%m/%Y %H:%M') if reporte.fecha_generacion else ''}."

    resultado = enviar_correo(
        destinatario=data.destinatario,
        asunto=asunto,
        cuerpo=cuerpo,
        adjunto=reporte.ruta_archivo,
    )

    entrada_bitacora = models.Bitacora(
        usuario_id=usuario.id,
        documento_nombre=os.path.basename(reporte.ruta_archivo),
        estado="Enviado" if resultado["exito"] else "Error envio",
        resultado=resultado["mensaje"],
    )
    db.add(entrada_bitacora)
    db.commit()

    if not resultado["exito"]:
        raise HTTPException(status_code=500, detail=resultado["mensaje"])

    return {"mensaje": resultado["mensaje"]}
