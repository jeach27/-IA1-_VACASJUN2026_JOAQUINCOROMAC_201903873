"""
Router de laberintos. Expone los endpoints relacionados con la configuracion
y consulta de laberintos disponibles en el sistema.
"""

from fastapi import APIRouter, Query

from app.services.generator_service import generate_maze
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


@router.get("/generate")
def generate_random_maze(
    rows: int = Query(default=10, ge=5, le=25, description="Filas del laberinto"),
    cols: int = Query(default=10, ge=5, le=25, description="Columnas del laberinto"),
    seed: int = Query(default=None, description="Semilla para reproducibilidad"),
):
    """Genera un laberinto aleatorio usando DFS aleatorizado (recursive backtracker).

    Produce un laberinto perfecto: existe exactamente un camino entre cualquier
    par de celdas. El tamano puede configurarse entre 5x5 y 25x25.

    Args:
        rows: Numero de filas (5-25).
        cols: Numero de columnas (5-25).
        seed: Semilla opcional para reproducir el mismo laberinto.

    Returns:
        Diccionario con rows, cols, grid, start y end del laberinto generado.
    """
    return generate_maze(rows, cols, seed)
