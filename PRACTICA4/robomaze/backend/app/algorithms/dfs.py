"""
Implementacion manual de Depth-First Search (DFS) para laberintos.
No se utiliza ninguna libreria externa de busqueda de rutas.
"""

import time

from app.models.maze import Maze
from app.models.search_result import SearchResult


def dfs(maze: Maze) -> SearchResult:
    """Encuentra una ruta entre inicio y destino usando DFS.

    Estrategia: explora tan profundo como sea posible por cada rama antes
    de retroceder. No garantiza la ruta optima; la primera solucion que
    encuentra depende del orden en que se visitan los vecinos.

    Complejidad temporal: O(V + E) donde V = filas*columnas, E = aristas entre
    celdas adyacentes libres.
    Complejidad espacial: O(V) para la pila y el diccionario de padres.

    Args:
        maze: Instancia del laberinto con grid, start y end definidos.

    Returns:
        SearchResult con la ruta encontrada, nodos explorados y tiempo
        de ejecucion. Si no existe ruta, found=False y path=[].
    """
    start_time = time.time()

    start = maze.start
    end = maze.end

    stack = [start]

    visited = set()
    visited.add(start)

    parents = {start: None}
    explored_nodes = 0
    explored_order = []

    found = False

    while stack:
        current = stack.pop()
        explored_nodes += 1
        explored_order.append(list(current))

        if current == end:
            found = True
            break

        for neighbor in maze.get_neighbors(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = current
                stack.append(neighbor)

    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000

    if not found:
        return SearchResult(
            algorithm="DFS",
            path=[],
            explored_nodes=explored_nodes,
            execution_time_ms=execution_time_ms,
            found=False,
            explored_order=explored_order,
        )

    path = _reconstruct_path(parents, start, end)

    return SearchResult(
        algorithm="DFS",
        path=path,
        explored_nodes=explored_nodes,
        execution_time_ms=execution_time_ms,
        found=True,
        explored_order=explored_order,
    )


def _reconstruct_path(parents: dict, start: tuple, end: tuple) -> list:
    """Reconstruye la ruta desde el destino hasta el inicio y la invierte.

    Args:
        parents: Diccionario nodo -> nodo_padre.
        start: Nodo inicial.
        end: Nodo objetivo.

    Returns:
        Lista de tuplas ordenada desde inicio hasta destino.
    """
    path = []
    current = end
    while current is not None:
        path.append(list(current))
        current = parents[current]
    path.reverse()
    return path
