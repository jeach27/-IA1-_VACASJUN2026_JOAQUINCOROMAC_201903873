"""
Router de busqueda. Expone los endpoints para ejecutar BFS, DFS, A* o
combinaciones sobre la configuracion de laberinto recibida en el cuerpo
de la peticion. Incluye validacion de entrada y manejo de errores HTTP.
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


def _validate_maze_request(request: MazeRequest) -> None:
    """Valida la configuracion del laberinto y lanza HTTPException 400 si hay errores.

    Verifica dimensiones, valores de celdas, posiciones de inicio/destino y
    que ninguno de los dos puntos sea un obstaculo o coincidan entre si.

    Args:
        request: Datos del laberinto recibidos en la peticion.

    Raises:
        HTTPException 400: Si alguna validacion falla, con un mensaje descriptivo.
    """
    if request.rows < 1 or request.cols < 1:
        raise HTTPException(
            status_code=400,
            detail="rows y cols deben ser enteros positivos mayores que 0.",
        )

    if len(request.grid) != request.rows:
        raise HTTPException(
            status_code=400,
            detail=(
                f"El grid tiene {len(request.grid)} filas "
                f"pero rows indica {request.rows}."
            ),
        )

    for i, row in enumerate(request.grid):
        if not isinstance(row, list):
            raise HTTPException(
                status_code=400,
                detail=f"La fila {i} del grid no es una lista.",
            )
        if len(row) != request.cols:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"La fila {i} tiene {len(row)} columnas "
                    f"pero cols indica {request.cols}."
                ),
            )
        for j, cell in enumerate(row):
            if cell not in (0, 1):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Valor invalido en celda ({i},{j}): "
                        f"se esperaba 0 o 1, se recibio {cell}."
                    ),
                )

    if len(request.start) != 2:
        raise HTTPException(
            status_code=400,
            detail="start debe ser una lista de exactamente dos enteros [fila, columna].",
        )
    if len(request.end) != 2:
        raise HTTPException(
            status_code=400,
            detail="end debe ser una lista de exactamente dos enteros [fila, columna].",
        )

    sr, sc = request.start
    er, ec = request.end

    if not (0 <= sr < request.rows and 0 <= sc < request.cols):
        raise HTTPException(
            status_code=400,
            detail=(
                f"La posicion inicial ({sr},{sc}) esta fuera de los limites "
                f"del laberinto ({request.rows}x{request.cols})."
            ),
        )
    if not (0 <= er < request.rows and 0 <= ec < request.cols):
        raise HTTPException(
            status_code=400,
            detail=(
                f"La posicion destino ({er},{ec}) esta fuera de los limites "
                f"del laberinto ({request.rows}x{request.cols})."
            ),
        )

    if request.grid[sr][sc] == 1:
        raise HTTPException(
            status_code=400,
            detail=f"La posicion inicial ({sr},{sc}) esta marcada como obstaculo.",
        )
    if request.grid[er][ec] == 1:
        raise HTTPException(
            status_code=400,
            detail=f"La posicion destino ({er},{ec}) esta marcada como obstaculo.",
        )

    if sr == er and sc == ec:
        raise HTTPException(
            status_code=400,
            detail="La posicion inicial y la posicion destino no pueden ser la misma celda.",
        )


@router.post("/bfs")
def search_bfs(request: MazeRequest):
    """Ejecuta BFS sobre el laberinto recibido.

    Retorna la ruta optima (mas corta) si existe, junto con la cantidad
    de nodos explorados, el orden de exploracion y el tiempo de ejecucion.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Resultado de BFS serializado. Si no hay ruta, found=false.

    Raises:
        HTTPException 400: Si la configuracion del laberinto es invalida.
        HTTPException 500: Si ocurre un error inesperado durante la ejecucion.
    """
    _validate_maze_request(request)
    try:
        maze = build_maze(request.model_dump())
        result = run_bfs(maze)
        response = result.to_dict()
        if not result.found:
            response["message"] = "No existe ruta entre el inicio y el destino."
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al ejecutar BFS: {str(e)}",
        )


@router.post("/dfs")
def search_dfs(request: MazeRequest):
    """Ejecuta DFS sobre el laberinto recibido.

    Retorna una ruta (no necesariamente la mas corta) si existe, junto con
    la cantidad de nodos explorados y el tiempo de ejecucion.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Resultado de DFS serializado. Si no hay ruta, found=false.

    Raises:
        HTTPException 400: Si la configuracion del laberinto es invalida.
        HTTPException 500: Si ocurre un error inesperado durante la ejecucion.
    """
    _validate_maze_request(request)
    try:
        maze = build_maze(request.model_dump())
        result = run_dfs(maze)
        response = result.to_dict()
        if not result.found:
            response["message"] = "No existe ruta entre el inicio y el destino."
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al ejecutar DFS: {str(e)}",
        )


@router.post("/astar")
def search_astar(request: MazeRequest):
    """Ejecuta A* sobre el laberinto recibido usando distancia Manhattan como heuristica.

    Garantiza la ruta optima al igual que BFS, pero generalmente explora menos
    nodos al guiarse por la heuristica hacia el destino.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Resultado de A* serializado. Si no hay ruta, found=false.

    Raises:
        HTTPException 400: Si la configuracion del laberinto es invalida.
        HTTPException 500: Si ocurre un error inesperado durante la ejecucion.
    """
    _validate_maze_request(request)
    try:
        maze = build_maze(request.model_dump())
        result = run_astar(maze)
        response = result.to_dict()
        if not result.found:
            response["message"] = "No existe ruta entre el inicio y el destino."
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al ejecutar A*: {str(e)}",
        )


@router.post("/both")
def search_both(request: MazeRequest):
    """Ejecuta BFS y DFS sobre el laberinto recibido y retorna ambos resultados.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Diccionario con claves 'bfs' y 'dfs', cada una con su resultado.

    Raises:
        HTTPException 400: Si la configuracion del laberinto es invalida.
        HTTPException 500: Si ocurre un error inesperado durante la ejecucion.
    """
    _validate_maze_request(request)
    try:
        maze = build_maze(request.model_dump())
        results = run_both(maze)
        for key in results:
            if not results[key]["found"]:
                results[key]["message"] = "No existe ruta entre el inicio y el destino."
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al ejecutar BFS y DFS: {str(e)}",
        )


@router.post("/all")
def search_all(request: MazeRequest):
    """Ejecuta BFS, DFS y A* y retorna los tres resultados para comparacion estadistica.

    Args:
        request: Configuracion del laberinto.

    Returns:
        Diccionario con claves 'bfs', 'dfs' y 'astar', cada una con su resultado.

    Raises:
        HTTPException 400: Si la configuracion del laberinto es invalida.
        HTTPException 500: Si ocurre un error inesperado durante la ejecucion.
    """
    _validate_maze_request(request)
    try:
        maze = build_maze(request.model_dump())
        results = run_all(maze)
        for key in results:
            if not results[key]["found"]:
                results[key]["message"] = "No existe ruta entre el inicio y el destino."
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al comparar algoritmos: {str(e)}",
        )
