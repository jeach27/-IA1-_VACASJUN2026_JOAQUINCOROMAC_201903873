# app.py
# Entrada principal del servidor Flask de Doctor Byte.
# Exponemos los endpoints REST del sistema experto y del panel de administracion,
# y servimos el frontend estatico desde la raiz.

import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from prolog_bridge import consultar_sintomas, consultar_diagnostico
from history import guardar_diagnostico, obtener_historial
from telegram_bot import enviar_diagnostico

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

app = Flask(__name__)
CORS(app)


# =============================================================================
# ENDPOINTS DEL SISTEMA EXPERTO
# =============================================================================

@app.route('/sintomas', methods=['GET'])
def get_sintomas():
    """Devuelve la lista de todos los sintomas disponibles en la base de conocimiento."""
    sintomas = consultar_sintomas()
    return jsonify({'sintomas': sintomas})


@app.route('/diagnostico', methods=['POST'])
def post_diagnostico():
    """
    Recibe una lista de sintomas y retorna los diagnosticos con recomendaciones.
    Cuerpo esperado: { "sintomas": [...] }
    Guarda el resultado en el historial y notifica via Telegram si esta configurado.
    """
    datos = request.get_json()

    if not datos or 'sintomas' not in datos:
        return jsonify({'error': 'Se requiere el campo sintomas en el cuerpo de la solicitud'}), 400

    sintomas = datos['sintomas']

    if not isinstance(sintomas, list) or len(sintomas) == 0:
        return jsonify({'error': 'El campo sintomas debe ser una lista con al menos un elemento'}), 400

    logger.info("Solicitud de diagnostico recibida con sintomas: %s", sintomas)

    diagnosticos = consultar_diagnostico(sintomas)
    registro = guardar_diagnostico(sintomas, diagnosticos)
    enviar_diagnostico(diagnosticos)

    return jsonify({
        'id': registro['id'],
        'fecha': registro['fecha'],
        'sintomas': sintomas,
        'diagnosticos': diagnosticos
    })


@app.route('/historial', methods=['GET'])
def get_historial():
    """Devuelve el historial de todos los diagnosticos realizados, del mas reciente al mas antiguo."""
    historial = obtener_historial()
    return jsonify({'historial': historial})


# =============================================================================
# ENDPOINTS DE ADMINISTRACION - SINTOMAS
# =============================================================================

@app.route('/admin/sintomas', methods=['GET'])
def admin_get_sintomas():
    from admin_manager import obtener_sintomas
    return jsonify({'sintomas': obtener_sintomas()})


@app.route('/admin/sintomas', methods=['POST'])
def admin_crear_sintoma():
    from admin_manager import agregar_sintoma
    datos = request.get_json() or {}
    try:
        agregar_sintoma(datos.get('nombre', ''), datos.get('etiqueta', ''))
        return jsonify({'ok': True}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/admin/sintomas/<nombre>', methods=['PUT'])
def admin_actualizar_sintoma(nombre):
    from admin_manager import actualizar_sintoma
    datos = request.get_json() or {}
    try:
        actualizar_sintoma(nombre, datos.get('nombre', nombre), datos.get('etiqueta', ''))
        return jsonify({'ok': True})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/admin/sintomas/<nombre>', methods=['DELETE'])
def admin_eliminar_sintoma(nombre):
    from admin_manager import eliminar_sintoma
    eliminar_sintoma(nombre)
    return jsonify({'ok': True})


# =============================================================================
# ENDPOINTS DE ADMINISTRACION - FALLAS
# =============================================================================

@app.route('/admin/fallas', methods=['GET'])
def admin_get_fallas():
    from admin_manager import obtener_fallas
    return jsonify({'fallas': obtener_fallas()})


@app.route('/admin/fallas', methods=['POST'])
def admin_crear_falla():
    from admin_manager import agregar_falla
    datos = request.get_json() or {}
    try:
        agregar_falla(datos.get('nombre', ''), datos.get('etiqueta', ''))
        return jsonify({'ok': True}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/admin/fallas/<nombre>', methods=['PUT'])
def admin_actualizar_falla(nombre):
    from admin_manager import actualizar_falla
    datos = request.get_json() or {}
    try:
        actualizar_falla(nombre, datos.get('nombre', nombre), datos.get('etiqueta', ''))
        return jsonify({'ok': True})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/admin/fallas/<nombre>', methods=['DELETE'])
def admin_eliminar_falla(nombre):
    from admin_manager import eliminar_falla
    eliminar_falla(nombre)
    return jsonify({'ok': True})


# =============================================================================
# ENDPOINTS DE ADMINISTRACION - RECOMENDACIONES
# =============================================================================

@app.route('/admin/recomendaciones', methods=['GET'])
def admin_get_recomendaciones():
    from admin_manager import obtener_recomendaciones
    return jsonify({'recomendaciones': obtener_recomendaciones()})


@app.route('/admin/recomendaciones/<falla>', methods=['PUT'])
def admin_actualizar_recomendacion(falla):
    from admin_manager import actualizar_recomendacion
    datos = request.get_json() or {}
    try:
        actualizar_recomendacion(falla, datos.get('texto', ''))
        return jsonify({'ok': True})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/admin/recomendaciones/<falla>', methods=['DELETE'])
def admin_eliminar_recomendacion(falla):
    from admin_manager import eliminar_recomendacion
    eliminar_recomendacion(falla)
    return jsonify({'ok': True})


# =============================================================================
# ENDPOINTS DE ADMINISTRACION - REGLAS
# =============================================================================

@app.route('/admin/reglas', methods=['GET'])
def admin_get_reglas():
    from admin_manager import obtener_reglas
    return jsonify({'reglas': obtener_reglas()})


@app.route('/admin/reglas', methods=['POST'])
def admin_crear_regla():
    from admin_manager import agregar_regla
    datos = request.get_json() or {}
    try:
        nueva = agregar_regla(
            datos.get('falla', ''),
            datos.get('sintomas_requeridos', []),
            datos.get('sintomas_negados', []),
            datos.get('usa_corte', True),
            datos.get('descripcion', ''),
        )
        return jsonify({'ok': True, 'regla': nueva}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/admin/reglas/<id_regla>', methods=['PUT'])
def admin_actualizar_regla(id_regla):
    from admin_manager import actualizar_regla
    datos = request.get_json() or {}
    try:
        regla = actualizar_regla(
            id_regla,
            datos.get('falla', ''),
            datos.get('sintomas_requeridos', []),
            datos.get('sintomas_negados', []),
            datos.get('usa_corte', True),
            datos.get('descripcion', ''),
        )
        return jsonify({'ok': True, 'regla': regla})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/admin/reglas/<id_regla>', methods=['DELETE'])
def admin_eliminar_regla(id_regla):
    from admin_manager import eliminar_regla
    try:
        eliminar_regla(id_regla)
        return jsonify({'ok': True})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


# =============================================================================
# ENDPOINTS DE ADMINISTRACION - ASOCIACIONES
# =============================================================================

@app.route('/admin/asociaciones', methods=['GET'])
def admin_get_asociaciones():
    from admin_manager import obtener_asociaciones
    return jsonify({'asociaciones': obtener_asociaciones()})


# =============================================================================
# ENDPOINTS DE ADMINISTRACION - CONFIGURACION DEL BOT
# =============================================================================

@app.route('/admin/configuracion', methods=['GET'])
def admin_get_configuracion():
    from admin_manager import obtener_config_bot
    return jsonify(obtener_config_bot())


@app.route('/admin/configuracion', methods=['PUT'])
def admin_actualizar_configuracion():
    from admin_manager import actualizar_config_bot
    datos = request.get_json() or {}
    config = actualizar_config_bot(
        datos.get('chat_id', ''),
        datos.get('habilitado', True),
        datos.get('mensajes', {}),
    )
    return jsonify(config)


# =============================================================================
# SERVICIO DE ARCHIVOS ESTATICOS
# =============================================================================

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/admin')
def admin_panel():
    return send_from_directory(FRONTEND_DIR, 'admin.html')


@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, 'css'), filename)


@app.route('/js/<path:filename>')
def js_files(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, 'js'), filename)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == '__main__':
    from telegram_bot import iniciar_bot
    iniciar_bot()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
