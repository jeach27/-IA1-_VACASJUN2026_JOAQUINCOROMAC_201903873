"""
Implementacion manual de A* (A-estrella) para laberintos.
Utiliza distancia Manhattan como heuristica admisible.
No se usa ninguna libreria externa de busqueda de rutas.
"""

import heapq
import time

from app.models.maze import Maze
from app.models.search_result import SearchResult


def astar(maze: Maze) -> SearchResult:
    """Encuentra la ruta optima entre inicio y destino usando A*.

    Estrategia: expande primero los nodos con menor f(n) = g(n) + h(n),
    donde g(n) es el costo real desde el inicio y h(n) es la distancia
    Manhattan al destino. Garantiza la ruta optima porque la heuristica
    es admisible (nunca sobreestima el costo real).

    Complejidad temporal: O(V log V) por el uso de heap.
    Complejidad espacial: O(V) para el heap y el diccionario de padres.

    Args:
        maze: Instancia del laberinto con grid, start y end definidos.

    Returns:
        SearchResult con la ruta optima, nodos explorados, orden de
        exploracion y tiempo de ejecucion. Si no existe ruta, found=False.
    """
    start_time = time.time()

    start = maze.start
    end = maze.end

    def heuristic(row: int, col: int) -> int:
        return abs(row - end[0]) + abs(col - end[1])

    # Entradas del heap: (f_score, g_score, fila, col)
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start[0], start[1]), 0, start[0], start[1]))

    g_scores = {start: 0}
    parents = {start: None}
    closed = set()
    explored_nodes = 0
    explored_order = []
    found = False

    while open_heap:
        f, g, r, c = heapq.heappop(open_heap)
        current = (r, c)

        if current in closed:
            continue

        closed.add(current)
        explored_nodes += 1
        explored_order.append(list(current))

        if current == end:
            found = True
            break

        for neighbor in maze.get_neighbors(r, c):
            if neighbor in closed:
                continue
            tentative_g = g + 1
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                parents[neighbor] = current
                f_new = tentative_g + heuristic(neighbor[0], neighbor[1])
                heapq.heappush(open_heap, (f_new, tentative_g, neighbor[0], neighbor[1]))

    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000

    if not found:
        return SearchResult(
            algorithm="A*",
            path=[],
            explored_nodes=explored_nodes,
            execution_time_ms=execution_time_ms,
            found=False,
            explored_order=explored_order,
        )

    path = _reconstruct_path(parents, start, end)

    return SearchResult(
        algorithm="A*",
        path=path,
        explored_nodes=explored_nodes,
        execution_time_ms=execution_time_ms,
        found=True,
        explored_order=explored_order,
    )


def _reconstruct_path(parents: dict, start: tuple, end: tuple) -> list:
    """Reconstruye la ruta desde el destino hasta el inicio y la invierte."""
    path = []
    current = end
    while current is not None:
        path.append(list(current))
        current = parents[current]
    path.reverse()
    return path
