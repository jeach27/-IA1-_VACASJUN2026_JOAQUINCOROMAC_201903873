from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
from auth.utils import get_current_user
from proveedores.schemas import ProveedorCreate, ProveedorUpdate, ProveedorResponse

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.get("/", response_model=List[ProveedorResponse])
def listar_proveedores(db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    return db.query(models.Proveedor).filter(models.Proveedor.activo == True).all()


@router.get("/{proveedor_id}", response_model=ProveedorResponse)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor


@router.post("/", response_model=ProveedorResponse, status_code=201)
def crear_proveedor(data: ProveedorCreate, db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    if db.query(models.Proveedor).filter(models.Proveedor.nit == data.nit).first():
        raise HTTPException(status_code=400, detail="Ya existe un proveedor con ese NIT")
    proveedor = models.Proveedor(**data.model_dump())
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor


@router.put("/{proveedor_id}", response_model=ProveedorResponse)
def actualizar_proveedor(
    proveedor_id: int,
    data: ProveedorUpdate,
    db: Session = Depends(get_db),
    _: models.Usuario = Depends(get_current_user),
):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(proveedor, campo, valor)

    db.commit()
    db.refresh(proveedor)
    return proveedor


@router.delete("/{proveedor_id}")
def desactivar_proveedor(proveedor_id: int, db: Session = Depends(get_db), _: models.Usuario = Depends(get_current_user)):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    proveedor.activo = False
    db.commit()
    return {"mensaje": "Proveedor desactivado correctamente"}
