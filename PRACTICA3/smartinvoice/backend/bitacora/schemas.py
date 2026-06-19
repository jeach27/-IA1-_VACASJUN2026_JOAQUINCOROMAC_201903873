from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BitacoraResponse(BaseModel):
    id: int
    fecha_hora: Optional[datetime] = None
    usuario_id: Optional[int] = None
    documento_nombre: Optional[str] = None
    estado: Optional[str] = None
    resultado: Optional[str] = None
    detalles: Optional[str] = None

    model_config = {"from_attributes": True}
