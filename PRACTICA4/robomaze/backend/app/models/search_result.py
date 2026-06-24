"""
Modelo del resultado de busqueda. Encapsula la salida que producen
los algoritmos BFS y DFS tras explorar el laberinto.
"""


class SearchResult:
    """Resultado de la ejecucion de un algoritmo de busqueda.

    Attributes:
        algorithm: Nombre del algoritmo utilizado ('BFS' o 'DFS').
        path: Lista de tuplas (fila, columna) que forman la ruta encontrada.
              Lista vacia si no existe ruta.
        explored_nodes: Cantidad de nodos procesados durante la busqueda.
        execution_time_ms: Tiempo de ejecucion en milisegundos.
        found: True si se encontro una ruta valida, False en caso contrario.
    """

    def __init__(
        self,
        algorithm: str,
        path: list,
        explored_nodes: int,
        execution_time_ms: float,
        found: bool,
    ):
        self.algorithm = algorithm
        self.path = path
        self.explored_nodes = explored_nodes
        self.execution_time_ms = execution_time_ms
        self.found = found

    def to_dict(self) -> dict:
        """Convierte el resultado a un diccionario serializable en JSON."""
        return {
            "algorithm": self.algorithm,
            "path": self.path,
            "path_length": len(self.path),
            "explored_nodes": self.explored_nodes,
            "execution_time_ms": round(self.execution_time_ms, 4),
            "found": self.found,
        }
