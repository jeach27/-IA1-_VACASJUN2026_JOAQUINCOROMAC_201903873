"""
Servicio de busqueda. Orquesta la ejecucion de los algoritmos BFS y DFS
sobre una instancia de Maze y retorna los resultados serializables.
"""

from app.algorithms.bfs import bfs
from app.algorithms.dfs import dfs
from app.models.maze import Maze
from app.models.search_result import SearchResult


def run_bfs(maze: Maze) -> SearchResult:
    """Ejecuta el algoritmo BFS sobre el laberinto dado.

    Args:
        maze: Instancia de Maze con la configuracion del laberinto.

    Returns:
        SearchResult con los resultados de la busqueda BFS.
    """
    return bfs(maze)


def run_dfs(maze: Maze) -> SearchResult:
    """Ejecuta el algoritmo DFS sobre el laberinto dado.

    Args:
        maze: Instancia de Maze con la configuracion del laberinto.

    Returns:
        SearchResult con los resultados de la busqueda DFS.
    """
    return dfs(maze)


def run_both(maze: Maze) -> dict:
    """Ejecuta BFS y DFS sobre el mismo laberinto y retorna ambos resultados.

    Args:
        maze: Instancia de Maze con la configuracion del laberinto.

    Returns:
        Diccionario con claves 'bfs' y 'dfs', cada una con el resultado
        serializado del algoritmo correspondiente.
    """
    result_bfs = bfs(maze)
    result_dfs = dfs(maze)
    return {
        "bfs": result_bfs.to_dict(),
        "dfs": result_dfs.to_dict(),
    }
