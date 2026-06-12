"""
Router de rutas: define los endpoints HTTP de la API.
Solo delega al servicio; no contiene logica de negocio.
"""

from fastapi import APIRouter, Depends
from models.esquemas import (
    ConsultaRuta,
    NuevaConexion,
    RespuestaRutaMasCorta,
    RespuestaTodasRutas,
    RespuestaCiudades,
    RespuestaConexiones,
    RespuestaExito,
)
from services.ruta_servicio import RutaServicio
from dependencias import obtener_servicio

router = APIRouter(prefix="/api", tags=["rutas"])


@router.get("/ciudades", response_model=RespuestaCiudades)
def listar_ciudades(servicio: RutaServicio = Depends(obtener_servicio)):
    """Devuelve la lista de todas las ciudades registradas."""
    return servicio.obtener_ciudades()


@router.get("/conexiones", response_model=RespuestaConexiones)
def listar_conexiones(servicio: RutaServicio = Depends(obtener_servicio)):
    """Devuelve todas las conexiones directas entre ciudades."""
    return servicio.obtener_conexiones()


@router.post("/ruta-mas-corta", response_model=RespuestaRutaMasCorta)
def ruta_mas_corta(
    consulta: ConsultaRuta, servicio: RutaServicio = Depends(obtener_servicio)
):
    """Calcula la ruta mas corta entre dos ciudades."""
    return servicio.ruta_mas_corta(consulta.origen, consulta.destino)


@router.post("/todas-las-rutas", response_model=RespuestaTodasRutas)
def todas_las_rutas(
    consulta: ConsultaRuta, servicio: RutaServicio = Depends(obtener_servicio)
):
    """Devuelve todas las rutas posibles entre dos ciudades, ordenadas por distancia."""
    return servicio.todas_las_rutas(consulta.origen, consulta.destino)


@router.post("/conexion", response_model=RespuestaExito)
def agregar_conexion(
    datos: NuevaConexion, servicio: RutaServicio = Depends(obtener_servicio)
):
    """Agrega una nueva conexion entre dos ciudades."""
    return servicio.agregar_conexion(datos.ciudad1, datos.ciudad2, datos.distancia)
