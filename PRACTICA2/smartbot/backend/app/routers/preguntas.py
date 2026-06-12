from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import obtener_sesion
from app.models import Pregunta, UsuarioAdmin
from app.schemas import PreguntaCrear, PreguntaActualizar, PreguntaRespuesta
from app.auth import obtener_usuario_actual

router = APIRouter(prefix="/preguntas", tags=["preguntas"])


@router.get("", response_model=list[PreguntaRespuesta])
def listar_preguntas(
    categoria_id: int | None = None,
    solo_activas: bool = False,
    sesion: Session = Depends(obtener_sesion),
):
    consulta = sesion.query(Pregunta)
    if categoria_id is not None:
        consulta = consulta.filter(Pregunta.categoria_id == categoria_id)
    if solo_activas:
        consulta = consulta.filter(Pregunta.activa == True)
    return consulta.order_by(Pregunta.id).all()


@router.post("", response_model=PreguntaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_pregunta(
    datos: PreguntaCrear,
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    pregunta = Pregunta(**datos.model_dump())
    sesion.add(pregunta)
    sesion.commit()
    sesion.refresh(pregunta)
    return pregunta


@router.put("/{pregunta_id}", response_model=PreguntaRespuesta)
def actualizar_pregunta(
    pregunta_id: int,
    datos: PreguntaActualizar,
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    pregunta = sesion.query(Pregunta).filter(Pregunta.id == pregunta_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(pregunta, campo, valor)
    sesion.commit()
    sesion.refresh(pregunta)
    return pregunta


@router.delete("/{pregunta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pregunta(
    pregunta_id: int,
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    pregunta = sesion.query(Pregunta).filter(Pregunta.id == pregunta_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    sesion.delete(pregunta)
    sesion.commit()
