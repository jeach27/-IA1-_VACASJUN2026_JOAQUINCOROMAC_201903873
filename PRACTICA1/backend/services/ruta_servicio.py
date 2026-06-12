"""
Servicio de rutas: contiene la logica de negocio.
Coordina las llamadas al repositorio y construye las respuestas
que los routers devuelven al frontend.
"""

from typing import List
from fastapi import HTTPException, status

from repositories.prolog_repositorio import PrologRepositorio
from models.esquemas import (
    RespuestaRutaMasCorta,
    RespuestaTodasRutas,
    RutaResultado,
    RespuestaCiudades,
    RespuestaConexiones,
    ConexionInfo,
    RespuestaExito,
)


class RutaServicio:
    """
    Orquesta la consulta al repositorio y aplica reglas de negocio:
    - Validacion de existencia de ciudades.
    - Construccion de respuestas tipadas.
    - Generacion de errores HTTP cuando no hay ruta disponible.
    """

    def __init__(self, repositorio: PrologRepositorio):
        self._repo = repositorio

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def obtener_ciudades(self) -> RespuestaCiudades:
        ciudades = self._repo.obtener_ciudades()
        return RespuestaCiudades(ciudades=ciudades, total=len(ciudades))

    def obtener_conexiones(self) -> RespuestaConexiones:
        raw = self._repo.obtener_conexiones()
        conexiones = [
            ConexionInfo(origen=o, destino=d, distancia=dist)
            for o, d, dist in raw
        ]
        return RespuestaConexiones(conexiones=conexiones, total=len(conexiones))

    def ruta_mas_corta(self, origen: str, destino: str) -> RespuestaRutaMasCorta:
        self._validar_ciudades(origen, destino)
        resultado = self._repo.obtener_ruta_mas_corta(
            origen.lower(), destino.lower()
        )
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe ruta entre {origen} y {destino}.",
            )
        ciudades, distancia = resultado
        return RespuestaRutaMasCorta(
            origen=origen,
            destino=destino,
            ruta=ciudades,
            distancia=distancia,
        )

    def todas_las_rutas(self, origen: str, destino: str) -> RespuestaTodasRutas:
        self._validar_ciudades(origen, destino)
        raw = self._repo.obtener_todas_rutas(origen.lower(), destino.lower())
        if not raw:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe ninguna ruta entre {origen} y {destino}.",
            )
        rutas = [
            RutaResultado(ciudades=ciudades, distancia=distancia)
            for ciudades, distancia in raw
        ]
        return RespuestaTodasRutas(
            origen=origen,
            destino=destino,
            rutas=rutas,
            total_rutas=len(rutas),
        )

    # ------------------------------------------------------------------
    # Operaciones de escritura
    # ------------------------------------------------------------------

    def agregar_conexion(
        self, ciudad1: str, ciudad2: str, distancia: int
    ) -> RespuestaExito:
        ciudad1 = ciudad1.lower().replace(" ", "_")
        ciudad2 = ciudad2.lower().replace(" ", "_")
        self._repo.agregar_conexion(ciudad1, ciudad2, distancia)
        return RespuestaExito(
            mensaje=f"Conexion entre {ciudad1} y {ciudad2} ({distancia} km) agregada correctamente."
        )

    # ------------------------------------------------------------------
    # Validacion interna
    # ------------------------------------------------------------------

    def _validar_ciudades(self, origen: str, destino: str) -> None:
        origen_norm = origen.lower().replace(" ", "_")
        destino_norm = destino.lower().replace(" ", "_")

        if not self._repo.ciudad_existe(origen_norm):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La ciudad de origen '{origen}' no existe en la base de conocimiento.",
            )
        if not self._repo.ciudad_existe(destino_norm):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La ciudad de destino '{destino}' no existe en la base de conocimiento.",
            )
        if origen_norm == destino_norm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La ciudad de origen y destino no pueden ser la misma.",
            )
