from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
from auth.schemas import LoginRequest, TokenResponse, RegistroRequest, UsuarioResponse
from auth.utils import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contrasena incorrectos",
        )
    if not user.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/registro", response_model=UsuarioResponse)
def registro(request: RegistroRequest, db: Session = Depends(get_db)):
    if db.query(models.Usuario).filter(models.Usuario.username == request.username).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    if db.query(models.Usuario).filter(models.Usuario.email == request.email).first():
        raise HTTPException(status_code=400, detail="El correo ya esta registrado")

    nuevo_usuario = models.Usuario(
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
        rol=request.rol or "usuario",
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: models.Usuario = Depends(get_current_user)):
    return current_user
