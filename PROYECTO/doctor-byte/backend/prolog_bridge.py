# prolog_bridge.py
# Comunicacion entre Python y SWI-Prolog mediante pyswip.
# Cargamos la base de conocimiento una sola vez y exponemos funciones de consulta.

import logging
from pathlib import Path
from pyswip import Prolog

logger = logging.getLogger(__name__)

RUTA_BASE_CONOCIMIENTO = Path(__file__).parent.parent / 'prolog' / 'knowledge_base.pl'

_prolog = None


def _obtener_instancia():
    """Retorna la instancia singleton de Prolog con la base de conocimiento cargada."""
    global _prolog
    if _prolog is None:
        _prolog = Prolog()
        _prolog.consult(str(RUTA_BASE_CONOCIMIENTO))
        logger.info("Base de conocimiento cargada desde %s", RUTA_BASE_CONOCIMIENTO)
    return _prolog


def recargar():
    """Descarta la instancia actual de Prolog para que se recargue en la proxima consulta."""
    global _prolog
    _prolog = None
    logger.info("Instancia de Prolog descartada; se recargara en la proxima consulta")


def _atom_a_str(valor):
    """Convierte un valor retornado por pyswip a cadena de texto legible."""
    if isinstance(valor, bytes):
        return valor.decode('utf-8')
    return str(valor)


def consultar_sintomas():
    """
    Consulta todos los sintomas disponibles en la base de conocimiento.
    Retorna una lista de strings con los nombres de los sintomas.
    """
    prolog = _obtener_instancia()
    resultados = list(prolog.query("listar_sintomas(Sintomas)"))
    if not resultados:
        return []
    return [_atom_a_str(s) for s in resultados[0]['Sintomas']]


def consultar_diagnostico(sintomas):
    """
    Dado una lista de nombres de sintomas, consulta las fallas diagnosticadas.
    Retorna una lista de diccionarios con 'falla' y 'recomendacion'.
    """
    prolog = _obtener_instancia()

    if not sintomas:
        return []

    # Construimos la lista de sintomas en formato Prolog: [sintoma1, sintoma2, ...]
    lista_prolog = '[' + ', '.join(sintomas) + ']'

    # Obtenemos las fallas diagnosticadas para esta combinacion de sintomas
    query_diagnosticos = f"obtener_diagnosticos({lista_prolog}, Diagnosticos)"
    resultados = list(prolog.query(query_diagnosticos))

    if not resultados or not resultados[0]['Diagnosticos']:
        return []

    diagnosticos = []
    for falla in resultados[0]['Diagnosticos']:
        falla_str = _atom_a_str(falla)

        # Obtenemos la recomendacion asociada a esta falla
        query_rec = f"recomendacion({falla_str}, Recomendacion)"
        rec_resultados = list(prolog.query(query_rec))

        if rec_resultados:
            recomendacion = _atom_a_str(rec_resultados[0]['Recomendacion'])
        else:
            recomendacion = 'No hay recomendacion disponible para esta falla.'

        diagnosticos.append({
            'falla': falla_str,
            'recomendacion': recomendacion
        })

    return diagnosticos
