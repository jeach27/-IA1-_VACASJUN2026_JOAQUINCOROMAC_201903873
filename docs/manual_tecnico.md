# Manual Tecnico
## Sistema de Rutas entre Ciudades

**Universidad San Carlos de Guatemala**
Facultad de Ingenieria - Ingenieria en Ciencias y Sistemas
Practica 1 - Inteligencia Artificial 1

---

## Tabla de contenidos

1. [Arquitectura del sistema](#1-arquitectura-del-sistema)
2. [Estructura del proyecto](#2-estructura-del-proyecto)
3. [Modulo Prolog](#3-modulo-prolog)
4. [Backend Python](#4-backend-python)
5. [Integracion Python-Prolog](#5-integracion-python-prolog)
6. [Frontend](#6-frontend)
7. [Flujo completo de una solicitud](#7-flujo-completo-de-una-solicitud)
8. [Mejoras futuras](#8-mejoras-futuras)

---

## 1. Arquitectura del sistema

El sistema utiliza el **patron Repository + Service** en el backend Python. Este patron divide las responsabilidades en capas independientes:

```
Frontend (HTML/CSS/JS)
        |
        | HTTP (REST)
        v
   Router (FastAPI)        <- define endpoints HTTP
        |
   Service Layer           <- logica de negocio y validaciones
        |
   Repository Layer        <- unica capa que habla con Prolog
        |
   SWI-Prolog (PySwip)     <- motor logico e inferencia
```

### Razon de eleccion del patron

- **Repository:** Aísla toda la comunicacion con Prolog. Si en el futuro se cambia la forma de comunicarse con Prolog (por ejemplo, via subprocess en lugar de PySwip), solo se modifica el repositorio.
- **Service:** Centraliza las validaciones y la construccion de respuestas. Los routers permanecen limpios y delegativos.
- **Restriccion de la practica:** Prolog es el motor de logica. Python no implementa ningun algoritmo de rutas; solo traduce solicitudes HTTP a consultas Prolog y regresa los resultados.

---

## 2. Estructura del proyecto

```
[IA1]_VACASJUN2026_JOAQUINCOROMAC_201903873/
|
+-- prolog/
|   +-- ciudades.pl          # Base de conocimiento y reglas de busqueda
|
+-- backend/
|   +-- main.py              # Punto de entrada de la app FastAPI
|   +-- dependencias.py      # Singleton del repositorio y servicio
|   +-- requirements.txt     # Dependencias Python
|   +-- models/
|   |   +-- esquemas.py      # Modelos Pydantic (validacion de datos)
|   +-- repositories/
|   |   +-- prolog_repositorio.py  # Consultas directas a SWI-Prolog
|   +-- services/
|   |   +-- ruta_servicio.py       # Logica de negocio
|   +-- routers/
|       +-- rutas.py               # Endpoints HTTP
|
+-- frontend/
|   +-- index.html           # Interfaz de usuario
|   +-- css/
|   |   +-- estilos.css
|   +-- js/
|       +-- app.js
|
+-- docs/
|   +-- manual_usuario.md
|   +-- manual_tecnico.md
|
+-- .gitignore
```

---

## 3. Modulo Prolog

Archivo: `prolog/ciudades.pl`

### 3.1. Hechos base

```prolog
conexion(CiudadA, CiudadB, DistanciaKm).
```

Representa una carretera directa entre dos ciudades. La relacion es unidireccional en el hecho, pero se vuelve bidireccional mediante la regla `camino/3`.

**Ejemplo:**

```prolog
conexion(guatemala, escuintla, 64).
conexion(guatemala, antigua, 45).
```

### 3.2. Relacion simetrica

```prolog
camino(X, Y, D) :- conexion(X, Y, D).
camino(X, Y, D) :- conexion(Y, X, D).
```

Permite viajar en ambas direcciones sin duplicar los hechos `conexion/3`.

### 3.3. Busqueda de rutas sin ciclos

```prolog
ruta(Origen, Destino, Ruta, Distancia) :-
    ruta_aux(Origen, Destino, [Origen], RutaInversa, Distancia),
    reverse(RutaInversa, Ruta).

ruta_aux(Destino, Destino, Visitados, Visitados, 0).
ruta_aux(Actual, Destino, Visitados, RutaFinal, Distancia) :-
    camino(Actual, Siguiente, D),
    \+ member(Siguiente, Visitados),
    ruta_aux(Siguiente, Destino, [Siguiente|Visitados], RutaFinal, DistResto),
    Distancia is D + DistResto.
```

**Como funciona:**

- `ruta_aux/5` es el predicado recursivo. Recibe el nodo actual, el destino, la lista de ciudades visitadas, la ruta acumulada y la distancia acumulada.
- Caso base: cuando `Actual == Destino`, la distancia restante es 0 y la ruta es la lista de visitados.
- Caso recursivo: elige un vecino `Siguiente` que no este en `Visitados` (evita ciclos con `\+ member`), lo agrega a la lista y continua la busqueda.
- Al retornar, acumula la distancia.
- El resultado final se invierte con `reverse/2` porque la lista se construye en orden inverso.

### 3.4. Ruta mas corta

```prolog
ruta_mas_corta(Origen, Destino, RutaOptima, DistanciaOptima) :-
    findall(D-R, ruta(Origen, Destino, R, D), Rutas),
    Rutas \= [],
    sort(Rutas, [DistanciaOptima-RutaOptima|_]).
```

`findall/3` reune todas las soluciones de `ruta/4`. `sort/2` ordena la lista de pares `Distancia-Ruta` de menor a mayor (Prolog compara terminos: primero por distancia numerica). El primer elemento de la lista ordenada es la ruta optima.

### 3.5. Predicado dinamico

```prolog
:- dynamic conexion/3.

agregar_conexion(Ciudad1, Ciudad2, Distancia) :-
    ( conexion(Ciudad1, Ciudad2, _) ->
        retract(conexion(Ciudad1, Ciudad2, _))
    ; true ),
    assertz(conexion(Ciudad1, Ciudad2, Distancia)).
```

`assertz/1` agrega un hecho al final de la base de conocimiento en tiempo de ejecucion. Si ya existe una conexion entre las mismas ciudades, se elimina con `retract/1` antes de agregar la nueva (actualizacion).

---

## 4. Backend Python

### 4.1. Capa de modelos (models/esquemas.py)

Define los contratos de datos usando **Pydantic**. Valida automaticamente los tipos de entrada/salida de los endpoints. Por ejemplo:

```python
class ConsultaRuta(BaseModel):
    origen: str
    destino: str
```

Si el cliente envia un JSON sin el campo `origen`, FastAPI devuelve un error 422 automaticamente.

### 4.2. Capa de repositorio (repositories/prolog_repositorio.py)

Es la unica clase que instancia `pyswip.Prolog`. Carga el archivo `.pl` una sola vez y expone metodos que encapsulan cada consulta Prolog:

| Metodo | Consulta Prolog |
|---|---|
| `obtener_ciudades()` | `todas_ciudades(Ciudades)` |
| `obtener_conexiones()` | `conexion(Origen, Destino, Distancia)` |
| `ciudad_existe(c)` | `ciudad_existe(c)` |
| `obtener_ruta_mas_corta(o, d)` | `ruta_mas_corta(o, d, Ruta, Distancia)` |
| `obtener_todas_rutas(o, d)` | `ruta(o, d, Ruta, Distancia)` (backtracking) |
| `agregar_conexion(c1, c2, dist)` | `agregar_conexion(c1, c2, dist)` |

### 4.3. Capa de servicio (services/ruta_servicio.py)

Contiene la logica de negocio:
- Valida que las ciudades existan antes de ejecutar la busqueda.
- Convierte los nombres a minusculas con guion bajo.
- Lanza `HTTPException` con codigo y mensaje claro cuando una operacion no puede completarse.
- Construye objetos Pydantic de respuesta a partir de los datos crudos del repositorio.

### 4.4. Capa de router (routers/rutas.py)

Define los endpoints HTTP con sus metodos, rutas URL y tipos de respuesta. Delega completamente al servicio mediante inyeccion de dependencias de FastAPI:

| Metodo | Endpoint | Descripcion |
|---|---|---|
| GET | `/api/ciudades` | Lista todas las ciudades |
| GET | `/api/conexiones` | Lista todas las conexiones |
| POST | `/api/ruta-mas-corta` | Calcula la ruta optima |
| POST | `/api/todas-las-rutas` | Devuelve todas las rutas ordenadas |
| POST | `/api/conexion` | Agrega una nueva conexion |

### 4.5. Gestion de dependencias (dependencias.py)

El repositorio y el servicio se crean una sola vez al iniciar la aplicacion (patron Singleton). FastAPI los inyecta en cada handler mediante `Depends(obtener_servicio)`. Esto evita reconectar a Prolog en cada solicitud.

---

## 5. Integracion Python-Prolog

La libreria **PySwip 0.3.x** carga la DLL de SWI-Prolog en el proceso Python y permite ejecutar consultas Prolog directamente desde Python. Se usa con SWI-Prolog 10.x.

**Deteccion automatica de SWI-Prolog:**

PySwip busca SWI-Prolog en el registro de Windows. Si esta instalado en una ruta personalizada, el repositorio lo detecta automaticamente usando `shutil.which`:

```python
import shutil, os
swipl_exe = shutil.which("swipl")
if swipl_exe:
    os.environ["SWI_HOME_DIR"] = os.path.dirname(os.path.dirname(swipl_exe))
```

Esta deteccion debe realizarse **antes** de importar PySwip, ya que la libreria busca la DLL al momento de la importacion.

**Flujo de una consulta:**

```python
from pyswip import Prolog

prolog = Prolog()
prolog.consult("prolog/ciudades.pl")  # Carga el archivo .pl

resultados = list(prolog.query("ruta_mas_corta(guatemala, flores, Ruta, Distancia)"))
# resultados = [{"Ruta": ["guatemala", "chimaltenango", "coban", "flores"], "Distancia": 493}]
ruta   = [str(c) for c in resultados[0]["Ruta"]]
distancia = int(resultados[0]["Distancia"])
```

**Estrategia para consultas que retornan estructuras:**

En PySwip 0.3.x los terminos compuestos (como `O-D-Dist`) llegan como strings, no como objetos con `.args`. Por eso el repositorio usa consultas con **variables individuales** en lugar de predicados que devuelven listas de terminos anidados:

```python
# Forma correcta: variables separadas (PySwip 0.3.x)
resultados = list(prolog.query("conexion(Origen, Destino, Distancia)"))
# resultados = [{"Origen": "guatemala", "Destino": "escuintla", "Distancia": 64}, ...]

# Forma correcta para todas las rutas: query directo a ruta/4
resultados = list(prolog.query("ruta(guatemala, flores, Ruta, Distancia)"))
# Cada resultado tiene Ruta como lista Python y Distancia como int
```

---

## 6. Frontend

El frontend es una SPA (Single Page Application) de una sola pagina HTML con CSS y JavaScript puro, sin frameworks.

**Comunicacion con el backend:**

Usa la API `fetch` para realizar solicitudes HTTP al backend:

```javascript
const resp = await fetch("http://localhost:8000/api/ruta-mas-corta", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ origen: "guatemala", destino: "flores" }),
});
```

**Estructura de la interfaz:**

- **Pestana 1 - Ruta Optima:** Selectores de ciudad + resultado con chips visuales.
- **Pestana 2 - Todas las Rutas:** Tabla ordenada con indicador de ruta optima.
- **Pestana 3 - Administrar:** Formulario para agregar conexiones + vistas de ciudades y conexiones registradas.

**Normalizacion de nombres:**

La funcion `formatearCiudad` convierte el identificador interno (`puerto_barrios`) al texto visible (`Puerto Barrios`) para mostrar al usuario.

---

## 7. Flujo completo de una solicitud

Ejemplo: el usuario solicita la ruta mas corta de Guatemala a Flores.

```
1. Usuario selecciona "Guatemala" y "Flores" en el frontend.
2. app.js llama: POST /api/ruta-mas-corta { "origen": "guatemala", "destino": "flores" }
3. FastAPI enruta a routers/rutas.py -> funcion ruta_mas_corta()
4. El router llama a RutaServicio.ruta_mas_corta("guatemala", "flores")
5. El servicio valida que ambas ciudades existen (via repositorio).
6. El servicio llama a repositorio.obtener_ruta_mas_corta("guatemala", "flores")
7. El repositorio ejecuta en Prolog:
       ruta_mas_corta(guatemala, flores, Ruta, Distancia)
8. Prolog recorre el grafo, reune todas las rutas con findall/3 y retorna la menor.
9. El repositorio parsea el resultado y lo devuelve al servicio.
10. El servicio construye un objeto RespuestaRutaMasCorta.
11. FastAPI serializa el objeto a JSON y lo envia al frontend.
12. app.js renderiza los chips de ciudades y la distancia total.
```

---

## 8. Mejoras futuras

| Mejora | Descripcion |
|---|---|
| Persistencia de conexiones | Guardar nuevas conexiones en el archivo `.pl` para que sobrevivan al reinicio del servidor. |
| Visualizacion del grafo | Renderizar el grafo de ciudades con una libreria como Vis.js o D3.js. |
| Pesos por tipo de carretera | Distinguir entre carretera asfaltada, terraceria o autopista con diferentes costos. |
| Busqueda bidireccional | Implementar en Prolog la busqueda bidireccional para reducir el espacio de busqueda. |
| Pruebas automatizadas | Agregar tests con pytest para verificar cada endpoint y las reglas Prolog. |
| Autenticacion | Proteger los endpoints de escritura con API key para evitar modificaciones no autorizadas. |
| Exportar resultados | Permitir descargar la ruta encontrada en formato PDF o CSV. |
