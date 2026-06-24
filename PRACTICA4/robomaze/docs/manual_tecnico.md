# Manual Tecnico - RoboMaze

## Descripcion general del sistema

RoboMaze es un sistema de busqueda de rutas en laberintos virtuales. Permite representar un laberinto como una cuadricula bidimensional donde cada celda puede ser libre u obstaculo, y ejecutar los algoritmos BFS, DFS y A* para encontrar rutas entre una posicion inicial y una posicion objetivo.

El sistema mide longitud de ruta, nodos explorados y tiempo de ejecucion para comparar el comportamiento de cada algoritmo. Incluye ademas generacion automatica de laberintos, modificacion del tamano de la cuadricula, animacion del proceso de exploracion y tabla comparativa de estadisticas.

---

## Patron de arquitectura

Se utiliza el patron de capas (Layered Architecture), organizado en cuatro niveles de backend mas el frontend independiente. Cada capa solo se comunica con la inmediatamente inferior, lo que facilita el reemplazo o extension de componentes.

```
+---------------------------------------+
|           Frontend                    |
|   index.html / api.js / ui.js         |
|   maze.js / styles.css                |
+-------------------+-------------------+
                    | HTTP JSON
                    v
+---------------------------------------+
|          API REST Layer               |
|   maze_router.py                      |
|   search_router.py                    |
+-------------------+-------------------+
                    |
                    v
+---------------------------------------+
|          Service Layer                |
|   maze_service.py                     |
|   generator_service.py                |
|   search_service.py                   |
+-------------------+-------------------+
                    |
                    v
+---------------------------------------+
|          Algorithm Layer              |
|   bfs.py   dfs.py   astar.py          |
+-------------------+-------------------+
                    |
                    v
+---------------------------------------+
|          Model Layer                  |
|   maze.py   search_result.py          |
+---------------------------------------+
```

Los diagramas completos en PlantUML (clases, componentes y secuencias) se encuentran en `.claude/diagramas_plantuml.md`.

---

## Estructura del proyecto

```
robomaze/
    backend/
        app/
            algorithms/
                bfs.py              - BFS manual con collections.deque
                dfs.py              - DFS manual con lista como pila
                astar.py            - A* manual con heapq y heuristica Manhattan
            models/
                maze.py             - Clase Maze: cuadricula y vecinos validos
                search_result.py    - Clase SearchResult con explored_order
            routers/
                maze_router.py      - GET /maze/predefined, GET /maze/generate
                search_router.py    - POST /search/bfs, /dfs, /astar, /both, /all
            services/
                maze_service.py     - build_maze() y 5 laberintos predefinidos
                generator_service.py- generate_maze() con DFS aleatorizado
                search_service.py   - run_bfs, run_dfs, run_astar, run_both, run_all
            main.py                 - FastAPI, CORS, registro de routers
        requirements.txt
    frontend/
        index.html                  - Unica pagina del sistema
        css/styles.css              - Estilos sin frameworks externos
        js/
            api.js                  - Comunicacion con todos los endpoints
            maze.js                 - Renderizado, animacion y edicion del laberinto
            ui.js                   - Eventos, validacion y visualizacion de resultados
    docs/
        manual_tecnico.md           - Este documento
        manual_usuario.md           - Guia de instalacion y uso
    .gitignore
    README.md
```

---

## Algoritmos implementados

### Breadth-First Search (BFS)

BFS explora el grafo por niveles usando una cola FIFO (`collections.deque`). Desde el nodo inicial agrega todos sus vecinos no visitados a la cola, luego los vecinos de esos vecinos, y asi sucesivamente. La primera vez que se alcanza el destino se garantiza que la ruta es optima.

- Complejidad temporal: O(V + E)
- Complejidad espacial: O(V)
- Garantia: ruta optima (minima cantidad de celdas)

### Depth-First Search (DFS)

DFS explora el grafo profundizando por cada rama usando una pila LIFO (lista de Python). No garantiza la ruta optima.

- Complejidad temporal: O(V + E)
- Complejidad espacial: O(V)
- Garantia: encuentra una ruta si existe, no necesariamente la mas corta

### A* (A-estrella)

A* usa una cola de prioridad (`heapq`) ordenada por f(n) = g(n) + h(n), donde g(n) es el costo acumulado desde el inicio y h(n) es la distancia Manhattan al destino. Al ser la heuristica admisible, garantiza la ruta optima y generalmente explora menos nodos que BFS.

- Complejidad temporal: O(V log V) por el heap
- Complejidad espacial: O(V)
- Garantia: ruta optima con heuristica admisible
- Heuristica: distancia Manhattan |dr| + |dc|

### Diferencias en comportamiento

| Criterio               | BFS                   | DFS                      | A*                        |
|------------------------|-----------------------|--------------------------|---------------------------|
| Estructura interna     | Cola FIFO             | Pila LIFO                | Min-heap por f(n)         |
| Ruta garantizada       | Optima                | No optima                | Optima                    |
| Nodos explorados       | Mayor cantidad        | Variable                 | Menor (guiado por h)      |
| Uso de memoria         | Alto                  | Bajo en grafos profundos | Moderado                  |
| Heuristica             | No                    | No                       | Si (Manhattan)            |

---

## Generacion automatica de laberintos

El servicio `generator_service.py` implementa el algoritmo Recursive Backtracker (DFS aleatorizado):

1. Inicializar toda la cuadricula como obstaculos (valor 1).
2. Marcar la celda (0, 0) como libre y agregarla a la pila.
3. Mientras la pila no este vacia:
   - Obtener la celda actual (cima de la pila).
   - Buscar vecinos a 2 pasos de distancia que no hayan sido visitados.
   - Si existen: elegir uno al azar, abrir esa celda y la pared intermedia (valor 0), agregar a la pila.
   - Si no existen: sacar de la pila (backtrack).
4. Determinar el destino como la celda libre mas lejana en la esquina opuesta.

El resultado es un laberinto perfecto: existe exactamente un camino entre cualquier par de celdas. El tamano puede configurarse entre 5x5 y 25x25.

---

## API REST

### Endpoints disponibles

| Metodo | Ruta                  | Descripcion                                      |
|--------|-----------------------|--------------------------------------------------|
| GET    | /                     | Estado de la API                                 |
| GET    | /maze/predefined      | Lista de 5 laberintos predefinidos               |
| GET    | /maze/generate        | Genera un laberinto aleatorio (rows, cols, seed) |
| POST   | /search/bfs           | Ejecuta BFS                                      |
| POST   | /search/dfs           | Ejecuta DFS                                      |
| POST   | /search/astar         | Ejecuta A*                                       |
| POST   | /search/both          | Ejecuta BFS y DFS                                |
| POST   | /search/all           | Ejecuta BFS, DFS y A* para comparacion           |

### Cuerpo de peticion para /search/*

```json
{
  "rows": 10,
  "cols": 10,
  "grid": [[0,0,1,...], ...],
  "start": [0, 0],
  "end": [9, 9]
}
```

### Respuesta de busqueda

```json
{
  "algorithm": "BFS",
  "path": [[0,0],[0,1],...,[9,9]],
  "path_length": 18,
  "explored_nodes": 45,
  "execution_time_ms": 0.21,
  "found": true,
  "explored_order": [[0,0],[0,1],...]
}
```

El campo `explored_order` contiene los nodos en el orden en que fueron procesados por el algoritmo. El frontend lo usa para la animacion.

### Respuesta de /search/all

```json
{
  "bfs":   { ...resultado BFS...  },
  "dfs":   { ...resultado DFS...  },
  "astar": { ...resultado A*...   }
}
```

---

## Requerimientos funcionales

- RF01: Representar laberintos como cuadriculas bidimensionales de 0s y 1s.
- RF02: Implementar el algoritmo BFS de forma manual.
- RF03: Implementar el algoritmo DFS de forma manual.
- RF04: Implementar el algoritmo A* de forma manual.
- RF05: Permitir definir posicion inicial y posicion objetivo.
- RF06: Permitir colocar y quitar obstaculos en la cuadricula.
- RF07: Mostrar graficamente la ruta encontrada sobre la cuadricula.
- RF08: Mostrar los nodos explorados y el tiempo de ejecucion.
- RF09: Ejecutar BFS, DFS y A* de forma independiente o conjunta.
- RF10: Exponer los algoritmos mediante una API REST.
- RF11: Proveer 5 laberintos predefinidos desde la API.
- RF12: Informar cuando no existe ruta entre inicio y destino.
- RF13: Generar laberintos aleatorios mediante DFS aleatorizado.
- RF14: Permitir modificar el tamano del laberinto (5x5 a 25x25).
- RF15: Animar el proceso de exploracion de nodos en la cuadricula.
- RF16: Mostrar tabla comparativa estadistica de los tres algoritmos.

---

## Requerimientos no funcionales

- RNF01 Rendimiento: los algoritmos responden en menos de 500 ms para cuadriculas de hasta 25x25.
- RNF02 Mantenibilidad: patron de capas con responsabilidad unica por modulo, documentado con docstrings.
- RNF03 Usabilidad: la interfaz web no requiere instalacion adicional; basta con abrir index.html en el navegador con el backend activo.
- RNF04 Escalabilidad: agregar un nuevo algoritmo requiere solo crear un modulo en `algorithms/`, una funcion en `search_service.py` y un endpoint en `search_router.py`.
- RNF05 Portabilidad: el backend requiere Python 3.11+; el frontend funciona en cualquier navegador moderno sin dependencias externas.
- RNF06 Restricciones: no se usan librerias externas de busqueda de rutas ni bases de datos.

---

## Posibles mejoras futuras

- Guardar y cargar laberintos personalizados en formato JSON (localStorage o archivo).
- Graficas de rendimiento comparando los tres algoritmos sobre multiples laberintos.
- Multiples puntos objetivo con busqueda desde la posicion mas cercana.
- Obstaculos dinamicos que se agregan durante la ejecucion del algoritmo.
- Exportacion de resultados y estadisticas a CSV o PDF.
- Soporte para movimiento diagonal (heuristica euclidiana para A*).
- Pesos en las celdas para implementar variantes de costo variable (Dijkstra, A* ponderado).
