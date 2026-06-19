import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

from database import engine, SessionLocal, Base
import models
from auth.utils import hash_password
from auth.router import router as auth_router
from proveedores.router import router as proveedores_router
from facturas.router import router as facturas_router
from bitacora.router import router as bitacora_router
from reportes.router import router as reportes_router

app = FastAPI(
    title="SmartInvoice API",
    description="API REST para el sistema de procesamiento inteligente de facturas",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(proveedores_router)
app.include_router(facturas_router)
app.include_router(bitacora_router)
app.include_router(reportes_router)


def crear_tablas_y_admin():
    """Crea las tablas en la base de datos y el usuario admin inicial si no existe."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = db.query(models.Usuario).filter(models.Usuario.username == "admin").first()
        if not admin:
            admin = models.Usuario(
                username="admin",
                email="admin@smartinvoice.local",
                password_hash=hash_password("admin123"),
                rol="admin",
                activo=True,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def startup():
    crear_tablas_y_admin()


@app.get("/")
def root():
    return {"mensaje": "SmartInvoice API funcionando", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "conectada"
    except Exception:
        db_status = "desconectada"

    return {"estado": "activo", "base_de_datos": db_status}
