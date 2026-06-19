from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegistroRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    rol: Optional[str] = "usuario"


class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: str
    rol: str
    activo: bool

    model_config = {"from_attributes": True}
