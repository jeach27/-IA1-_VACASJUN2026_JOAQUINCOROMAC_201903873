"""
Servicio de laberintos. Construye instancias de Maze a partir de datos
recibidos y provee los 5 laberintos predefinidos para pruebas.
"""

from app.models.maze import Maze


def build_maze(data: dict) -> Maze:
    """Construye una instancia de Maze a partir de un diccionario de datos.

    Args:
        data: Diccionario con claves rows, cols, grid, start y end.

    Returns:
        Instancia de Maze lista para ser procesada por los algoritmos.
    """
    return Maze(
        rows=data["rows"],
        cols=data["cols"],
        grid=data["grid"],
        start=tuple(data["start"]),
        end=tuple(data["end"]),
    )


def get_predefined_mazes() -> list:
    """Retorna la lista de los 5 laberintos predefinidos para pruebas.

    Los laberintos cubren casos variados: camino simple, medio, largo,
    sin solucion y complejo. Todos son cuadriculas de 10x10.
    Valor 0 = celda libre, valor 1 = obstaculo.

    Returns:
        Lista de diccionarios, cada uno con id, name, rows, cols, grid,
        start y end.
    """
    return [
        {
            "id": 1,
            "name": "simple",
            "description": "Laberinto sencillo con camino directo",
            "rows": 10,
            "cols": 10,
            "start": [0, 0],
            "end": [9, 9],
            "grid": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 1, 0, 1, 1, 0, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
        },
        {
            "id": 2,
            "name": "medio",
            "description": "Laberinto de dificultad media con varios pasillos",
            "rows": 10,
            "cols": 10,
            "start": [0, 0],
            "end": [9, 9],
            "grid": [
                [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            ],
        },
        {
            "id": 3,
            "name": "largo",
            "description": "Laberinto con ruta larga en forma de espiral",
            "rows": 10,
            "cols": 10,
            "start": [0, 0],
            "end": [9, 9],
            "grid": [
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                [1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
            ],
        },
        {
            "id": 4,
            "name": "sinruta",
            "description": "Laberinto sin solucion posible (muro completo central)",
            "rows": 10,
            "cols": 10,
            "start": [0, 0],
            "end": [9, 9],
            "grid": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
        },
        {
            "id": 5,
            "name": "complejo",
            "description": "Laberinto complejo con multiples bifurcaciones",
            "rows": 10,
            "cols": 10,
            "start": [0, 0],
            "end": [9, 9],
            "grid": [
                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                [1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                [1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                [1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
            ],
        },
    ]
