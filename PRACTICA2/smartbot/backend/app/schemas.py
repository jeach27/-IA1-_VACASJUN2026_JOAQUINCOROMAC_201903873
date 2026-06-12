from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# --- Auth ---

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Categoria ---

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class CategoriaCrear(CategoriaBase):
    pass


class CategoriaActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class CategoriaRespuesta(CategoriaBase):
    id: int
    creado_en: datetime

    class Config:
        from_attributes = True


# --- Pregunta ---

class PreguntaBase(BaseModel):
    texto: str
    respuesta: str
    categoria_id: Optional[int] = None
    activa: bool = True


class PreguntaCrear(PreguntaBase):
    pass


class PreguntaActualizar(BaseModel):
    texto: Optional[str] = None
    respuesta: Optional[str] = None
    categoria_id: Optional[int] = None
    activa: Optional[bool] = None


class PreguntaRespuesta(PreguntaBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime
    categoria: Optional[CategoriaRespuesta] = None

    class Config:
        from_attributes = True


# --- Consulta ---

class ConsultaRequest(BaseModel):
    texto: str
    telegram_user: Optional[str] = None
    telegram_user_id: Optional[int] = None


class ConsultaRespuestaBot(BaseModel):
    respuesta: str
    encontrada: bool
    pregunta_id: Optional[int] = None


class ConsultaRespuesta(BaseModel):
    id: int
    telegram_user: Optional[str]
    telegram_user_id: Optional[int]
    texto_consulta: str
    texto_respuesta: Optional[str]
    encontrada: bool
    consultado_en: datetime

    class Config:
        from_attributes = True


# --- Configuracion ---

class ConfiguracionActualizar(BaseModel):
    valor: str


class ConfiguracionRespuesta(BaseModel):
    id: int
    clave: str
    valor: Optional[str]
    descripcion: Optional[str]
    actualizado_en: datetime

    class Config:
        from_attributes = True


# --- Estadisticas ---

class EstadisticasRespuesta(BaseModel):
    total_consultas: int
    consultas_encontradas: int
    consultas_no_encontradas: int
    total_usuarios_unicos: int
    total_preguntas: int
    total_categorias: int
    consultas_por_categoria: list
    preguntas_mas_consultadas: list
