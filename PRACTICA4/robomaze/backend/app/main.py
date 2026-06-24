"""
Punto de entrada de la aplicacion FastAPI para RoboMaze.
Configura CORS, registra los routers y define el endpoint de estado.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.maze_router import router as maze_router
from app.routers.search_router import router as search_router

app = FastAPI(
    title="RoboMaze API",
    description="API REST para busqueda de rutas en laberintos usando BFS y DFS.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(maze_router)
app.include_router(search_router)


@app.get("/")
def root():
    """Endpoint raiz que retorna el estado de la API."""
    return {
        "status": "ok",
        "app": "RoboMaze API",
        "version": "1.0.0",
        "docs": "/docs",
    }
