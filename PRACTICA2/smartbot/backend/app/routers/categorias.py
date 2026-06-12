from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import obtener_sesion
from app.models import Categoria, UsuarioAdmin
from app.schemas import CategoriaCrear, CategoriaActualizar, CategoriaRespuesta
from app.auth import obtener_usuario_actual

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("", response_model=list[CategoriaRespuesta])
def listar_categorias(sesion: Session = Depends(obtener_sesion)):
    return sesion.query(Categoria).order_by(Categoria.nombre).all()


@router.post("", response_model=CategoriaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    datos: CategoriaCrear,
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    existente = sesion.query(Categoria).filter(Categoria.nombre == datos.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una categoria con ese nombre")
    categoria = Categoria(**datos.model_dump())
    sesion.add(categoria)
    sesion.commit()
    sesion.refresh(categoria)
    return categoria


@router.put("/{categoria_id}", response_model=CategoriaRespuesta)
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaActualizar,
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    categoria = sesion.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(categoria, campo, valor)
    sesion.commit()
    sesion.refresh(categoria)
    return categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(
    categoria_id: int,
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    categoria = sesion.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    sesion.delete(categoria)
    sesion.commit()
