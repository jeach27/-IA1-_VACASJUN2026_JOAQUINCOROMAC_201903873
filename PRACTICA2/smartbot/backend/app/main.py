import logging
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.config import settings
from app.database import Base, engine, obtener_sesion, SessionLocal
from app.models import UsuarioAdmin
from app.auth import verificar_password, crear_token, hashear_password
from app.schemas import LoginRequest, TokenResponse
from app.routers import categorias, preguntas, consultas, configuracion, estadisticas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)


def seed_admin():
    # Garantizamos que el usuario administrador preconfigurado exista con la contrasena correcta
    sesion = SessionLocal()
    try:
        admin = sesion.query(UsuarioAdmin).filter(UsuarioAdmin.username == "IA1-User").first()
        hash_correcto = hashear_password("IA1-password@_new")
        if not admin:
            sesion.add(UsuarioAdmin(username="IA1-User", password_hash=hash_correcto))
            sesion.commit()
            logger.info("Usuario administrador creado")
        else:
            admin.password_hash = hash_correcto
            sesion.commit()
    finally:
        sesion.close()


seed_admin()

app = FastAPI(title="SmartBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categorias.router)
app.include_router(preguntas.router)
app.include_router(consultas.router)
app.include_router(configuracion.router)
app.include_router(estadisticas.router)


@app.post("/auth/login", response_model=TokenResponse)
def login(datos: LoginRequest, sesion: Session = Depends(obtener_sesion)):
    # Verificamos las credenciales del administrador y generamos el token JWT
    usuario = sesion.query(UsuarioAdmin).filter(UsuarioAdmin.username == datos.username).first()
    if not usuario or not verificar_password(datos.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contrasena incorrectos",
        )
    token = crear_token(
        datos={"sub": usuario.username},
        expiracion=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return TokenResponse(access_token=token)


@app.get("/health")
def health():
    return {"estado": "ok"}


try:
    app.mount("/", StaticFiles(directory="/admin", html=True), name="admin")
except Exception:
    logger.warning("Panel administrativo no encontrado en /admin")
