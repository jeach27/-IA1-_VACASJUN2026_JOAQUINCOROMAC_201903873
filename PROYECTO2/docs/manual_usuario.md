# Manual de Usuario - Smart Warehouse

---

## 1. Requisitos Previos

Antes de ejecutar el sistema, verificar que lo siguiente este instalado:

| Requisito | Version Minima | Verificacion |
|---|---|---|
| Python | 3.11 | `python --version` |
| SWI-Prolog | 9.x | `swipl --version` |
| pip | 23.x | `pip --version` |
| Navegador moderno | Chrome 110+ / Firefox 110+ / Edge 110+ | - |

### Instalacion de SWI-Prolog

Descargar e instalar desde: https://www.swi-prolog.org/download/stable

Durante la instalacion en Windows, marcar la opcion para agregar SWI-Prolog al PATH del sistema. Verificar con:

```
swipl --version
```

---

## 2. Instalacion del Proyecto

### Paso 1: Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>/PROYECTO2
```

### Paso 2: Instalar dependencias Python

```bash
cd backend
pip install -r requirements.txt
```

Dependencias que se instalaran:
- `flask` - servidor web
- `flask-cors` - soporte para peticiones desde el frontend
- `pyswip` - integracion con SWI-Prolog

---

## 3. Ejecucion del Sistema

### Paso 1: Iniciar el backend

Desde la carpeta `PROYECTO2/backend`:

```bash
python app.py
```

El servidor iniciara en `http://localhost:5000`. La salida esperada es:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Dejar esta terminal abierta mientras se usa el sistema.

### Paso 2: Abrir el frontend

Abrir el archivo `PROYECTO2/frontend/index.html` directamente en el navegador.

En Windows se puede hacer doble clic sobre el archivo o arrastrar el archivo al navegador.

Al cargar, el mapa aparece con el estado inicial de la bodega.

---

## 4. Uso del Sistema

### Vista General de la Interfaz

```
+-------------------------------------------------------+
| Smart Warehouse                                       |
+-------------------------------------------------------+
| [Iniciar] [Paso a Paso] [Pausar] [Reiniciar]         |
| Modo: (x) Automatico ( ) Paso a Paso  Velocidad: 600 |
+------------------------------+------------------------+
|                              |  Estadisticas          |
|   MAPA DE LA BODEGA (10x10)  |  Registro de Acciones  |
|                              |  Estado de Robots      |
+------------------------------+------------------------+
|  Historial de Simulaciones                            |
+-------------------------------------------------------+
```

### Leyenda del Mapa

| Simbolo | Color | Significado |
|---|---|---|
| R | Azul | Robot sin carga |
| R+P | Azul claro | Robot cargando un paquete |
| P1..P5 | Verde | Paquete disponible para recoger |
| E | Amarillo | Zona de entrega |
| X | Rojo oscuro | Obstaculo (no transitable) |
| . | Gris oscuro | Casilla vacia |

---

### 4.1 Iniciar una Simulacion

1. Verificar que el backend este corriendo en el puerto 5000.
2. Hacer clic en el boton **Iniciar**.
3. El mapa se actualiza con el estado inicial cargado desde Prolog.
4. Si el modo es **Automatico**, la simulacion comienza a ejecutarse sola.
5. Si el modo es **Paso a Paso**, el boton **Paso a Paso** se habilita para avanzar manualmente.

---

### 4.2 Modo Automatico

En modo automatico el sistema ejecuta un paso cada N milisegundos segun el valor del campo **Velocidad**.

- Velocidad baja (100-300 ms): la simulacion avanza rapidamente.
- Velocidad alta (1000-3000 ms): la simulacion avanza lentamente, util para observar el comportamiento.

Para cambiar la velocidad durante la simulacion: modificar el campo **Velocidad (ms)** y la siguiente iteracion tomara el nuevo valor.

---

### 4.3 Modo Paso a Paso

1. Seleccionar la opcion **Paso a Paso** antes o durante una simulacion.
2. Hacer clic en el boton **Paso a Paso** para avanzar un paso.
3. Cada clic ejecuta exactamente una accion por robot.
4. El mapa, el registro de acciones y las estadisticas se actualizan despues de cada paso.

---

### 4.4 Pausar y Reanudar

- Hacer clic en **Pausar** para detener la ejecucion automatica sin perder el estado.
- El boton cambia su texto a **Reanudar**.
- Hacer clic en **Reanudar** para continuar desde donde se detuvo.

La pausa solo funciona en modo automatico. En modo paso a paso simplemente no se hace clic en el boton.

---

### 4.5 Reiniciar la Simulacion

Hacer clic en **Reiniciar** para volver al estado inicial:

- El robot regresa a su posicion de inicio (fila 1, columna 1).
- Todos los paquetes vuelven a sus posiciones originales.
- Las estadisticas se reinician a cero.
- El historial registra la simulacion anterior como "cancelada".

---

### 4.6 Estadisticas

El panel de estadisticas muestra en tiempo real:

| Campo | Descripcion |
|---|---|
| Movimientos | Numero total de pasos de movimiento ejecutados |
| Entregas | Cantidad de paquetes entregados en zonas correctas |
| Pendientes | Paquetes que aun no han sido entregados |
| Tiempo | Segundos transcurridos desde el inicio de la simulacion |
| Eficiencia | Porcentaje: (entregas / movimientos) * 100 |

---

### 4.7 Historial de Simulaciones

La tabla al final de la pagina muestra las simulaciones anteriores con:

- ID de la simulacion (primeros 8 caracteres)
- Fecha y hora de inicio
- Movimientos y entregas realizadas
- Tiempo total
- Resultado: `completada` (todos los paquetes entregados) o `cancelada` (reiniciada manualmente)

---

## 5. Solucion de Problemas Comunes

### El mapa no se renderiza al abrir el frontend

**Causa probable:** El backend no esta corriendo.

**Solucion:** Verificar que `python app.py` este ejecutandose en la carpeta `backend`. La consola debe mostrar el mensaje de Flask indicando que corre en el puerto 5000.

---

### Error "No se pudo conectar con el backend"

**Causa probable:** El backend no esta en el puerto 5000 o hay un firewall bloqueando la conexion.

**Solucion:**
1. Verificar que el backend este activo con `python app.py`.
2. Abrir `http://localhost:5000/api/mapa/inicial` en el navegador para confirmar que responde.
3. Si el puerto 5000 esta ocupado, cambiar el puerto en la ultima linea de `app.py` y actualizar la constante `API` en `app.js`.

---

### Error de conexion con Prolog al iniciar el backend

**Causa probable:** SWI-Prolog no esta instalado o no esta en el PATH del sistema.

**Solucion:**
1. Verificar con `swipl --version` en la terminal.
2. Si el comando no se reconoce, reinstalar SWI-Prolog marcando la opcion de agregar al PATH.
3. Reiniciar la terminal despues de la instalacion.

---

### El robot no se mueve o siempre ejecuta "esperar"

**Causa probable:** Un obstaculo bloquea todas las direcciones validas hacia el destino.

**Comportamiento esperado:** El robot ejecuta `esperar` hasta que se libere una ruta. En el mapa 10x10 incluido, todas las rutas tienen al menos un camino alternativo.

---

### pyswip no se instala correctamente

**Causa probable:** Version incompatible de Python o pip desactualizado.

**Solucion:**
```bash
pip install --upgrade pip
pip install pyswip==0.3.3
```

---

## 6. Ejecucion con Docker (opcional)

Docker empaqueta Python, SWI-Prolog y la aplicacion en un solo contenedor, eliminando la necesidad de instalar dependencias manualmente.

### Requisitos previos para Docker

- Docker Desktop instalado y en ejecucion
  - Windows/Mac: descargar desde https://www.docker.com/products/docker-desktop
  - Linux: instalar Docker Engine y Docker Compose

### Iniciar con Docker Compose

Desde la carpeta `PROYECTO2/`:

```bash
docker compose up --build
```

La primera vez descarga la imagen base e instala SWI-Prolog (puede tardar 2-5 minutos). Las siguientes ejecuciones usan la cache y son mas rapidas.

Al finalizar la construccion, el sistema estara disponible en:

- Frontend y API: `http://localhost:5000`

Para detener el sistema:

```bash
docker compose down
```

### Diferencias respecto a la ejecucion local

| Aspecto | Local | Docker |
|---|---|---|
| Frontend | Abrir index.html en el navegador | Abrir http://localhost:5000 |
| Backend | python app.py | docker compose up |
| SWI-Prolog | Instalacion manual requerida | Incluido en el contenedor |
| Dependencias Python | pip install -r requirements.txt | Incluidas en el contenedor |