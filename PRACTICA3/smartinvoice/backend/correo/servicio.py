import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, Optional

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


def enviar_correo(
    destinatario: str,
    asunto: str,
    cuerpo: str,
    adjunto: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Envia un correo electronico con smtplib usando STARTTLS.
    Retorna un dict con exito (bool) y mensaje (str).
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        return {
            "exito": False,
            "mensaje": "Credenciales SMTP no configuradas. Revisar variables de entorno SMTP_USER y SMTP_PASSWORD.",
        }

    mensaje = MIMEMultipart()
    mensaje["From"] = SMTP_USER
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

    if adjunto and os.path.exists(adjunto):
        nombre_archivo = os.path.basename(adjunto)
        with open(adjunto, "rb") as f:
            parte = MIMEBase("application", "octet-stream")
            parte.set_payload(f.read())
        encoders.encode_base64(parte)
        parte.add_header("Content-Disposition", f'attachment; filename="{nombre_archivo}"')
        mensaje.attach(parte)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.ehlo()
            servidor.login(SMTP_USER, SMTP_PASSWORD)
            servidor.sendmail(SMTP_USER, destinatario, mensaje.as_string())

        return {
            "exito": True,
            "mensaje": f"Correo enviado exitosamente a {destinatario}",
        }

    except smtplib.SMTPAuthenticationError:
        return {
            "exito": False,
            "mensaje": "Error de autenticacion SMTP. Verificar SMTP_USER y SMTP_PASSWORD.",
        }
    except smtplib.SMTPException as e:
        return {
            "exito": False,
            "mensaje": f"Error SMTP al enviar correo: {str(e)}",
        }
    except Exception as e:
        return {
            "exito": False,
            "mensaje": f"Error inesperado al enviar correo: {str(e)}",
        }
