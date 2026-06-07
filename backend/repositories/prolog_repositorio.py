"""
Repositorio Prolog: unica capa que se comunica directamente con SWI-Prolog
mediante PySwip. No contiene logica de negocio; solo ejecuta consultas.
"""

import os
from typing import List, Tuple, Optional
from pyswip import Prolog


# Ruta absoluta al archivo .pl para que funcione desde cualquier directorio
_RUTA_PL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "prolog",
    "ciudades.pl",
)


class PrologRepositorio:
    """
    Encapsula todas las consultas directas a la base de conocimiento Prolog.
    Se instancia una sola vez (singleton gestionado por el servicio).
    """

    def __init__(self):
        self._prolog = Prolog()
        self._prolog.consult(_RUTA_PL)

    # ------------------------------------------------------------------
    # Consultas de lectura
    # ------------------------------------------------------------------

    def obtener_ciudades(self) -> List[str]:
        resultados = list(self._prolog.query("todas_ciudades(Ciudades)"))
        if not resultados:
            return []
        return [str(c) for c in resultados[0]["Ciudades"]]

    def obtener_conexiones(self) -> List[Tuple[str, str, int]]:
        resultados = list(self._prolog.query("todas_conexiones(Conexiones)"))
        if not resultados:
            return []
        conexiones = []
        for item in resultados[0]["Conexiones"]:
            # item tiene la forma ciudad1-ciudad2-distancia en Prolog
            origen = str(item.args[0].args[0])
            destino = str(item.args[0].args[1])
            distancia = int(item.args[1])
            conexiones.append((origen, destino, distancia))
        return conexiones

    def ciudad_existe(self, ciudad: str) -> bool:
        consulta = f"ciudad_existe({ciudad})"
        return bool(list(self._prolog.query(consulta)))

    def obtener_ruta_mas_corta(
        self, origen: str, destino: str
    ) -> Optional[Tuple[List[str], int]]:
        consulta = f"ruta_mas_corta({origen}, {destino}, Ruta, Distancia)"
        resultados = list(self._prolog.query(consulta))
        if not resultados:
            return None
        ciudades = [str(c) for c in resultados[0]["Ruta"]]
        distancia = int(resultados[0]["Distancia"])
        return (ciudades, distancia)

    def obtener_todas_rutas(
        self, origen: str, destino: str
    ) -> List[Tuple[List[str], int]]:
        consulta = f"todas_las_rutas({origen}, {destino}, Rutas)"
        resultados = list(self._prolog.query(consulta))
        if not resultados:
            return []
        rutas = []
        for item in resultados[0]["Rutas"]:
            # Cada item tiene la forma Distancia-ListaCiudades
            distancia = int(item.args[0])
            ciudades = [str(c) for c in item.args[1]]
            rutas.append((ciudades, distancia))
        return rutas

    # ------------------------------------------------------------------
    # Operaciones de escritura
    # ------------------------------------------------------------------

    def agregar_conexion(self, ciudad1: str, ciudad2: str, distancia: int) -> None:
        consulta = f"agregar_conexion({ciudad1}, {ciudad2}, {distancia})"
        list(self._prolog.query(consulta))
