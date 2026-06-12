# telegram_bot.py
# Envio de notificaciones de diagnostico al bot de Telegram.
# Usamos urllib de la libreria estandar de Python para hacer la peticion HTTP,
# sin dependencias externas especificas de Telegram.
# El token y el chat_id se leen siempre desde variables de entorno.

import os
import json
import logging
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/sendMessage'


def _formatear_mensaje(diagnosticos):
    """Construye el texto del mensaje a enviar al chat de Telegram."""
    if not diagnosticos:
        return 'Doctor Byte: No se encontraron diagnosticos para los sintomas indicados.'

    lineas = ['*Doctor Byte - Resultado del Diagnostico*', '']
    for d in diagnosticos:
        falla_legible = d['falla'].replace('_', ' ').title()
        lineas.append(f"*Falla detectada:* {falla_legible}")
        lineas.append(f"*Recomendacion:* {d['recomendacion']}")
        lineas.append('')

    return '\n'.join(lineas)


def enviar_diagnostico(diagnosticos):
    """
    Envia los resultados del diagnostico al chat de Telegram configurado.
    Lee TELEGRAM_TOKEN y TELEGRAM_CHAT_ID desde variables de entorno.
    Si alguna de las dos no esta configurada, omite el envio y registra una advertencia.
    """
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        logger.warning(
            "TELEGRAM_TOKEN o TELEGRAM_CHAT_ID no configurados, se omite el envio"
        )
        return

    mensaje = _formatear_mensaje(diagnosticos)
    url = TELEGRAM_API_URL.format(token=token)

    cuerpo = json.dumps({
        'chat_id': chat_id,
        'text': mensaje,
        'parse_mode': 'Markdown'
    }).encode('utf-8')

    peticion = urllib.request.Request(
        url,
        data=cuerpo,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(peticion, timeout=10) as respuesta:
            logger.info(
                "Notificacion enviada a Telegram, estado HTTP: %s", respuesta.status
            )
    except urllib.error.URLError as error:
        logger.error("Error al enviar notificacion a Telegram: %s", error)
