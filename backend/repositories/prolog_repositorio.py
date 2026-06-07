"""
Repositorio Prolog: unica capa que se comunica directamente con SWI-Prolog
mediante PySwip. No contiene logica de negocio; solo ejecuta consultas.
"""

import os
import shutil
from typing import List, Tuple, Optional

# PySwip busca SWI-Prolog en el registro de Windows o en rutas predefinidas.
# Si SWI-Prolog esta instalado en una ruta personalizada, auto-detectamos
# el directorio home a partir del ejecutable encontrado en el PATH.
if not os.environ.get("SWI_HOME_DIR") and not os.environ.get("SWIPL"):
    _swipl_exe = shutil.which("swipl")
    if _swipl_exe:
        os.environ["SWI_HOME_DIR"] = os.path.dirname(os.path.dirname(_swipl_exe))

try:
    from pyswip import Prolog
except (IndexError, OSError) as exc:
    raise RuntimeError(
        "PySwip no pudo localizar SWI-Prolog. "
        "Asegurate de que SWI-Prolog este instalado y disponible en el PATH. "
        "Descargalo desde https://www.swi-prolog.org/Download.html"
    ) from exc


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
        resultados = list(self._prolog.query("conexion(Origen, Destino, Distancia)"))
        return [(str(r["Origen"]), str(r["Destino"]), int(r["Distancia"])) for r in resultados]

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
        consulta = f"ruta({origen}, {destino}, Ruta, Distancia)"
        resultados = list(self._prolog.query(consulta))
        rutas = [([str(c) for c in r["Ruta"]], int(r["Distancia"])) for r in resultados]
        return sorted(rutas, key=lambda x: x[1])

    # ------------------------------------------------------------------
    # Operaciones de escritura
    # ------------------------------------------------------------------

    def agregar_conexion(self, ciudad1: str, ciudad2: str, distancia: int) -> None:
        consulta = f"agregar_conexion({ciudad1}, {ciudad2}, {distancia})"
        list(self._prolog.query(consulta))
