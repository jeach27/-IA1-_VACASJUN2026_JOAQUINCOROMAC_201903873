"""
Servicio de generacion automatica de laberintos.
Implementa un generador basado en DFS aleatorizado (recursive backtracker)
que produce laberintos perfectos: un unico camino entre cualquier par de celdas.
"""

import random
from collections import deque


def generate_maze(rows: int, cols: int, seed: int = None) -> dict:
    """Genera un laberinto aleatorio usando DFS aleatorizado.

    El algoritmo trabaja sobre una cuadricula logica de celdas (positions)
    separadas por muros. Parte de todas las celdas bloqueadas y va abriendo
    caminos entre celdas vecinas de forma aleatoria hasta conectarlas todas.

    Args:
        rows: Numero de filas del laberinto (minimo 5, maximo 25).
        cols: Numero de columnas del laberinto (minimo 5, maximo 25).
        seed: Semilla para reproducibilidad. Si es None, es aleatorio.

    Returns:
        Diccionario con rows, cols, grid, start y end listo para la API.
    """
    rows = max(5, min(25, rows))
    cols = max(5, min(25, cols))

    if seed is not None:
        random.seed(seed)

    # Comenzar con todas las celdas como obstaculos.
    grid = [[1] * cols for _ in range(rows)]

    # La celda (0, 0) es el inicio; marcarla como libre.
    grid[0][0] = 0
    visited = {(0, 0)}
    stack = [(0, 0)]

    # DFS aleatorizado: moverse de 2 en 2 para que queden paredes entre celdas.
    while stack:
        r, c = stack[-1]
        # Vecinos a 2 pasos de distancia que no han sido visitados.
        neighbors = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                neighbors.append((nr, nc, r + dr // 2, c + dc // 2))

        if neighbors:
            nr, nc, wr, wc = random.choice(neighbors)
            # Abrir la celda destino y el muro intermedio.
            grid[nr][nc] = 0
            grid[wr][wc] = 0
            visited.add((nr, nc))
            stack.append((nr, nc))
        else:
            stack.pop()

    # El destino es la ultima celda visitada que este libre en la esquina opuesta.
    end = _find_end(grid, rows, cols)

    # Garantizar que inicio y destino esten libres.
    grid[0][0] = 0
    grid[end[0]][end[1]] = 0

    return {
        "rows": rows,
        "cols": cols,
        "grid": grid,
        "start": [0, 0],
        "end": end,
    }


def _find_end(grid: list, rows: int, cols: int) -> list:
    """Busca la celda libre mas lejana al origen en la esquina inferior derecha."""
    # Intentar celdas desde la esquina inferior derecha hacia el origen.
    for r in range(rows - 1, rows // 2 - 1, -1):
        for c in range(cols - 1, cols // 2 - 1, -1):
            if grid[r][c] == 0:
                return [r, c]
    # Fallback: asegurar que la ultima celda este libre.
    grid[rows - 1][cols - 1] = 0
    return [rows - 1, cols - 1]
