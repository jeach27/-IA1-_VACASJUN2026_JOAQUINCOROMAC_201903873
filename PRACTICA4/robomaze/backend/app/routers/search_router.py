"""
Router de busqueda. Expone los endpoints para ejecutar BFS, DFS o ambos
sobre la configuracion de laberinto recibida en el cuerpo de la peticion.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.maze_service import build_maze
from app.services.search_service import run_astar, run_bfs, run_dfs, run_both, run_all

router = APIRouter(prefix="/search", tags=["search"])


class MazeRequest(BaseModel):
    """Esquema de la peticion de busqueda.

    Attributes:
        rows: Numero de filas del laberinto.
        cols: Numero de columnas del laberinto.
        grid: Cuadricula de enteros (0=libre, 1=obstaculo).
        start: Lista [fila, columna] con la posicion inicial.
        end: Lista [fila, columna] con la posicion objetivo.
    """

    rows: int
    cols: int
    grid: list
    start: list
    end: list


@router.post("/bfs")
def search_bfs(request: MazeRequest):
    """Ejecuta BFS sobre el laberinto recibido.

    Retorna la ruta optima (mas corta) si existe, junto con la cantidad
    de nodos explorados y el tiempo de ejecucion.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Resultado de BFS serializado. Si no hay ruta, found=false.
    """
    maze = build_maze(request.model_dump())
    result = run_bfs(maze)
    response = result.to_dict()
    if not result.found:
        response["message"] = "No existe ruta entre el inicio y el destino."
    return response


@router.post("/dfs")
def search_dfs(request: MazeRequest):
    """Ejecuta DFS sobre el laberinto recibido.

    Retorna una ruta (no necesariamente la mas corta) si existe, junto con
    la cantidad de nodos explorados y el tiempo de ejecucion.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Resultado de DFS serializado. Si no hay ruta, found=false.
    """
    maze = build_maze(request.model_dump())
    result = run_dfs(maze)
    response = result.to_dict()
    if not result.found:
        response["message"] = "No existe ruta entre el inicio y el destino."
    return response


@router.post("/astar")
def search_astar(request: MazeRequest):
    """Ejecuta A* sobre el laberinto recibido usando distancia Manhattan como heuristica.

    Garantiza la ruta optima al igual que BFS, pero generalmente explora menos
    nodos al guiarse por la heuristica hacia el destino.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Resultado de A* serializado. Si no hay ruta, found=false.
    """
    maze = build_maze(request.model_dump())
    result = run_astar(maze)
    response = result.to_dict()
    if not result.found:
        response["message"] = "No existe ruta entre el inicio y el destino."
    return response


@router.post("/both")
def search_both(request: MazeRequest):
    """Ejecuta BFS y DFS sobre el laberinto recibido y retorna ambos resultados.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Diccionario con claves 'bfs' y 'dfs', cada una con su resultado.
    """
    maze = build_maze(request.model_dump())
    results = run_both(maze)
    for key in results:
        if not results[key]["found"]:
            results[key]["message"] = "No existe ruta entre el inicio y el destino."
    return results


@router.post("/all")
def search_all(request: MazeRequest):
    """Ejecuta BFS, DFS y A* y retorna los tres resultados para comparacion estadistica.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Diccionario con claves 'bfs', 'dfs' y 'astar', cada una con su resultado.
    """
    maze = build_maze(request.model_dump())
    results = run_all(maze)
    for key in results:
        if not results[key]["found"]:
            results[key]["message"] = "No existe ruta entre el inicio y el destino."
    return results
