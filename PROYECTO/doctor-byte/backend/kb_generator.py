# kb_generator.py
# Genera el archivo knowledge_base.pl a partir de knowledge_store.json.
# Llamamos esta funcion cada vez que el admin modifica la base de conocimiento.

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

RUTA_STORE = Path(__file__).parent / 'data' / 'knowledge_store.json'
RUTA_PL = Path(__file__).parent.parent / 'prolog' / 'knowledge_base.pl'


def _cargar_store():
    with open(RUTA_STORE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _escapar_texto_prolog(texto):
    """Escapa comillas simples dentro de textos que iran como atomos Prolog."""
    return texto.replace("'", "\\'")


def _generar_regla(regla):
    """Convierte un diccionario de regla en lineas Prolog validas."""
    lineas = []
    lineas.append(f"% Regla {regla['id']}: {regla['descripcion']}")
    lineas.append(f"diagnostico(Sintomas, {regla['falla']}) :-")

    condiciones = []
    for s in regla.get('sintomas_requeridos', []):
        condiciones.append(f"    member({s}, Sintomas)")
    for s in regla.get('sintomas_negados', []):
        condiciones.append(f"    \\+ member({s}, Sintomas)")
    if regla.get('usa_corte', False):
        condiciones.append('    !')

    if condiciones:
        for i, cond in enumerate(condiciones):
            separador = ',' if i < len(condiciones) - 1 else '.'
            lineas.append(cond + separador)
    else:
        lineas.append('    true.')

    return lineas


def regenerar_base_conocimiento():
    """
    Lee knowledge_store.json, genera knowledge_base.pl y recarga la instancia de Prolog.
    Retorna True si tuvo exito, False si hubo un error.
    """
    try:
        store = _cargar_store()
    except Exception as e:
        logger.error("Error al leer knowledge_store.json: %s", e)
        return False

    lineas = []

    lineas += [
        '% knowledge_base.pl',
        '% Generado automaticamente por kb_generator.py desde knowledge_store.json.',
        '% Para modificar la base de conocimiento usa la interfaz de administracion.',
        '',
    ]

    # Sintomas
    lineas += [
        '% =============================================================================',
        f"% SECCION 1: SINTOMAS DISPONIBLES ({len(store['sintomas'])} sintomas)",
        '% =============================================================================',
        '',
    ]
    for s in store['sintomas']:
        lineas.append(f"sintoma({s['nombre']}).")
    lineas.append('')

    # Fallas
    lineas += [
        '% =============================================================================',
        f"% SECCION 2: FALLAS DIAGNOSTICABLES ({len(store['fallas'])} fallas)",
        '% =============================================================================',
        '',
    ]
    for f in store['fallas']:
        lineas.append(f"falla({f['nombre']}).")
    lineas.append('')

    # Recomendaciones
    lineas += [
        '% =============================================================================',
        f"% SECCION 3: RECOMENDACIONES ({len(store['recomendaciones'])} recomendaciones)",
        '% =============================================================================',
        '',
    ]
    for r in store['recomendaciones']:
        texto = _escapar_texto_prolog(r['texto'])
        lineas.append(f"recomendacion({r['falla']},")
        lineas.append(f"    '{texto}').")
    lineas.append('')

    # Reglas
    lineas += [
        '% =============================================================================',
        f"% SECCION 4: REGLAS DE INFERENCIA ({len(store['reglas'])} reglas)",
        '% Usamos member/2 para verificar pertenencia en la lista de sintomas.',
        '% Usamos cortes (!) para evitar backtracking cuando la causa es clara.',
        '% =============================================================================',
        '',
    ]
    for regla in store['reglas']:
        lineas += _generar_regla(regla)
        lineas.append('')

    # Predicados utilitarios (siempre iguales)
    lineas += [
        '% =============================================================================',
        '% SECCION 5: PREDICADOS UTILITARIOS',
        '% =============================================================================',
        '',
        '% listar_sintomas(-Sintomas)',
        '% Obtiene la lista de todos los sintomas disponibles en la base de conocimiento.',
        'listar_sintomas(Sintomas) :-',
        '    findall(S, sintoma(S), Sintomas).',
        '',
        '% obtener_diagnosticos(+Sintomas, -Diagnosticos)',
        '% Dado una lista de sintomas, obtiene todas las fallas diagnosticadas sin duplicados.',
        'obtener_diagnosticos(Sintomas, Diagnosticos) :-',
        '    findall(F, diagnostico(Sintomas, F), DiagnosticosDups),',
        '    list_to_set(DiagnosticosDups, Diagnosticos).',
        '',
    ]

    try:
        RUTA_PL.write_text('\n'.join(lineas), encoding='utf-8')
        logger.info("knowledge_base.pl regenerado con %d sintomas, %d fallas, %d reglas",
                    len(store['sintomas']), len(store['fallas']), len(store['reglas']))
    except Exception as e:
        logger.error("Error al escribir knowledge_base.pl: %s", e)
        return False

    # Recargamos el motor de inferencia
    import prolog_bridge
    prolog_bridge.recargar()
    return True
