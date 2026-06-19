from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ReporteResponse(BaseModel):
    id: int
    nombre: str
    formato: str
    ruta_archivo: Optional[str] = None
    fecha_generacion: Optional[datetime] = None

    model_config = {"from_attributes": True}


class GenerarReporteRequest(BaseModel):
    formato: str  # pdf, excel, csv


class EnviarReporteRequest(BaseModel):
    destinatario: str
    asunto: Optional[str] = None
    mensaje: Optional[str] = None
