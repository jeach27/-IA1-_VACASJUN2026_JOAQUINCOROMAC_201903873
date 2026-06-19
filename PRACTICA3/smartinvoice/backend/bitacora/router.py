from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from database import get_db
import models
from auth.utils import get_current_user
from bitacora.schemas import BitacoraResponse

router = APIRouter(prefix="/bitacora", tags=["Bitacora"])


@router.get("/", response_model=List[BitacoraResponse])
def listar_bitacora(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    estado: Optional[str] = None,
    usuario_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(get_current_user),
):
    query = db.query(models.Bitacora).order_by(models.Bitacora.fecha_hora.desc())

    if fecha_inicio:
        query = query.filter(models.Bitacora.fecha_hora >= fecha_inicio)
    if fecha_fin:
        from datetime import datetime, timedelta
        fin_con_hora = datetime.combine(fecha_fin, datetime.max.time())
        query = query.filter(models.Bitacora.fecha_hora <= fin_con_hora)
    if estado:
        query = query.filter(models.Bitacora.estado.ilike(f"%{estado}%"))
    if usuario_id:
        query = query.filter(models.Bitacora.usuario_id == usuario_id)

    return query.all()


@router.get("/{registro_id}", response_model=BitacoraResponse)
def obtener_registro(registro_id: int, db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    registro = db.query(models.Bitacora).filter(models.Bitacora.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro
