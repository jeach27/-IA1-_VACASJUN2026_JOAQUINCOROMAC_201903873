from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ItemFacturaResponse(BaseModel):
    id: int
    descripcion: Optional[str] = None
    cantidad: float
    precio_unitario: float
    total: float

    model_config = {"from_attributes": True}


class FacturaResponse(BaseModel):
    id: int
    numero_factura: Optional[str] = None
    fecha_factura: Optional[str] = None
    proveedor_nombre: Optional[str] = None
    proveedor_nit: Optional[str] = None
    subtotal: float
    impuesto: float
    total: float
    archivo_nombre: Optional[str] = None
    estado: str
    fecha_carga: Optional[datetime] = None
    rpa_ejecutado: bool
    errores_validacion: Optional[str] = None

    model_config = {"from_attributes": True}


class FacturaDetalleResponse(FacturaResponse):
    texto_extraido: Optional[str] = None
    rpa_captura: Optional[str] = None
    items: List[ItemFacturaResponse] = []


class EstadoUpdate(BaseModel):
    estado: str


class CargaResponse(BaseModel):
    factura: FacturaResponse
    campos_extraidos: dict
    mensaje: str
