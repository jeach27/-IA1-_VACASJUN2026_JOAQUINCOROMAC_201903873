# history.py
# Gestion del historial de diagnosticos realizados.
# Persistimos cada diagnostico en un archivo JSON dentro de la carpeta data/.

import json
import uuid
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

RUTA_HISTORIAL = Path(__file__).parent / 'data' / 'historial.json'


def _cargar_historial():
    """Lee el historial desde el archivo JSON. Si no existe, retorna lista vacia."""
    RUTA_HISTORIAL.parent.mkdir(exist_ok=True)
    if not RUTA_HISTORIAL.exists():
        return []
    with open(RUTA_HISTORIAL, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)


def _persistir_historial(historial):
    """Escribe el historial completo al archivo JSON."""
    RUTA_HISTORIAL.parent.mkdir(exist_ok=True)
    with open(RUTA_HISTORIAL, 'w', encoding='utf-8') as archivo:
        json.dump(historial, archivo, ensure_ascii=False, indent=2)


def guardar_diagnostico(sintomas, diagnosticos):
    """
    Guarda un nuevo registro de diagnostico en el historial.
    Recibe la lista de sintomas y la lista de diagnosticos obtenidos.
    Retorna el registro creado con su id y fecha.
    """
    historial = _cargar_historial()

    registro = {
        'id': str(uuid.uuid4())[:8],
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sintomas': sintomas,
        'diagnosticos': diagnosticos
    }

    historial.append(registro)
    _persistir_historial(historial)
    logger.info("Diagnostico guardado con id %s", registro['id'])
    return registro


def obtener_historial():
    """
    Retorna todos los diagnosticos guardados, del mas reciente al mas antiguo.
    """
    historial = _cargar_historial()
    return list(reversed(historial))
