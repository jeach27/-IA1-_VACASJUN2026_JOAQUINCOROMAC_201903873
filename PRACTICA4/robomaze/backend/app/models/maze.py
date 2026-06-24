"""
Modelo del laberinto. Representa la cuadricula bidimensional y expone la
logica de vecinos validos utilizada por los algoritmos de busqueda.
"""


class Maze:
    """Laberinto representado como cuadricula de enteros.

    Cada celda tiene valor 0 (libre) o 1 (obstaculo).
    Las coordenadas son tuplas (fila, columna).
    """

    def __init__(self, rows: int, cols: int, grid: list, start: tuple, end: tuple):
        """
        Args:
            rows: Numero de filas del laberinto.
            cols: Numero de columnas del laberinto.
            grid: Lista de listas de enteros (0=libre, 1=obstaculo).
            start: Tupla (fila, columna) con la posicion inicial.
            end: Tupla (fila, columna) con la posicion objetivo.
        """
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.start = tuple(start)
        self.end = tuple(end)

    def get_neighbors(self, row: int, col: int) -> list:
        """Retorna las celdas adyacentes validas desde (row, col).

        Solo se consideran las cuatro direcciones cardinales: arriba, abajo,
        izquierda y derecha. Se excluyen celdas fuera de limites y obstaculos.

        Args:
            row: Fila de la celda actual.
            col: Columna de la celda actual.

        Returns:
            Lista de tuplas (fila, columna) de vecinos validos.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] == 0:
                    neighbors.append((nr, nc))
        return neighbors
