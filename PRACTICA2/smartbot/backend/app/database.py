from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def obtener_sesion():
    # Generamos una sesion de base de datos por cada request y la cerramos al terminar
    sesion = SessionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
