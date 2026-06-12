import difflib
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import obtener_sesion
from app.models import Configuracion, Consulta, Pregunta, UsuarioAdmin
from app.schemas import ConsultaRequest, ConsultaRespuestaBot, ConsultaRespuesta
from app.auth import obtener_usuario_actual

router = APIRouter(tags=["consultas"])

UMBRAL_SIMILITUD = 0.45


def buscar_respuesta(texto: str, sesion: Session):
    # Buscamos la pregunta activa cuyo texto sea mas similar al del usuario
    preguntas = sesion.query(Pregunta).filter(Pregunta.activa == True).all()
    if not preguntas:
        return None

    texto_lower = texto.lower()
    mejor_ratio = 0.0
    mejor_pregunta = None

    for pregunta in preguntas:
        ratio = difflib.SequenceMatcher(None, texto_lower, pregunta.texto.lower()).ratio()
        if ratio > mejor_ratio:
            mejor_ratio = ratio
            mejor_pregunta = pregunta

    if mejor_ratio >= UMBRAL_SIMILITUD:
        return mejor_pregunta
    return None


@router.post("/consultar", response_model=ConsultaRespuestaBot)
def consultar(datos: ConsultaRequest, sesion: Session = Depends(obtener_sesion)):
    # Obtenemos el mensaje de no encontrado desde la configuracion del sistema
    config_no_encontrado = (
        sesion.query(Configuracion)
        .filter(Configuracion.clave == "mensaje_no_encontrado")
        .first()
    )
    mensaje_no_encontrado = (
        config_no_encontrado.valor
        if config_no_encontrado and config_no_encontrado.valor
        else "Lo siento, no encontre una respuesta para tu consulta."
    )

    pregunta_encontrada = buscar_respuesta(datos.texto, sesion)

    if pregunta_encontrada:
        respuesta_texto = pregunta_encontrada.respuesta
        encontrada = True
        pregunta_id = pregunta_encontrada.id
    else:
        respuesta_texto = mensaje_no_encontrado
        encontrada = False
        pregunta_id = None

    # Registramos la consulta en el historial
    registro = Consulta(
        telegram_user=datos.telegram_user,
        telegram_user_id=datos.telegram_user_id,
        texto_consulta=datos.texto,
        texto_respuesta=respuesta_texto,
        pregunta_id=pregunta_id,
        encontrada=encontrada,
    )
    sesion.add(registro)
    sesion.commit()

    return ConsultaRespuestaBot(
        respuesta=respuesta_texto,
        encontrada=encontrada,
        pregunta_id=pregunta_id,
    )


@router.get("/consultas", response_model=list[ConsultaRespuesta])
def listar_consultas(
    limite: int = 100,
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    return (
        sesion.query(Consulta)
        .order_by(Consulta.consultado_en.desc())
        .limit(limite)
        .all()
    )
