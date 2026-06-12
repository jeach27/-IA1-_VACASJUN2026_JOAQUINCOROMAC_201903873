# app.py
# Entrada principal del servidor Flask de Doctor Byte.
# Exponemos tres endpoints REST y servimos el frontend estatico desde la raiz.

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


# --- Endpoints de la API ---

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
    La notificacion de Telegram se envia automaticamente si TELEGRAM_TOKEN y
    TELEGRAM_CHAT_ID estan configurados como variables de entorno.
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

    # Enviamos la notificacion a Telegram; token y chat_id vienen de variables de entorno
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


# --- Servicio de archivos estaticos del frontend ---

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, 'css'), filename)


@app.route('/js/<path:filename>')
def js_files(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, 'js'), filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
