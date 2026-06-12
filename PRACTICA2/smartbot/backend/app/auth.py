from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import obtener_sesion
from app.models import UsuarioAdmin

contexto_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verificar_password(plano: str, hash_guardado: str) -> bool:
    return contexto_pwd.verify(plano, hash_guardado)


def hashear_password(password: str) -> str:
    return contexto_pwd.hash(password)


def crear_token(datos: dict, expiracion: Optional[timedelta] = None) -> str:
    payload = datos.copy()
    expira = datetime.utcnow() + (expiracion or timedelta(minutes=settings.access_token_expire_minutes))
    payload.update({"exp": expira})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    sesion: Session = Depends(obtener_sesion),
) -> UsuarioAdmin:
    excepcion = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise excepcion
    except JWTError:
        raise excepcion

    usuario = sesion.query(UsuarioAdmin).filter(UsuarioAdmin.username == username).first()
    if usuario is None:
        raise excepcion
    return usuario
