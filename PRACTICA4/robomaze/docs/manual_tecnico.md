# Manual Tecnico - RoboMaze

## Descripcion general del sistema

RoboMaze es un sistema de busqueda de rutas en laberintos virtuales. Permite representar un laberinto como una cuadricula bidimensional donde cada celda puede ser libre u obstaculo, y ejecutar los algoritmos Breadth-First Search (BFS) y Depth-First Search (DFS) para encontrar rutas entre una posicion inicial y una posicion objetivo.

El sistema esta orientado al aprendizaje y comparacion de algoritmos de busqueda en espacios de estados, midiendo la longitud de la ruta encontrada, los nodos explorados y el tiempo de ejecucion.

---

## Patron de arquitectura

Se utiliza el patron de capas (Layered Architecture), organizado en tres niveles: Router, Service y Model. El frontend es independiente y se comunica unicamente con la capa de routers a traves de la API REST.

```
+-------------------+
|     Frontend      |
|  HTML / CSS / JS  |
+--------+----------+
         |  HTTP (JSON)
         v
+--------+----------+
|   API REST Layer  |
|  maze_router.py   |
|  search_router.py |
+--------+----------+
         |
         v
+--------+----------+
|   Service Layer   |
|  maze_service.py  |
|  search_service.py|
+--------+----------+
         |
         v
+--------+----------+
|  Algorithm Layer  |
|    bfs.py         |
|    dfs.py         |
+--------+----------+
         |
         v
+--------+----------+
|    Model Layer    |
|    maze.py        |
|  search_result.py |
+-------------------+
```

El Frontend envia la configuracion del laberinto a la API REST. El Router valida la peticion y delega al Service correspondiente. El Service construye el modelo Maze y llama al algoritmo. El algoritmo opera sobre el modelo y retorna un SearchResult que sube por las capas hasta el cliente.

---

## Estructura del proyecto

```
robomaze/
    backend/
        app/
            algorithms/
                bfs.py           - Implementacion manual de BFS con deque
                dfs.py           - Implementacion manual de DFS con lista como pila
            models/
                maze.py          - Clase Maze: cuadricula y logica de vecinos
                search_result.py - Clase SearchResult: resultado de busqueda
            routers/
                maze_router.py   - Endpoints GET /maze/predefined
                search_router.py - Endpoints POST /search/bfs, /dfs, /both
            services/
                maze_service.py  - Construye Maze y retorna laberintos predefinidos
                search_service.py- Orquesta la ejecucion de BFS y DFS
            main.py              - Punto de entrada FastAPI, CORS, routers
        requirements.txt         - Dependencias Python
    frontend/
        index.html               - Unica pagina del sistema
        css/
            styles.css           - Estilos de la interfaz
        js/
            api.js               - Funciones de comunicacion con la API
            maze.js              - Renderizado y edicion del laberinto
            ui.js                - Inicializacion, eventos y visualizacion de resultados
    docs/
        manual_tecnico.md        - Este documento
        manual_usuario.md        - Guia de instalacion y uso
    .gitignore
    README.md
```

---

## Algoritmos implementados

### Breadth-First Search (BFS)

BFS explora el grafo por niveles usando una cola FIFO (collections.deque). Desde el nodo inicial agrega todos sus vecinos no visitados a la cola, luego los vecinos de esos vecinos, y asi sucesivamente. La primera vez que se alcanza el nodo destino se garantiza que la ruta es optima (minima cantidad de celdas).

- Complejidad temporal: O(V + E), donde V = filas * columnas y E = aristas entre celdas libres adyacentes.
- Complejidad espacial: O(V) para la cola y el diccionario de padres.
- Garantia: ruta optima cuando todos los costos de arista son iguales.

### Depth-First Search (DFS)

DFS explora el grafo profundizando por cada rama usando una pila LIFO (lista de Python). Desde el nodo inicial empuja sus vecinos a la pila, saca el ultimo y repite. No garantiza la ruta optima; la ruta encontrada depende del orden en que se agregan los vecinos.

- Complejidad temporal: O(V + E).
- Complejidad espacial: O(V) para la pila y el diccionario de padres.
- Garantia: encuentra una ruta si existe, pero puede ser suboptima.

### Diferencias en comportamiento

| Criterio           | BFS                      | DFS                         |
|--------------------|--------------------------|-----------------------------|
| Estructura         | Cola (FIFO)              | Pila (LIFO)                 |
| Ruta encontrada    | Optima (mas corta)       | No necesariamente optima    |
| Nodos explorados   | Generalmente mas nodos   | Puede explorar menos nodos  |
| Uso de memoria     | Mayor (cola mas amplia)  | Menor en grafos profundos   |

---

## API REST

### GET /

Retorna el estado de la API.

Respuesta:
```json
{
  "status": "ok",
  "app": "RoboMaze API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### GET /maze/predefined

Retorna la lista de los 5 laberintos predefinidos.

Respuesta:
```json
[
  {
    "id": 1,
    "name": "simple",
    "description": "Laberinto sencillo con camino directo",
    "rows": 10,
    "cols": 10,
    "start": [0, 0],
    "end": [9, 9],
    "grid": [[0,0,...], ...]
  },
  ...
]
```

---

### POST /search/bfs

Ejecuta BFS sobre el laberinto recibido.

Cuerpo de la peticion:
```json
{
  "rows": 10,
  "cols": 10,
  "grid": [[0,0,1,...], ...],
  "start": [0, 0],
  "end": [9, 9]
}
```

Respuesta (ruta encontrada):
```json
{
  "algorithm": "BFS",
  "path": [[0,0],[0,1],...,[9,9]],
  "path_length": 18,
  "explored_nodes": 45,
  "execution_time_ms": 0.21,
  "found": true
}
```

Respuesta (sin ruta):
```json
{
  "algorithm": "BFS",
  "path": [],
  "path_length": 0,
  "explored_nodes": 50,
  "execution_time_ms": 0.18,
  "found": false,
  "message": "No existe ruta entre el inicio y el destino."
}
```

---

### POST /search/dfs

Misma estructura de peticion y respuesta que `/search/bfs`, con `"algorithm": "DFS"`.

---

### POST /search/both

Ejecuta ambos algoritmos y retorna los dos resultados.

Respuesta:
```json
{
  "bfs": { ... },
  "dfs": { ... }
}
```

---

## Requerimientos funcionales

- RF01: Representar laberintos como cuadriculas bidimensionales de 0s y 1s.
- RF02: Implementar el algoritmo BFS de forma manual.
- RF03: Implementar el algoritmo DFS de forma manual.
- RF04: Permitir definir posicion inicial y posicion objetivo.
- RF05: Permitir colocar y quitar obstaculos en la cuadricula.
- RF06: Mostrar graficamente la ruta encontrada sobre la cuadricula.
- RF07: Mostrar la cantidad de nodos explorados por cada algoritmo.
- RF08: Mostrar el tiempo de ejecucion en milisegundos.
- RF09: Ejecutar BFS y DFS de forma independiente o conjunta.
- RF10: Exponer los algoritmos mediante una API REST.
- RF11: Proveer 5 laberintos predefinidos desde la API.
- RF12: Informar cuando no existe ruta entre inicio y destino.

---

## Requerimientos no funcionales

- RNF01 Rendimiento: los algoritmos deben responder en menos de 500 ms para cuadriculas de hasta 20x20 en hardware de escritorio estandar.
- RNF02 Mantenibilidad: el codigo sigue el patron de capas; cada modulo tiene una responsabilidad unica y esta documentado con docstrings.
- RNF03 Usabilidad: la interfaz web no requiere instalacion adicional; basta con abrir index.html en el navegador.
- RNF04 Escalabilidad: la arquitectura permite agregar nuevos algoritmos de busqueda creando un modulo en `algorithms/` y un endpoint en `search_router.py` sin modificar el resto del sistema.
- RNF05 Portabilidad: el backend requiere Python 3.11 o superior; el frontend funciona en cualquier navegador moderno sin dependencias externas.

---

## Posibles mejoras futuras

- Generacion automatica de laberintos mediante algoritmos como Recursive Backtracker o Kruskal.
- Implementacion del algoritmo A* para comparacion con heuristica de distancia Manhattan.
- Animaciones del proceso de exploracion, mostrando cada nodo al momento de ser visitado.
- Guardado y carga de laberintos personalizados en formato JSON.
- Estadisticas comparativas graficas (graficas de barras de nodos explorados y tiempo).
- Soporte para laberintos de tamano variable configurable desde la interfaz.
- Multiples puntos objetivo.
- Exportacion de resultados a CSV o PDF.
