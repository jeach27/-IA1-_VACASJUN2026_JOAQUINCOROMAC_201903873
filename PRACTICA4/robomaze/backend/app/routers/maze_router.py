"""
Router de laberintos. Expone los endpoints relacionados con la consulta
de laberintos predefinidos y la generacion aleatoria de nuevos laberintos.
Incluye manejo de errores HTTP para fallos inesperados.
"""

from fastapi import APIRouter, HTTPException, Query

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

    Raises:
        HTTPException 500: Si ocurre un error inesperado al obtener los laberintos.
    """
    try:
        return get_predefined_mazes()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al obtener los laberintos predefinidos: {str(e)}",
        )


@router.get("/generate")
def generate_random_maze(
    rows: int = Query(default=10, ge=5, le=25, description="Filas del laberinto (5-25)"),
    cols: int = Query(default=10, ge=5, le=25, description="Columnas del laberinto (5-25)"),
    seed: int = Query(default=None, description="Semilla para reproducibilidad"),
):
    """Genera un laberinto aleatorio usando DFS aleatorizado (recursive backtracker).

    Produce un laberinto perfecto: existe exactamente un camino entre cualquier
    par de celdas. FastAPI valida automaticamente que rows y cols esten entre
    5 y 25; valores fuera de rango producen un error 422.

    Args:
        rows: Numero de filas (5-25).
        cols: Numero de columnas (5-25).
        seed: Semilla opcional para reproducir el mismo laberinto.

    Returns:
        Diccionario con rows, cols, grid, start y end del laberinto generado.

    Raises:
        HTTPException 422: Si rows o cols estan fuera del rango permitido (validacion automatica).
        HTTPException 500: Si ocurre un error inesperado durante la generacion.
    """
    try:
        return generate_maze(rows, cols, seed)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al generar el laberinto: {str(e)}",
        )
