# Documento Tecnico - Smart Warehouse

**Curso:** Inteligencia Artificial 1
**Universidad:** Universidad de San Carlos de Guatemala
**Facultad:** Ingenieria en Ciencias y Sistemas
**Fecha:** Junio 2026

---

## 1. Arquitectura del Sistema

### Diagrama de Componentes

```
+------------------+        HTTP/REST        +-------------------+
|                  | <---------------------> |                   |
|   FRONTEND WEB   |                         |   BACKEND PYTHON  |
|  (HTML/CSS/JS)   |   fetch() / JSON        |   (Flask)         |
|                  | <---------------------> |   app.py          |
+------------------+                         +--------+----------+
                                                      |
                                                      | pyswip
                                                      |
                                             +--------+----------+
                                             |                   |
                                             |   MOTOR PROLOG    |
                                             |   (SWI-Prolog)    |
                                             |   warehouse.pl    |
                                             +-------------------+
```

### Descripcion de Componentes

| Componente | Tecnologia | Responsabilidad |
|---|---|---|
| Frontend | HTML + CSS + JavaScript | Visualizar el mapa, controlar la simulacion, mostrar estadisticas e historial |
| Backend | Python 3 + Flask | Gestionar el estado de la simulacion, exponer la API REST, coordinar la comunicacion con Prolog |
| Motor de Inferencia | SWI-Prolog | Tomar decisiones sobre las acciones de los robots mediante reglas de inferencia |
| Interfaz Prolog | pyswip | Puente de comunicacion entre Python y SWI-Prolog |

---

## 2. Tecnologias Utilizadas

| Tecnologia | Version | Proposito |
|---|---|---|
| SWI-Prolog | 10.0.2 | Motor de inferencia y toma de decisiones de los robots |
| Python | 3.13+ | Desarrollo del backend, gestion del estado y coordinacion |
| Flask | 3.1.3 | Framework web para la API REST |
| flask-cors | 6.0.5 | Manejo de CORS para peticiones desde el frontend |
| pyswip | 0.3.3 | Integracion entre Python y SWI-Prolog |
| HTML5 | - | Estructura de la interfaz web |
| CSS3 | - | Estilos y visualizacion del mapa |
| JavaScript (ES2020) | - | Logica del cliente, renderizado y comunicacion con el backend |
| Git | 2.x | Control de versiones |

---

## 3. Estructura del Proyecto

```
PROYECTO2/
    backend/
        app.py              - Servidor Flask. Define los endpoints REST y gestiona el estado
        prolog_interface.py - Clase PrologInterface. Encapsula todas las consultas a SWI-Prolog
        requirements.txt    - Dependencias Python del proyecto
    prolog/
        warehouse.pl        - Base de conocimiento. Hechos del mapa y reglas de inferencia
    frontend/
        index.html          - Interfaz web principal con el mapa y los controles
        styles.css          - Estilos visuales del sistema
        app.js              - Logica JavaScript del cliente
    docs/
        documento_tecnico.md - Este archivo
        manual_usuario.md    - Guia de instalacion y uso del sistema
        evidencias/          - Capturas de pantalla del sistema en funcionamiento
    .gitignore
    README.md
```

---

## 4. Reglas de Inferencia Implementadas en Prolog

Archivo: `prolog/warehouse.pl`

### Regla 1: casilla_valida/2

**Descripcion:** Verifica que una casilla este dentro de los limites del mapa 10x10 y no sea un obstaculo.

```prolog
casilla_valida(F, C) :-
    dimension(MaxF, MaxC),
    F > 0, F =< MaxF,
    C > 0, C =< MaxC,
    \+ obstaculo(F, C).
```

**Consulta de ejemplo:**
```prolog
?- casilla_valida(1, 1).
true.

?- casilla_valida(2, 2).
false.
```

---

### Regla 2: puede_mover_arriba/4

**Descripcion:** Determina si el robot puede moverse a la fila superior. Calcula la nueva fila y valida la casilla.

```prolog
puede_mover_arriba(F, C, NF, C) :-
    NF is F - 1,
    casilla_valida(NF, C).
```

**Consulta de ejemplo:**
```prolog
?- puede_mover_arriba(3, 1, NF, NC).
NF = 2, NC = 1.
```

---

### Regla 3: puede_mover_abajo/4

**Descripcion:** Determina si el robot puede moverse a la fila inferior. Calcula la nueva fila y valida la casilla.

```prolog
puede_mover_abajo(F, C, NF, C) :-
    NF is F + 1,
    casilla_valida(NF, C).
```

---

### Regla 4: puede_mover_izquierda/4 y puede_mover_derecha/4

**Descripcion:** Determinan si el robot puede moverse en direccion horizontal. Calculan la nueva columna y validan la casilla.

```prolog
puede_mover_izquierda(F, C, F, NC) :- NC is C - 1, casilla_valida(F, NC).
puede_mover_derecha(F, C, F, NC)   :- NC is C + 1, casilla_valida(F, NC).
```

---

### Regla 5: puede_recoger/3

**Descripcion:** El robot puede recoger un paquete si esta exactamente en la misma casilla. Usa corte (!) para retornar solo la primera coincidencia.

```prolog
puede_recoger(RobotF, RobotC, PaqueteID) :-
    paquete(PaqueteID, RobotF, RobotC, _),
    !.
```

**Consulta de ejemplo:**
```prolog
?- puede_recoger(1, 4, PID).
PID = p1.
```

---

### Regla 6: puede_entregar/3

**Descripcion:** El robot puede entregar el paquete si se encuentra en la zona de entrega asignada a ese paquete. Usa corte (!) para evitar backtracking innecesario.

```prolog
puede_entregar(RobotF, RobotC, PaqueteID) :-
    paquete(PaqueteID, _, _, ZonaID),
    zona_entrega(ZonaID, RobotF, RobotC),
    !.
```

**Consulta de ejemplo:**
```prolog
?- puede_entregar(1, 9, p1).
true.
```

---

### Regla 7: decidir_accion/7

**Descripcion:** Regla principal de decision. Determina la accion a ejecutar segun el estado actual del robot. Evalua en orden de prioridad: (1) entregar si ya esta en la zona correcta, (2) recoger si hay un paquete en su posicion, (3) navegar hacia el destino usando BFS (Regla 8). Usa corte (!) en cada caso para garantizar una decision unica.

```prolog
decidir_accion(RobotF, RobotC, LlevaPaquete, PaqueteID, DestF, DestC, Accion)
```

**Parametros de entrada:**
- `RobotF, RobotC`: posicion actual del robot
- `LlevaPaquete`: atomo `si` o `no`
- `PaqueteID`: ID del paquete que lleva, o `ninguno`
- `DestF, DestC`: coordenadas del destino calculadas por el backend

**Parametro de salida:**
- `Accion`: una de `entregar_paquete`, `recoger_paquete`, `mover_arriba`, `mover_abajo`, `mover_derecha`, `mover_izquierda`, `esperar`

**Consulta de ejemplo:**
```prolog
?- decidir_accion(1, 1, no, ninguno, 1, 4, Accion).
Accion = mover_derecha.

?- decidir_accion(1, 4, no, ninguno, 1, 4, Accion).
Accion = recoger_paquete.

?- decidir_accion(1, 9, si, p1, 1, 9, Accion).
Accion = entregar_paquete.
```

---

### Regla 8: BFS para navegacion optima (siguiente_movimiento/5 y bfs_buscar/5)

**Descripcion:** Busqueda en anchura (BFS) que encuentra el camino mas corto desde la posicion actual hasta el destino, evitando obstaculos. Retorna la primera accion del camino optimo. Garantiza que el robot nunca quede bloqueado mientras exista un camino.

```prolog
% Punto de entrada del BFS
siguiente_movimiento(InicioF, InicioC, DestF, DestC, Accion) :-
    bfs_buscar([[InicioF, InicioC, none]], DestF, DestC, [InicioF-InicioC], Accion).

% Caso base: se llego al destino
bfs_buscar([[DestF, DestC, Accion]|_], DestF, DestC, _, Accion) :-
    Accion \= none, !.

% Caso recursivo: expandir nodos
bfs_buscar([[F, C, PrimerAccion]|Cola], DestF, DestC, Visitados, Resultado) :-
    findall([NF, NC, PA], (
        movimiento_bfs(F, C, NF, NC, Act),
        \+ member(NF-NC, Visitados),
        (PrimerAccion = none -> PA = Act ; PA = PrimerAccion)
    ), Hijos),
    findall(NF-NC, member([NF, NC, _], Hijos), NuevosVisitados),
    append(Visitados, NuevosVisitados, TodosVisitados),
    append(Cola, Hijos, ColaNueva),
    bfs_buscar(ColaNueva, DestF, DestC, TodosVisitados, Resultado).
```

**Consulta de ejemplo:**
```prolog
% Robot en (5,9) hacia (5,2): hay obstaculo en (5,8), BFS rodea por arriba
?- siguiente_movimiento(5, 9, 5, 2, Accion).
Accion = mover_arriba.
```

---

### Regla 9: zona_de_paquete/4 y utilidades

**Descripcion:** Consulta la zona de entrega asociada a un paquete. Utiliza encadenamiento de hechos `paquete/4` y `zona_entrega/3`.

```prolog
zona_de_paquete(PaqueteID, ZonaID, ZonaF, ZonaC) :-
    paquete(PaqueteID, _, _, ZonaID),
    zona_entrega(ZonaID, ZonaF, ZonaC).
```

**Consulta de ejemplo:**
```prolog
?- zona_de_paquete(p1, ZID, ZF, ZC).
ZID = zona1, ZF = 1, ZC = 9.
```

---

## 5. Funcionamiento General

### Flujo de una Simulacion

```
1. El usuario abre index.html en el navegador.
2. app.js llama a GET /api/mapa/inicial para renderizar el mapa en estado inicial.
3. El usuario hace clic en "Iniciar".
4. app.js llama a POST /api/simulacion/iniciar.
5. El backend carga el estado inicial desde Prolog y retorna el estado al frontend.
6. Por cada paso (automatico o manual):
   a. app.js llama a GET /api/simulacion/paso.
   b. El backend calcula el destino del robot (paquete o zona segun si lleva carga).
   c. El backend consulta a Prolog: decidir_accion(F, C, lleva, pid, DF, DC, Accion).
   d. Prolog evalua las reglas y retorna la accion.
   e. El backend aplica la accion al estado (mueve coordenadas, marca paquetes).
   f. El backend retorna el nuevo estado al frontend.
   g. app.js renderiza el mapa actualizado y actualiza estadisticas.
7. Cuando todos los paquetes estan entregados, la simulacion se marca como completada.
8. El historial se actualiza con los resultados de la simulacion.
```

### Comunicacion Frontend - Backend

El frontend se comunica con el backend mediante peticiones HTTP usando la API Fetch de JavaScript. Todas las respuestas son en formato JSON. El backend corre en `http://localhost:5000`.

### Comunicacion Backend - Prolog

El backend usa la libreria `pyswip` para instanciar SWI-Prolog y ejecutar consultas directamente desde Python. La clase `PrologInterface` encapsula esta logica y expone metodos de alto nivel como `decidir_accion()` y `zona_de_paquete()`.

### Actualizacion del Estado del Mapa

El estado del mapa (posiciones de robots, estado de paquetes) se mantiene en memoria en el backend (`estado_simulacion`). Prolog no guarda estado: se usa exclusivamente como motor de inferencia sin efectos secundarios. Cada consulta a Prolog recibe el estado actual como argumentos y retorna la accion recomendada.

---

## 6. Distribucion del Trabajo

| Nombre | Carnet | Tareas Realizadas |
|---|---|---|
| Joaquin Emmanuel Aldair Coromac Huezo | 201903873 | Arquitectura del sistema, base de conocimiento Prolog |
