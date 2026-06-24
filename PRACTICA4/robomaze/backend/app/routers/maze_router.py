"""
Router de laberintos. Expone los endpoints relacionados con la configuracion
y consulta de laberintos disponibles en el sistema.
"""

from fastapi import APIRouter

from app.services.maze_service import get_predefined_mazes

router = APIRouter(prefix="/maze", tags=["maze"])


@router.get("/predefined")
def list_predefined_mazes():
    """Retorna la lista de laberintos predefinidos disponibles para pruebas.

    Cada laberinto incluye id, nombre, descripcion, dimensiones, grid,
    posicion inicial y posicion objetivo.

    Returns:
        Lista de diccionarios con la configuracion de cada laberinto.
    """
    return get_predefined_mazes()
