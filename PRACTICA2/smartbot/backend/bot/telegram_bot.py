import logging
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
API_URL = os.environ.get("API_URL", "http://backend:8000")


def consultar_api(texto: str, telegram_user: str, telegram_user_id: int) -> str:
    # Enviamos la consulta del usuario al endpoint de la API y retornamos la respuesta
    try:
        respuesta = requests.post(
            f"{API_URL}/consultar",
            json={
                "texto": texto,
                "telegram_user": telegram_user,
                "telegram_user_id": telegram_user_id,
            },
            timeout=10,
        )
        respuesta.raise_for_status()
        datos = respuesta.json()
        return datos.get("respuesta", "No se pudo obtener una respuesta.")
    except requests.RequestException as error:
        logger.error("Error al consultar la API: %s", error)
        return "Ocurrio un error al procesar tu consulta. Por favor intenta mas tarde."


async def comando_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    nombre = update.effective_user.first_name or "usuario"
    await update.message.reply_text(
        f"Hola {nombre}! Soy SmartBot, tu asistente de preguntas frecuentes.\n"
        "Escribe tu pregunta y te respondere con la informacion disponible.\n\n"
        "Comandos disponibles:\n"
        "/start - Mensaje de bienvenida\n"
        "/ayuda - Muestra esta informacion"
    )


async def comando_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Puedes hacerme preguntas sobre horarios, tramites, tecnologia, pagos y temas generales.\n"
        "Simplemente escribe tu pregunta y la buscamos en nuestra base de conocimiento."
    )


async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Procesamos el mensaje del usuario y respondemos con la informacion de la API
    usuario = update.effective_user
    texto = update.message.text.strip()

    if not texto:
        return

    logger.info("Consulta de %s (id=%s): %s", usuario.username or usuario.first_name, usuario.id, texto)

    respuesta = consultar_api(
        texto=texto,
        telegram_user=usuario.username or usuario.first_name,
        telegram_user_id=usuario.id,
    )
    await update.message.reply_text(respuesta)


def main() -> None:
    aplicacion = Application.builder().token(TELEGRAM_TOKEN).build()

    aplicacion.add_handler(CommandHandler("start", comando_inicio))
    aplicacion.add_handler(CommandHandler("ayuda", comando_ayuda))
    aplicacion.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    logger.info("SmartBot iniciado. Escuchando mensajes...")
    aplicacion.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
