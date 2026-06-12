from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import obtener_sesion
from app.models import Configuracion, UsuarioAdmin
from app.schemas import ConfiguracionActualizar, ConfiguracionRespuesta
from app.auth import obtener_usuario_actual

router = APIRouter(prefix="/configuracion", tags=["configuracion"])


@router.get("", response_model=list[ConfiguracionRespuesta])
def listar_configuracion(
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    return sesion.query(Configuracion).order_by(Configuracion.clave).all()


@router.get("/{clave}", response_model=ConfiguracionRespuesta)
def obtener_configuracion(clave: str, sesion: Session = Depends(obtener_sesion)):
    config = sesion.query(Configuracion).filter(Configuracion.clave == clave).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    return config


@router.put("/{clave}", response_model=ConfiguracionRespuesta)
def actualizar_configuracion(
    clave: str,
    datos: ConfiguracionActualizar,
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    config = sesion.query(Configuracion).filter(Configuracion.clave == clave).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    config.valor = datos.valor
    sesion.commit()
    sesion.refresh(config)
    return config
