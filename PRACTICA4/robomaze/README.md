# RoboMaze

Sistema de busqueda de rutas en laberintos virtuales mediante los algoritmos BFS y DFS.

Desarrollado para la Practica 4 de Inteligencia Artificial 1 - Universidad de San Carlos de Guatemala.

---

## Descripcion

RoboMaze permite representar laberintos como cuadriculas bidimensionales y encontrar rutas desde una posicion inicial hasta una posicion objetivo usando Breadth-First Search (BFS) y Depth-First Search (DFS). El sistema mide nodos explorados y tiempo de ejecucion para cada algoritmo.

---

## Tecnologias

- Backend: Python 3.11, FastAPI, Uvicorn
- Frontend: HTML, CSS y JavaScript vanilla
- Control de versiones: Git y GitHub

---

## Estructura del proyecto

```
robomaze/
    backend/
        app/
            algorithms/    # BFS y DFS implementados manualmente
            models/        # Clases Maze y SearchResult
            routers/       # Endpoints de la API REST
            services/      # Logica de negocio
            main.py        # Punto de entrada de FastAPI
        requirements.txt
    frontend/
        index.html
        css/styles.css
        js/api.js, maze.js, ui.js
    docs/
        manual_tecnico.md
        manual_usuario.md
```

---

## Instalacion y ejecucion

### Backend

1. Entrar a la carpeta backend:
   ```
   cd robomaze/backend
   ```

2. Crear y activar entorno virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Ejecutar el servidor:
   ```
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend

Abrir el archivo `frontend/index.html` directamente en el navegador, o servir con cualquier servidor estatico.

---

## Documentacion

- [Manual Tecnico](docs/manual_tecnico.md)
- [Manual de Usuario](docs/manual_usuario.md)

---

## Autor

Joaquin Emmanuel Aldair Coromac Huezo - 201903873
