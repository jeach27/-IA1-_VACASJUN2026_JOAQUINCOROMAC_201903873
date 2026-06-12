from datetime import datetime
from sqlalchemy import Boolean, BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    creado_en = Column(DateTime, default=datetime.now)

    preguntas = relationship("Pregunta", back_populates="categoria")


class Pregunta(Base):
    __tablename__ = "pregunta"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text, nullable=False)
    respuesta = Column(Text, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=True)
    activa = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.now)
    actualizado_en = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    categoria = relationship("Categoria", back_populates="preguntas")
    consultas = relationship("Consulta", back_populates="pregunta")


class UsuarioAdmin(Base):
    __tablename__ = "usuario_admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    creado_en = Column(DateTime, default=datetime.now)


class Consulta(Base):
    __tablename__ = "consulta"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user = Column(String(100))
    telegram_user_id = Column(BigInteger)
    texto_consulta = Column(Text, nullable=False)
    texto_respuesta = Column(Text)
    pregunta_id = Column(Integer, ForeignKey("pregunta.id"), nullable=True)
    encontrada = Column(Boolean, default=False)
    consultado_en = Column(DateTime, default=datetime.now)

    pregunta = relationship("Pregunta", back_populates="consultas")


class Configuracion(Base):
    __tablename__ = "configuracion"

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(100), unique=True, nullable=False)
    valor = Column(Text)
    descripcion = Column(Text)
    actualizado_en = Column(DateTime, default=datetime.now, onupdate=datetime.now)
