from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ProveedorBase(BaseModel):
    nombre: str
    nit: str
    direccion: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = None
    nit: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class ProveedorResponse(ProveedorBase):
    id: int
    activo: bool
    fecha_creacion: Optional[datetime] = None

    model_config = {"from_attributes": True}
