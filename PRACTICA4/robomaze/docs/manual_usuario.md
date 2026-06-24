# Manual de Usuario - RoboMaze

## Requisitos previos

- Python 3.11 o superior instalado en el sistema.
- Pip actualizado (`python -m pip install --upgrade pip`).
- Navegador web actualizado (Chrome, Firefox, Edge o equivalente).
- Conexion a internet no requerida en modo local.

---

## Instalacion del backend

### Paso 1: Abrir una terminal

Abra una terminal (PowerShell, CMD o bash) en la carpeta raiz del proyecto (`robomaze/`).

### Paso 2: Entrar a la carpeta backend

```
cd backend
```

### Paso 3: Crear el entorno virtual

```
python -m venv venv
```

### Paso 4: Activar el entorno virtual

En Windows:
```
venv\Scripts\activate
```

En Linux / macOS:
```
source venv/bin/activate
```

### Paso 5: Instalar dependencias

```
pip install -r requirements.txt
```

### Paso 6: Iniciar el servidor

```
uvicorn app.main:app --reload --port 8000
```

Si el servidor inicia correctamente vera en la terminal:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

La documentacion interactiva de la API estara disponible en:
```
http://localhost:8000/docs
```

---

## Uso del frontend

Abra el archivo `frontend/index.html` directamente en el navegador (doble clic o arrastrar al navegador). No se necesita ninguna instalacion adicional.

Asegurese de que el backend esta en ejecucion antes de abrir el frontend, ya que la interfaz se conecta automaticamente a `http://localhost:8000`.

---

## Como usar el sistema

### 1. Cargar un laberinto predefinido

Al abrir la aplicacion, el sistema descarga automaticamente los 5 laberintos predefinidos desde la API y los muestra en el selector "Laberinto predefinido". Seleccione uno de la lista para cargarlo en la cuadricula.

Los laberintos disponibles son:
- simple: camino directo sin muchos obstaculos.
- medio: dificultad media con varios pasillos.
- largo: ruta larga en forma de espiral.
- sinruta: laberinto sin solucion (muro central completo).
- complejo: multiples bifurcaciones y obstaculos.

### 2. Editar el laberinto

Use los botones de "Modo de edicion" para elegir la accion que realizara al hacer clic sobre una celda:

- **Colocar / quitar obstaculo**: hace clic en una celda libre para convertirla en obstaculo (negro), y en un obstaculo para liberarla.
- **Definir posicion inicial**: el siguiente clic marca la celda como punto de partida (verde).
- **Definir posicion destino**: el siguiente clic marca la celda como punto de llegada (rojo).

El boton del modo activo aparece resaltado en azul oscuro.

### 3. Ejecutar los algoritmos

Haga clic en uno de los botones del panel "Ejecutar algoritmos":

- **Ejecutar BFS**: busca la ruta optima (mas corta) con Breadth-First Search.
- **Ejecutar DFS**: busca una ruta con Depth-First Search.
- **Ejecutar BFS y DFS**: ejecuta ambos algoritmos y muestra los dos resultados.

Si no ha definido inicio o destino, aparecera un mensaje de error en rojo.

### 4. Leer los resultados

El panel "Resultados" muestra, para cada algoritmo ejecutado:

- Si se encontro ruta o no.
- Longitud de la ruta (cantidad de celdas).
- Nodos explorados durante la busqueda.
- Tiempo de ejecucion en milisegundos.

La ruta encontrada se visualiza en la cuadricula en color azul. Si no existe ruta, el panel muestra el mensaje "No existe ruta entre el inicio y el destino."

### Leyenda de colores de la cuadricula

| Color       | Significado           |
|-------------|-----------------------|
| Blanco      | Celda libre           |
| Negro       | Obstaculo             |
| Verde       | Posicion inicial      |
| Rojo        | Posicion destino      |
| Azul        | Ruta encontrada       |
| Amarillo    | Nodo explorado        |

---

## Capturas de pantalla

*Las capturas de pantalla del sistema en funcionamiento se agregan en esta seccion una vez que el sistema este desplegado.*

<!-- Agregar capturas reales del laberinto cargado, la ejecucion de BFS y DFS, y la comparacion de resultados. -->
