from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import obtener_sesion
from app.models import Categoria, Consulta, Pregunta, UsuarioAdmin
from app.schemas import EstadisticasRespuesta
from app.auth import obtener_usuario_actual

router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])


@router.get("", response_model=EstadisticasRespuesta)
def obtener_estadisticas(
    sesion: Session = Depends(obtener_sesion),
    _: UsuarioAdmin = Depends(obtener_usuario_actual),
):
    total_consultas = sesion.query(func.count(Consulta.id)).scalar()
    consultas_encontradas = sesion.query(func.count(Consulta.id)).filter(Consulta.encontrada == True).scalar()
    consultas_no_encontradas = total_consultas - consultas_encontradas
    total_usuarios_unicos = sesion.query(func.count(func.distinct(Consulta.telegram_user_id))).scalar()
    total_preguntas = sesion.query(func.count(Pregunta.id)).scalar()
    total_categorias = sesion.query(func.count(Categoria.id)).scalar()

    # Consultas agrupadas por categoria
    consultas_por_categoria = (
        sesion.query(Categoria.nombre, func.count(Consulta.id).label("total"))
        .join(Pregunta, Pregunta.categoria_id == Categoria.id)
        .join(Consulta, Consulta.pregunta_id == Pregunta.id)
        .group_by(Categoria.nombre)
        .order_by(func.count(Consulta.id).desc())
        .all()
    )

    # Preguntas mas consultadas (top 10)
    preguntas_mas_consultadas = (
        sesion.query(Pregunta.texto, func.count(Consulta.id).label("total"))
        .join(Consulta, Consulta.pregunta_id == Pregunta.id)
        .group_by(Pregunta.id, Pregunta.texto)
        .order_by(func.count(Consulta.id).desc())
        .limit(10)
        .all()
    )

    return EstadisticasRespuesta(
        total_consultas=total_consultas or 0,
        consultas_encontradas=consultas_encontradas or 0,
        consultas_no_encontradas=consultas_no_encontradas or 0,
        total_usuarios_unicos=total_usuarios_unicos or 0,
        total_preguntas=total_preguntas or 0,
        total_categorias=total_categorias or 0,
        consultas_por_categoria=[{"categoria": r[0], "total": r[1]} for r in consultas_por_categoria],
        preguntas_mas_consultadas=[{"pregunta": r[0], "total": r[1]} for r in preguntas_mas_consultadas],
    )
