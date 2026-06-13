# admin_manager.py
# Operaciones CRUD sobre knowledge_store.json y bot_config.json.
# Cada operacion de escritura llama a kb_generator para mantener el .pl sincronizado.

import json
import logging
import re
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

RUTA_STORE = Path(__file__).parent / 'data' / 'knowledge_store.json'
RUTA_BOT_CONFIG = Path(__file__).parent / 'data' / 'bot_config.json'

_RE_NOMBRE_VALIDO = re.compile(r'^[a-z][a-z0-9_]*$')


def _validar_nombre(nombre):
    """Lanza ValueError si el nombre no es un atomo Prolog valido."""
    if not nombre or not _RE_NOMBRE_VALIDO.match(nombre):
        raise ValueError(
            f"El nombre '{nombre}' no es valido. "
            "Debe comenzar con letra minuscula y contener solo letras, digitos y guiones bajos."
        )


def _cargar_store():
    with open(RUTA_STORE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _guardar_store(store):
    RUTA_STORE.parent.mkdir(exist_ok=True)
    with open(RUTA_STORE, 'w', encoding='utf-8') as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


def _guardar_y_regenerar(store):
    """Persiste el store y regenera el archivo .pl."""
    _guardar_store(store)
    from kb_generator import regenerar_base_conocimiento
    regenerar_base_conocimiento()


# =============================================================================
# SINTOMAS
# =============================================================================

def obtener_sintomas():
    return _cargar_store()['sintomas']


def agregar_sintoma(nombre, etiqueta):
    _validar_nombre(nombre)
    if not etiqueta or not etiqueta.strip():
        raise ValueError("La etiqueta no puede estar vacia")
    store = _cargar_store()
    if any(s['nombre'] == nombre for s in store['sintomas']):
        raise ValueError(f"Ya existe el sintoma '{nombre}'")
    store['sintomas'].append({'nombre': nombre, 'etiqueta': etiqueta.strip()})
    _guardar_y_regenerar(store)


def actualizar_sintoma(nombre_original, nombre_nuevo, etiqueta):
    _validar_nombre(nombre_nuevo)
    if not etiqueta or not etiqueta.strip():
        raise ValueError("La etiqueta no puede estar vacia")
    store = _cargar_store()
    encontrado = False
    for s in store['sintomas']:
        if s['nombre'] == nombre_original:
            if nombre_nuevo != nombre_original and any(x['nombre'] == nombre_nuevo for x in store['sintomas']):
                raise ValueError(f"Ya existe el sintoma '{nombre_nuevo}'")
            s['nombre'] = nombre_nuevo
            s['etiqueta'] = etiqueta.strip()
            encontrado = True
            break
    if not encontrado:
        raise ValueError(f"No se encontro el sintoma '{nombre_original}'")
    # Actualizamos referencias en reglas si cambio el nombre
    if nombre_nuevo != nombre_original:
        for regla in store['reglas']:
            regla['sintomas_requeridos'] = [
                nombre_nuevo if x == nombre_original else x
                for x in regla['sintomas_requeridos']
            ]
            regla['sintomas_negados'] = [
                nombre_nuevo if x == nombre_original else x
                for x in regla['sintomas_negados']
            ]
    _guardar_y_regenerar(store)


def eliminar_sintoma(nombre):
    store = _cargar_store()
    store['sintomas'] = [s for s in store['sintomas'] if s['nombre'] != nombre]
    _guardar_y_regenerar(store)


# =============================================================================
# FALLAS
# =============================================================================

def obtener_fallas():
    return _cargar_store()['fallas']


def agregar_falla(nombre, etiqueta):
    _validar_nombre(nombre)
    if not etiqueta or not etiqueta.strip():
        raise ValueError("La etiqueta no puede estar vacia")
    store = _cargar_store()
    if any(f['nombre'] == nombre for f in store['fallas']):
        raise ValueError(f"Ya existe la falla '{nombre}'")
    store['fallas'].append({'nombre': nombre, 'etiqueta': etiqueta.strip()})
    _guardar_y_regenerar(store)


def actualizar_falla(nombre_original, nombre_nuevo, etiqueta):
    _validar_nombre(nombre_nuevo)
    if not etiqueta or not etiqueta.strip():
        raise ValueError("La etiqueta no puede estar vacia")
    store = _cargar_store()
    encontrado = False
    for f in store['fallas']:
        if f['nombre'] == nombre_original:
            if nombre_nuevo != nombre_original and any(x['nombre'] == nombre_nuevo for x in store['fallas']):
                raise ValueError(f"Ya existe la falla '{nombre_nuevo}'")
            f['nombre'] = nombre_nuevo
            f['etiqueta'] = etiqueta.strip()
            encontrado = True
            break
    if not encontrado:
        raise ValueError(f"No se encontro la falla '{nombre_original}'")
    if nombre_nuevo != nombre_original:
        for r in store['reglas']:
            if r['falla'] == nombre_original:
                r['falla'] = nombre_nuevo
        for r in store['recomendaciones']:
            if r['falla'] == nombre_original:
                r['falla'] = nombre_nuevo
    _guardar_y_regenerar(store)


def eliminar_falla(nombre):
    store = _cargar_store()
    store['fallas'] = [f for f in store['fallas'] if f['nombre'] != nombre]
    _guardar_y_regenerar(store)


# =============================================================================
# RECOMENDACIONES
# =============================================================================

def obtener_recomendaciones():
    return _cargar_store()['recomendaciones']


def actualizar_recomendacion(falla, texto):
    if not texto or not texto.strip():
        raise ValueError("El texto de la recomendacion no puede estar vacio")
    store = _cargar_store()
    for r in store['recomendaciones']:
        if r['falla'] == falla:
            r['texto'] = texto.strip()
            _guardar_y_regenerar(store)
            return
    store['recomendaciones'].append({'falla': falla, 'texto': texto.strip()})
    _guardar_y_regenerar(store)


def eliminar_recomendacion(falla):
    store = _cargar_store()
    store['recomendaciones'] = [r for r in store['recomendaciones'] if r['falla'] != falla]
    _guardar_y_regenerar(store)


# =============================================================================
# REGLAS
# =============================================================================

def obtener_reglas():
    return _cargar_store()['reglas']


def agregar_regla(falla, sintomas_requeridos, sintomas_negados, usa_corte, descripcion):
    if not falla:
        raise ValueError("La falla es obligatoria")
    if not sintomas_requeridos and not sintomas_negados:
        raise ValueError("La regla debe tener al menos un sintoma requerido o negado")
    store = _cargar_store()
    nueva = {
        'id': 'r' + str(uuid.uuid4())[:6],
        'falla': falla,
        'sintomas_requeridos': list(sintomas_requeridos),
        'sintomas_negados': list(sintomas_negados),
        'usa_corte': bool(usa_corte),
        'descripcion': (descripcion or '').strip(),
    }
    store['reglas'].append(nueva)
    _guardar_y_regenerar(store)
    return nueva


def actualizar_regla(id_regla, falla, sintomas_requeridos, sintomas_negados, usa_corte, descripcion):
    if not falla:
        raise ValueError("La falla es obligatoria")
    store = _cargar_store()
    for r in store['reglas']:
        if r['id'] == id_regla:
            r['falla'] = falla
            r['sintomas_requeridos'] = list(sintomas_requeridos)
            r['sintomas_negados'] = list(sintomas_negados)
            r['usa_corte'] = bool(usa_corte)
            r['descripcion'] = (descripcion or '').strip()
            _guardar_y_regenerar(store)
            return r
    raise ValueError(f"No se encontro la regla '{id_regla}'")


def eliminar_regla(id_regla):
    store = _cargar_store()
    store['reglas'] = [r for r in store['reglas'] if r['id'] != id_regla]
    _guardar_y_regenerar(store)


# =============================================================================
# ASOCIACIONES (lectura derivada de reglas + recomendaciones)
# =============================================================================

def obtener_asociaciones():
    """
    Retorna una vista agrupada por falla con sus sintomas de activacion y recomendacion.
    Usada por la seccion de asociaciones del panel admin.
    """
    store = _cargar_store()
    rec_map = {r['falla']: r['texto'] for r in store['recomendaciones']}
    falla_map = {f['nombre']: f['etiqueta'] for f in store['fallas']}
    sint_map = {s['nombre']: s['etiqueta'] for s in store['sintomas']}

    agrupado = {}
    for regla in store['reglas']:
        falla = regla['falla']
        if falla not in agrupado:
            agrupado[falla] = {
                'falla': falla,
                'etiqueta_falla': falla_map.get(falla, falla),
                'recomendacion': rec_map.get(falla, ''),
                'reglas': [],
            }
        agrupado[falla]['reglas'].append({
            'id': regla['id'],
            'sintomas_requeridos': [
                {'nombre': s, 'etiqueta': sint_map.get(s, s)}
                for s in regla['sintomas_requeridos']
            ],
            'sintomas_negados': [
                {'nombre': s, 'etiqueta': sint_map.get(s, s)}
                for s in regla['sintomas_negados']
            ],
        })

    return list(agrupado.values())


# =============================================================================
# CONFIGURACION DEL BOT
# =============================================================================

def obtener_config_bot():
    if RUTA_BOT_CONFIG.exists():
        with open(RUTA_BOT_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'chat_id': '',
        'habilitado': True,
        'mensajes': {
            'sin_diagnostico': 'No se encontraron fallas especificas para los sintomas indicados.',
            'bienvenida': 'Bienvenido a Doctor Byte. Sistema experto de diagnostico de fallas en computadoras.',
        }
    }


def actualizar_config_bot(chat_id, habilitado, mensajes):
    config = {
        'chat_id': (chat_id or '').strip(),
        'habilitado': bool(habilitado),
        'mensajes': {
            'sin_diagnostico': mensajes.get('sin_diagnostico', '').strip(),
            'bienvenida': mensajes.get('bienvenida', '').strip(),
        }
    }
    RUTA_BOT_CONFIG.parent.mkdir(exist_ok=True)
    with open(RUTA_BOT_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    logger.info("Configuracion del bot actualizada")
    return config
