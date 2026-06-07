"""
Punto de entrada de la aplicacion FastAPI.
Registra el router y configura CORS para que el frontend pueda consumir la API.
"""

import sys
import os

# Permite importar modulos del backend sin instalar el paquete
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.rutas import router

app = FastAPI(
    title="Sistema de Rutas entre Ciudades",
    description="API REST que consulta SWI-Prolog para encontrar rutas optimas.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def raiz():
    return {"mensaje": "Sistema de Rutas - API activa. Consulte /docs para la documentacion."}
