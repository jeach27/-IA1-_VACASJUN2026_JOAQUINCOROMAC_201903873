import os
import shutil
import time
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
from auth.utils import get_current_user
from facturas.schemas import FacturaResponse, FacturaDetalleResponse, EstadoUpdate, CargaResponse, ItemFacturaResponse
from ocr.procesador import extraer_texto
from ocr.extractor import extraer_campos
from rpa.automatizacion import ejecutar_automatizacion

router = APIRouter(prefix="/facturas", tags=["Facturas"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/uploads")
EXTENSIONES_PERMITIDAS = {".pdf", ".jpg", ".jpeg", ".png"}


def _registrar_bitacora(db: Session, usuario_id: int, documento: str, estado: str, resultado: str, detalles: str = ""):
    entrada = models.Bitacora(
        usuario_id=usuario_id,
        documento_nombre=documento,
        estado=estado,
        resultado=resultado,
        detalles=detalles,
    )
    db.add(entrada)
    db.commit()


@router.post("/cargar", response_model=CargaResponse)
def cargar_factura(
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    extension = os.path.splitext(archivo.filename)[1].lower()
    if extension not in EXTENSIONES_PERMITIDAS:
        raise HTTPException(status_code=400, detail=f"Formato no permitido. Use: {', '.join(EXTENSIONES_PERMITIDAS)}")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ruta_archivo = os.path.join(UPLOAD_DIR, archivo.filename)

    if os.path.exists(ruta_archivo):
        base, ext = os.path.splitext(archivo.filename)
        nombre_unico = f"{base}_{int(time.time())}{ext}"
        ruta_archivo = os.path.join(UPLOAD_DIR, nombre_unico)
    else:
        nombre_unico = archivo.filename

    with open(ruta_archivo, "wb") as f:
        shutil.copyfileobj(archivo.file, f)

    factura = models.Factura(
        archivo_nombre=nombre_unico,
        archivo_ruta=ruta_archivo,
        estado=models.EstadoFactura.PENDIENTE,
        usuario_id=usuario.id,
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)

    try:
        resultado_ocr = extraer_texto(ruta_archivo)
        campos = extraer_campos(resultado_ocr)

        factura.numero_factura = campos.get("numero_factura")
        factura.fecha_factura = campos.get("fecha_factura")
        factura.proveedor_nombre = campos.get("proveedor_nombre")
        factura.proveedor_nit = campos.get("proveedor_nit")
        factura.subtotal = campos.get("subtotal", 0.0)
        factura.impuesto = campos.get("impuesto", 0.0)
        factura.total = campos.get("total", 0.0)
        factura.texto_extraido = campos.get("texto_completo", "")

        if campos.get("proveedor_nit"):
            proveedor_existente = db.query(models.Proveedor).filter(
                models.Proveedor.nit == campos["proveedor_nit"]
            ).first()
            if proveedor_existente:
                factura.proveedor_id = proveedor_existente.id

        validacion = campos.get("validacion", {})
        if validacion.get("valido"):
            factura.estado = models.EstadoFactura.PROCESADO
            estado_bitacora = "Procesado"
            resultado_bitacora = f"Factura {factura.numero_factura} procesada. Total: Q{factura.total:.2f}"
        else:
            factura.estado = models.EstadoFactura.RECHAZADO
            factura.errores_validacion = validacion.get("error", "Error de validacion desconocido")
            estado_bitacora = "Rechazado"
            resultado_bitacora = f"Validacion fallida: {factura.errores_validacion}"

        db.commit()
        db.refresh(factura)

        _registrar_bitacora(
            db, usuario.id, nombre_unico, estado_bitacora, resultado_bitacora,
            detalles=factura.texto_extraido[:500] if factura.texto_extraido else "",
        )

        return CargaResponse(
            factura=FacturaResponse.model_validate(factura),
            campos_extraidos=campos,
            mensaje=resultado_bitacora,
        )

    except Exception as e:
        factura.estado = models.EstadoFactura.ERROR
        factura.errores_validacion = str(e)
        db.commit()
        _registrar_bitacora(db, usuario.id, nombre_unico, "Error", str(e)[:500])
        raise HTTPException(status_code=500, detail=f"Error al procesar la factura: {str(e)}")


@router.get("/", response_model=List[FacturaResponse])
def listar_facturas(db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    return db.query(models.Factura).order_by(models.Factura.fecha_carga.desc()).all()


@router.get("/{factura_id}", response_model=FacturaDetalleResponse)
def obtener_factura(factura_id: int, db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.put("/{factura_id}/estado")
def actualizar_estado(
    factura_id: int,
    data: EstadoUpdate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    estados_validos = ["Procesado", "Pendiente", "Error", "Rechazado"]
    if data.estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado invalido. Use: {', '.join(estados_validos)}")

    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    factura.estado = data.estado
    db.commit()
    _registrar_bitacora(db, usuario.id, factura.archivo_nombre or str(factura_id), data.estado, f"Estado actualizado a {data.estado}")
    return {"mensaje": f"Estado actualizado a {data.estado}"}


@router.get("/{factura_id}/items", response_model=List[ItemFacturaResponse])
def listar_items(factura_id: int, db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura.items


@router.post("/{factura_id}/rpa")
def ejecutar_rpa(
    factura_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    datos = {
        "numero_factura": factura.numero_factura or "",
        "fecha_factura": factura.fecha_factura or "",
        "proveedor": factura.proveedor_nombre or "",
        "nit": factura.proveedor_nit or "",
        "subtotal": str(factura.subtotal),
        "impuesto": str(factura.impuesto),
        "total": str(factura.total),
    }

    resultado = ejecutar_automatizacion(datos)

    factura.rpa_ejecutado = True
    if resultado.get("captura"):
        factura.rpa_captura = resultado["captura"]
    db.commit()

    _registrar_bitacora(
        db, usuario.id, factura.archivo_nombre or str(factura_id),
        "RPA Ejecutado", resultado.get("mensaje", "Automatizacion completada"),
        detalles=str(resultado),
    )

    return resultado
