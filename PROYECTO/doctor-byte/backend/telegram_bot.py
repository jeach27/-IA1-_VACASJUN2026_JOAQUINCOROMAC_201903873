# telegram_bot.py
# Notificaciones y bot interactivo de Telegram para Doctor Byte.
# Enviamos diagnosticos al chat configurado y procesamos comandos de usuarios.
# El token del bot se lee siempre desde la variable de entorno TELEGRAM_TOKEN.
# El chat_id y la configuracion adicional se leen desde data/bot_config.json.

import os
import json
import logging
import threading
import time
import urllib.request
import urllib.error
from pathlib import Path

logger = logging.getLogger(__name__)

RUTA_BOT_CONFIG = Path(__file__).parent / 'data' / 'bot_config.json'
URL_BACKEND = 'http://localhost:5000'
_TELEGRAM_API = 'https://api.telegram.org/bot{token}/{metodo}'


# =============================================================================
# UTILIDADES INTERNAS
# =============================================================================

def _cargar_config():
    """Carga la configuracion del bot desde bot_config.json."""
    if RUTA_BOT_CONFIG.exists():
        try:
            with open(RUTA_BOT_CONFIG, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'chat_id': '', 'habilitado': True, 'mensajes': {}}


def _llamar_api_telegram(token, metodo, datos=None):
    """Realiza una llamada POST a la API de Telegram y retorna el JSON de respuesta."""
    url = _TELEGRAM_API.format(token=token, metodo=metodo)
    cuerpo = json.dumps(datos or {}).encode('utf-8')
    peticion = urllib.request.Request(
        url, data=cuerpo,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(peticion, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.URLError as e:
        logger.error("Error en llamada a Telegram API (%s): %s", metodo, e)
        return None


def _enviar_mensaje(token, chat_id, texto):
    """Envia un mensaje de texto en formato Markdown a un chat de Telegram."""
    _llamar_api_telegram(token, 'sendMessage', {
        'chat_id': chat_id,
        'text': texto,
        'parse_mode': 'Markdown',
    })


def _obtener_actualizaciones(token, offset):
    """
    Obtiene actualizaciones pendientes con long polling (25 s de espera en el servidor).
    Retorna lista de updates o lista vacia si hubo error o timeout sin novedades.
    """
    url = (
        f"https://api.telegram.org/bot{token}/getUpdates"
        f"?offset={offset}&timeout=25&allowed_updates=%5B%22message%22%5D"
    )
    try:
        peticion = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(peticion, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('result', [])
    except Exception:
        return []


# =============================================================================
# LOGICA DE COMANDOS DEL BOT
# =============================================================================

def _consultar_sintomas():
    """Pide al endpoint /sintomas del backend la lista actualizada de sintomas."""
    try:
        with urllib.request.urlopen(f"{URL_BACKEND}/sintomas", timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('sintomas', [])
    except Exception as e:
        logger.error("Error al obtener sintomas del backend: %s", e)
        return []


def _consultar_diagnostico(sintomas):
    """Envia una lista de sintomas al endpoint /diagnostico y retorna los resultados."""
    cuerpo = json.dumps({'sintomas': sintomas}).encode('utf-8')
    peticion = urllib.request.Request(
        f"{URL_BACKEND}/diagnostico",
        data=cuerpo,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(peticion, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        logger.error("Error al consultar el backend: %s", e)
        return None


def _texto_bienvenida(config):
    return (
        config.get('mensajes', {}).get('bienvenida',
            'Bienvenido a Doctor Byte. Sistema experto de diagnostico de fallas en computadoras.')
        + '\n\n'
        '*Comandos disponibles:*\n'
        '/sintomas \\- Ver todos los sintomas disponibles\n'
        '/diagnosticar s1,s2,... \\- Obtener diagnostico\n'
        '/ayuda \\- Mostrar esta ayuda'
    )


def _procesar_update(token, update, config):
    """Procesa un update recibido de Telegram y responde al usuario."""
    if 'message' not in update:
        return
    msg = update['message']
    chat_id = str(msg['chat']['id'])
    texto = msg.get('text', '').strip()
    if not texto:
        return

    logger.info("Mensaje recibido del chat %s: %s", chat_id, texto[:60])

    if texto.startswith('/start'):
        _enviar_mensaje(token, chat_id, _texto_bienvenida(config))

    elif texto.startswith('/sintomas'):
        sintomas = _consultar_sintomas()
        if sintomas:
            lista = '\n'.join(f'- `{s}`' for s in sintomas)
            _enviar_mensaje(token, chat_id,
                f'*Sintomas disponibles ({len(sintomas)}):*\n{lista}\n\n'
                'Usa: `/diagnosticar s1,s2,...`'
            )
        else:
            _enviar_mensaje(token, chat_id,
                'No se pudo obtener la lista de sintomas. Verifica que el servidor este activo.')

    elif texto.startswith('/diagnosticar'):
        argumento = texto[len('/diagnosticar'):].strip()
        if not argumento:
            _enviar_mensaje(token, chat_id,
                'Uso: `/diagnosticar sintoma1,sintoma2,...`\n'
                'Ejemplo: `/diagnosticar pantalla_negra,no_enciende`'
            )
            return

        sintomas = [s.strip() for s in argumento.split(',') if s.strip()]
        resultado = _consultar_diagnostico(sintomas)

        if resultado is None:
            _enviar_mensaje(token, chat_id,
                'Error al conectar con el servidor de diagnostico. Intenta mas tarde.')
            return

        diagnosticos = resultado.get('diagnosticos', [])
        if not diagnosticos:
            msg_vacio = config.get('mensajes', {}).get(
                'sin_diagnostico',
                'No se encontraron fallas especificas para los sintomas indicados.'
            )
            _enviar_mensaje(token, chat_id, msg_vacio)
            return

        lineas = ['*Doctor Byte \\- Resultado del Diagnostico*', '']
        for d in diagnosticos:
            falla_legible = d['falla'].replace('_', ' ').title()
            lineas.append(f"*Falla:* {falla_legible}")
            lineas.append(f"*Recomendacion:* {d['recomendacion']}")
            lineas.append('')
        _enviar_mensaje(token, chat_id, '\n'.join(lineas))

    elif texto.startswith('/ayuda'):
        _enviar_mensaje(token, chat_id,
            '*Comandos de Doctor Byte:*\n'
            '/start \\- Mensaje de bienvenida\n'
            '/sintomas \\- Ver sintomas disponibles\n'
            '/diagnosticar s1,s2,... \\- Obtener diagnostico\n'
            '/ayuda \\- Mostrar esta ayuda'
        )

    else:
        _enviar_mensaje(token, chat_id,
            'Comando no reconocido. Usa /ayuda para ver los comandos disponibles.')


# =============================================================================
# HILO DE POLLING
# =============================================================================

def _hilo_polling():
    """
    Hilo de fondo que realiza long polling a la API de Telegram.
    Procesa cada mensaje recibido y llama al backend para obtener diagnosticos.
    """
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        logger.warning("TELEGRAM_TOKEN no configurado; el bot interactivo no iniciara")
        return

    logger.info("Bot interactivo de Telegram iniciado en modo polling")

    # Esperamos a que Flask este listo para recibir peticiones
    time.sleep(4)

    offset = 0
    while True:
        try:
            config = _cargar_config()
            updates = _obtener_actualizaciones(token, offset)
            for update in updates:
                _procesar_update(token, update, config)
                offset = update['update_id'] + 1
        except Exception as e:
            logger.error("Error en el hilo de polling: %s", e)
            time.sleep(5)


def iniciar_bot():
    """Inicia el hilo de polling en segundo plano. Debe llamarse una sola vez al arrancar."""
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        logger.warning("TELEGRAM_TOKEN no definido; el bot no se iniciara")
        return
    hilo = threading.Thread(target=_hilo_polling, daemon=True, name='telegram-polling')
    hilo.start()
    logger.info("Hilo del bot de Telegram iniciado")


# =============================================================================
# ENVIO DE NOTIFICACIONES (llamado desde el endpoint /diagnostico)
# =============================================================================

def _formatear_mensaje_notificacion(diagnosticos, config):
    """Construye el texto del mensaje de notificacion para el chat configurado."""
    if not diagnosticos:
        return config.get('mensajes', {}).get(
            'sin_diagnostico',
            'Doctor Byte: No se encontraron diagnosticos para los sintomas indicados.'
        )
    lineas = ['*Doctor Byte \\- Resultado del Diagnostico*', '']
    for d in diagnosticos:
        falla_legible = d['falla'].replace('_', ' ').title()
        lineas.append(f"*Falla detectada:* {falla_legible}")
        lineas.append(f"*Recomendacion:* {d['recomendacion']}")
        lineas.append('')
    return '\n'.join(lineas)


def enviar_diagnostico(diagnosticos):
    """
    Envia los resultados del diagnostico al chat de Telegram configurado.
    Lee TELEGRAM_TOKEN desde variables de entorno.
    Lee chat_id y estado habilitado desde data/bot_config.json.
    Si el bot esta deshabilitado o faltan datos, omite el envio sin lanzar excepciones.
    """
    config = _cargar_config()

    if not config.get('habilitado', True):
        logger.info("Bot deshabilitado en configuracion; se omite el envio")
        return

    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = config.get('chat_id') or os.environ.get('TELEGRAM_CHAT_ID', '')

    if not token or not chat_id:
        logger.warning("TELEGRAM_TOKEN o chat_id no configurados; se omite el envio")
        return

    mensaje = _formatear_mensaje_notificacion(diagnosticos, config)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    cuerpo = json.dumps({
        'chat_id': chat_id,
        'text': mensaje,
        'parse_mode': 'MarkdownV2',
    }).encode('utf-8')
    peticion = urllib.request.Request(
        url, data=cuerpo,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(peticion, timeout=10) as resp:
            logger.info("Notificacion enviada a Telegram, estado HTTP: %s", resp.status)
    except urllib.error.URLError as e:
        logger.error("Error al enviar notificacion a Telegram: %s", e)
