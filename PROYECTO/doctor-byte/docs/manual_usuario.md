# Manual de Usuario - Doctor Byte

---

## Requisitos previos

Antes de ejecutar el sistema, se deben tener instalados los siguientes programas:

| Programa | Version minima | Descarga |
|---|---|---|
| Python | 3.10 | https://www.python.org/downloads/ |
| SWI-Prolog | 9.0 | https://www.swi-prolog.org/Download.html |
| Git | cualquiera | https://git-scm.com/ |

---

## 1. Instalacion

### Paso 1 - Clonar el repositorio

```bash
git clone https://github.com/USUARIO/REPO.git
cd REPO/doctor-byte
```

### Paso 2 - Instalar dependencias Python

```bash
cd backend
pip install -r requirements.txt
```

### Paso 3 - Configurar variables de entorno

Copiar el archivo de ejemplo y editarlo con los valores reales:

```bash
cp .env.example .env
```

Abrir `.env` y completar:

```
TELEGRAM_TOKEN=tu_token_aqui
```

Si no se usara Telegram, dejar el archivo como esta. El sistema funcionara sin notificaciones.

### Paso 4 - Verificar SWI-Prolog en el PATH

Ejecutar en la terminal:

```bash
swipl --version
```

Si el comando no se reconoce, agregar SWI-Prolog al PATH del sistema o reinstalarlo marcando la opcion correspondiente.

En Windows, la ruta tipica es: `C:\Program Files\swipl\bin`

---

## 2. Ejecucion del sistema

### Iniciar el servidor

Desde la carpeta `backend/`:

```bash
python app.py
```

Se vera en la terminal:

```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Abrir la interfaz

Abrir un navegador web (Chrome, Edge o Firefox) e ingresar:

```
http://localhost:5000
```

---

## 3. Uso de la interfaz

### Seleccionar sintomas

La interfaz muestra una cuadricula con todos los sintomas disponibles. Hacer clic en uno o mas sintomas para seleccionarlos. Los items seleccionados se resaltan en azul.

Los sintomas disponibles son:

- Pantalla negra
- Reinicio inesperado
- Lentitud extrema
- El equipo no enciende
- Sonidos de pitidos al arranque
- Sobrecalentamiento
- Pantalla azul de la muerte (BSOD)
- No reconoce el disco duro
- Las aplicaciones se cierran solas
- Sin sonido
- La red no conecta
- El teclado no responde
- El mouse no responde
- La bateria no carga
- Ventilador muy ruidoso

### Configurar notificacion de Telegram (opcional)

Si se desea recibir el resultado por Telegram, ingresar el Chat ID en el campo correspondiente.

Para obtener el Chat ID:
1. Abrir Telegram.
2. Buscar el bot @userinfobot.
3. Enviarle cualquier mensaje.
4. Copiar el numero que aparece en la respuesta (campo "Id:").

### Solicitar el diagnostico

Hacer clic en el boton **Diagnosticar**. El sistema procesara los sintomas y mostrara:

- La o las fallas detectadas.
- La recomendacion de accion para cada falla.

Si no se encuentra ninguna falla para la combinacion de sintomas indicada, se mostrara un mensaje sugiriendo consultar a un tecnico.

### Ver el historial

En la parte inferior de la pagina se muestra el historial de todos los diagnosticos realizados. Cada entrada muestra el id, la fecha, los sintomas y las fallas detectadas. Hacer clic en **Actualizar** para refrescar el historial sin recargar la pagina.

### Limpiar la seleccion

Hacer clic en **Limpiar seleccion** para desmarcar todos los sintomas y ocultar el panel de resultado.

---

## 4. Verificar la base de conocimiento en SWI-Prolog

Para probar la base de conocimiento directamente:

```bash
swipl prolog/knowledge_base.pl
```

Consultas de ejemplo en la consola:

```prolog
% Listar todos los sintomas
?- listar_sintomas(S).

% Diagnosticar pantalla negra y equipo que no enciende
?- obtener_diagnosticos([pantalla_negra, no_enciende], D).

% Obtener recomendacion de una falla
?- recomendacion(falla_fuente_poder, R).

% Ejecutar todos los casos de prueba
?- consult('prolog/tests.pl'), ejecutar_todas_las_pruebas.
```

---

## 5. Probar los endpoints directamente

Con curl desde la terminal:

```bash
# Obtener lista de sintomas
curl http://localhost:5000/sintomas

# Enviar diagnostico
curl -X POST http://localhost:5000/diagnostico \
  -H "Content-Type: application/json" \
  -d '{"sintomas": ["pantalla_negra", "no_enciende"]}'

# Ver historial
curl http://localhost:5000/historial
```

---

## 6. Solucion de problemas comunes

| Problema | Causa probable | Solucion |
|---|---|---|
| Error "SWI-Prolog not found" | SWI-Prolog no esta en el PATH | Agregar el directorio bin de SWI-Prolog al PATH del sistema |
| Error al importar pyswip | pyswip no instalado o incompatible | Ejecutar `pip install pyswip==0.2.10` |
| Pagina no carga en el navegador | El servidor Flask no esta corriendo | Verificar que `python app.py` este activo |
| Telegram no envia mensajes | TELEGRAM_TOKEN no configurado | Completar el archivo `.env` con el token real |
| Sin diagnostico para los sintomas | Combinacion no cubierta por las reglas | Agregar mas sintomas o consultar directamente en SWI-Prolog |
