"""
Implementacion manual de Breadth-First Search (BFS) para laberintos.
No se utiliza ninguna libreria externa de busqueda de rutas.
"""

import time
from collections import deque

from app.models.maze import Maze
from app.models.search_result import SearchResult


def bfs(maze: Maze) -> SearchResult:
    """Encuentra la ruta mas corta entre inicio y destino usando BFS.

    Estrategia: explora nivel por nivel desde el nodo inicial, garantizando
    que la primera vez que se alcanza el destino la ruta es optima (minima
    cantidad de celdas).

    Complejidad temporal: O(V + E) donde V = filas*columnas, E = aristas entre
    celdas adyacentes libres.
    Complejidad espacial: O(V) para la cola y el diccionario de padres.

    Args:
        maze: Instancia del laberinto con grid, start y end definidos.

    Returns:
        SearchResult con la ruta encontrada, nodos explorados y tiempo
        de ejecucion. Si no existe ruta, found=False y path=[].
    """
    start_time = time.time()

    start = maze.start
    end = maze.end

    queue = deque()
    queue.append(start)

    visited = set()
    visited.add(start)

    parents = {start: None}
    explored_nodes = 0

    found = False

    while queue:
        current = queue.popleft()
        explored_nodes += 1

        if current == end:
            found = True
            break

        for neighbor in maze.get_neighbors(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = current
                queue.append(neighbor)

    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000

    if not found:
        return SearchResult(
            algorithm="BFS",
            path=[],
            explored_nodes=explored_nodes,
            execution_time_ms=execution_time_ms,
            found=False,
        )

    path = _reconstruct_path(parents, start, end)

    return SearchResult(
        algorithm="BFS",
        path=path,
        explored_nodes=explored_nodes,
        execution_time_ms=execution_time_ms,
        found=True,
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
