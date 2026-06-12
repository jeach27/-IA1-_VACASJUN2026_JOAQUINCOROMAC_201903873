# Manual de Usuario
## Sistema de Rutas entre Ciudades

**Universidad San Carlos de Guatemala**
Facultad de Ingenieria - Ingenieria en Ciencias y Sistemas
Practica 1 - Inteligencia Artificial 1

---

## Tabla de contenidos

1. [Requisitos del sistema](#1-requisitos-del-sistema)
2. [Instalacion](#2-instalacion)
3. [Ejecucion del sistema](#3-ejecucion-del-sistema)
4. [Uso del sistema](#4-uso-del-sistema)
   - [Ruta optima](#41-ruta-optima)
   - [Todas las rutas](#42-todas-las-rutas)
   - [Administrar ciudades y conexiones](#43-administrar-ciudades-y-conexiones)
5. [Ciudades disponibles](#5-ciudades-disponibles)
6. [Mensajes del sistema](#6-mensajes-del-sistema)
7. [Preguntas frecuentes](#7-preguntas-frecuentes)

---

## 1. Requisitos del sistema

| Componente | Version minima |
|---|---|
| Python | 3.11 o superior |
| SWI-Prolog | 9.x o 10.x (64 bits) |
| Navegador web | Chrome, Firefox, Edge (actualizado) |
| Sistema operativo | Windows 10/11, Linux, macOS |

> **Importante:** SWI-Prolog debe instalarse antes de instalar PySwip. Descarga SWI-Prolog desde [https://www.swi-prolog.org/Download.html](https://www.swi-prolog.org/Download.html). En Windows, marca la opcion "Add SWI-Prolog to PATH" durante la instalacion.

---

## 2. Instalacion

### Paso 1: Clonar o descargar el repositorio

```
git clone <URL_DEL_REPOSITORIO>
cd [IA1]_VACASJUN2026_JOAQUINCOROMAC_201903873
```

### Paso 2: Instalar SWI-Prolog

1. Descarga el instalador desde [https://www.swi-prolog.org](https://www.swi-prolog.org)
2. Ejecuta el instalador y sigue las instrucciones.
3. En Windows, asegurate de marcar la opcion "Add SWI-Prolog to PATH".
4. Verifica la instalacion abriendo una terminal y ejecutando:
   ```
   swipl --version
   ```

### Paso 3: Crear entorno virtual de Python

```
cd backend
python -m venv venv
```

Activar el entorno:

- **Windows:**
  ```
  venv\Scripts\activate
  ```
- **Linux / macOS:**
  ```
  source venv/bin/activate
  ```

### Paso 4: Instalar dependencias de Python

```
pip install -r requirements.txt
```

---

## 3. Ejecucion del sistema

### Iniciar el backend

Con el entorno virtual activado y dentro de la carpeta `backend`:

```
python -m uvicorn main:app --reload
```

> En Windows, usa siempre `python -m uvicorn` para garantizar que se usa el uvicorn del entorno activo.

El servidor se iniciara en: `http://localhost:8000`

Podras verificar que esta activo visitando `http://localhost:8000` en el navegador; deberas ver:

```json
{"mensaje": "Sistema de Rutas - API activa. Consulte /docs para la documentacion."}
```

### Abrir el frontend

Abre el archivo `frontend/index.html` directamente en tu navegador. No requiere servidor adicional.

> Si el navegador bloquea las solicitudes al backend por CORS, usa una extension como "Live Server" de VS Code para servir el frontend desde `http://127.0.0.1:5500`.

---

## 4. Uso del sistema

### 4.1. Ruta optima

Esta seccion calcula la ruta con la menor distancia total entre dos ciudades.

**Pasos:**

1. En la pestana **Ruta Optima**, selecciona una ciudad en el campo "Ciudad de Origen".
2. Selecciona una ciudad diferente en "Ciudad de Destino".
3. Presiona el boton **Buscar Ruta Optima**.
4. El resultado mostrara:
   - La secuencia de ciudades del recorrido.
   - La distancia total en kilometros.

**Ejemplo de resultado:**

```
Distancia: 127 km
Guatemala > Antigua > Escuintla > Mazatenango
```

El boton **Limpiar** resetea la seleccion y el resultado.

---

### 4.2. Todas las rutas

Esta seccion muestra todas las rutas posibles entre dos ciudades, ordenadas de menor a mayor distancia.

**Pasos:**

1. Ir a la pestana **Todas las Rutas**.
2. Seleccionar ciudad de origen y ciudad de destino.
3. Presionar **Obtener Todas las Rutas**.
4. Se muestra una tabla con:
   - Numero de la ruta.
   - Secuencia de ciudades.
   - Distancia total.
   - La primera fila esta marcada como **Optima** (la mas corta).

**Ejemplo de tabla:**

| # | Ruta | Distancia |
|---|---|---|
| 1 | Guatemala > Antigua > Escuintla > Mazatenango (Optima) | 127 km |
| 2 | Guatemala > Escuintla > Mazatenango | 148 km |
| 3 | Guatemala > Chimaltenango > Quetzaltenango > Mazatenango | 246 km |

---

### 4.3. Administrar ciudades y conexiones

Esta seccion permite agregar nuevas ciudades y rutas al sistema sin reiniciar la aplicacion.

**Agregar una nueva conexion:**

1. Ir a la pestana **Administrar**.
2. Ingresar el nombre de la Ciudad 1 y Ciudad 2.
3. Ingresar la distancia en kilometros (numero entero positivo).
4. Presionar **Agregar Conexion**.
5. Si la operacion es exitosa, aparece un mensaje de confirmacion.

> Los nombres se normalizan automaticamente: se convierten a minusculas y los espacios se reemplazan por guion bajo. Por ejemplo, "San Marcos" se almacena como "san_marcos".

**Ver ciudades y conexiones:**

- La seccion **Ciudades Registradas** muestra todas las ciudades en la base de conocimiento.
- La seccion **Conexiones Registradas** muestra todas las rutas directas disponibles con sus distancias.

---

## 5. Ciudades disponibles

El sistema incluye de base las siguientes ciudades de Guatemala:

| Ciudad | Abreviatura interna |
|---|---|
| Guatemala | guatemala |
| Antigua Guatemala | antigua |
| Escuintla | escuintla |
| Chimaltenango | chimaltenango |
| Quetzaltenango | quetzaltenango |
| Mazatenango | mazatenango |
| Huehuetenango | huehuetenango |
| Coban | coban |
| Zacapa | zacapa |
| Jalapa | jalapa |
| Puerto Barrios | puerto_barrios |
| Flores | flores |

---

## 6. Mensajes del sistema

| Mensaje | Causa | Solucion |
|---|---|---|
| "Debe seleccionar origen y destino." | No se seleccionaron ambas ciudades. | Seleccionar ambas ciudades antes de buscar. |
| "La ciudad de origen no existe en la base de conocimiento." | La ciudad ingresada no esta registrada. | Revisar el nombre o agregarla en la pestana Administrar. |
| "No existe ruta entre X y Y." | Las ciudades no estan conectadas en el grafo. | Agregar conexiones intermedias desde la pestana Administrar. |
| "La distancia debe ser un numero mayor a 0." | Distancia invalida al agregar conexion. | Ingresar un valor numerico positivo. |
| "Error de conexion con el servidor." | El backend no esta activo. | Verificar que uvicorn este corriendo en el puerto 8000. |

---

## 7. Preguntas frecuentes

**La aplicacion no carga las ciudades al abrir el frontend.**
Verifica que el backend este activo ejecutando `python -m uvicorn main:app --reload` dentro de la carpeta `backend`.

**Instale SWI-Prolog pero PySwip no lo encuentra.**
El sistema detecta automaticamente SWI-Prolog si el ejecutable `swipl` esta en el PATH. Verifica ejecutando `swipl --version` en la terminal. Si no responde, reinstala SWI-Prolog marcando "Add SWI-Prolog to PATH" y reinicia la terminal.

**Quiero agregar muchas ciudades a la vez.**
Actualmente se agregan de una en una desde la interfaz. Tambien puedes editar directamente el archivo `prolog/ciudades.pl` y agregar hechos `conexion/3` antes de iniciar el backend.

**Las rutas agregadas desaparecen al reiniciar el servidor.**
Las conexiones nuevas se almacenan en memoria en la sesion actual de Prolog. Para persistirlas, agregarlas directamente al archivo `prolog/ciudades.pl`.
