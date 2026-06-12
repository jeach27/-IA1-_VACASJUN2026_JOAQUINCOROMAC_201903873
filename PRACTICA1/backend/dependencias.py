"""
Gestion de dependencias para inyeccion en FastAPI.
El repositorio y el servicio se crean una sola vez al iniciar la aplicacion.
"""

from repositories.prolog_repositorio import PrologRepositorio
from services.ruta_servicio import RutaServicio

_repositorio = PrologRepositorio()
_servicio = RutaServicio(_repositorio)


def obtener_servicio() -> RutaServicio:
    return _servicio
