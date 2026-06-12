# [IA1] VACASJUN2026 - Joaquin Coromac - 201903873

Sistema de Rutas entre Ciudades de Guatemala
Practica 1 - Inteligencia Artificial 1
Universidad San Carlos de Guatemala

## Descripcion

Sistema que utiliza SWI-Prolog como motor logico para encontrar rutas entre ciudades, con un backend Python (FastAPI) y un frontend web.

## Tecnologias

- SWI-Prolog (logica de busqueda y optimizacion)
- Python 3.11 + FastAPI + PySwip (backend REST)
- HTML / CSS / JavaScript puro (frontend)

## Instalacion rapida

```bash
# 1. Instalar SWI-Prolog desde https://www.swi-prolog.org
# 2. Crear entorno virtual e instalar dependencias
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt

# 3. Iniciar el backend
uvicorn main:app --reload

# 4. Abrir frontend/index.html en el navegador
```

## Documentacion

- [Manual de Usuario](docs/manual_usuario.md)
- [Manual Tecnico](docs/manual_tecnico.md)
