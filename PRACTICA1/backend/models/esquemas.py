"""
Esquemas Pydantic para validacion de datos de entrada y salida.
"""

from pydantic import BaseModel, Field
from typing import List


class ConsultaRuta(BaseModel):
    origen: str = Field(..., description="Ciudad de origen")
    destino: str = Field(..., description="Ciudad de destino")


class RutaResultado(BaseModel):
    ciudades: List[str]
    distancia: int


class RespuestaRutaMasCorta(BaseModel):
    origen: str
    destino: str
    ruta: List[str]
    distancia: int


class RespuestaTodasRutas(BaseModel):
    origen: str
    destino: str
    rutas: List[RutaResultado]
    total_rutas: int


class NuevaConexion(BaseModel):
    ciudad1: str = Field(..., description="Primera ciudad")
    ciudad2: str = Field(..., description="Segunda ciudad")
    distancia: int = Field(..., gt=0, description="Distancia en km (debe ser mayor a 0)")


class RespuestaCiudades(BaseModel):
    ciudades: List[str]
    total: int


class ConexionInfo(BaseModel):
    origen: str
    destino: str
    distancia: int


class RespuestaConexiones(BaseModel):
    conexiones: List[ConexionInfo]
    total: int


class RespuestaExito(BaseModel):
    mensaje: str


class RespuestaError(BaseModel):
    detalle: str
