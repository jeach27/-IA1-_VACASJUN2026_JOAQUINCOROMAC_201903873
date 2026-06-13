# Manual de Usuario - Doctor Byte

---

## Requisitos previos

| Programa | Version | Descarga |
|---|---|---|
| Python | 3.10 o superior | https://www.python.org/downloads/ |
| SWI-Prolog | 10.x | https://www.swi-prolog.org/Download.html |
| Git | cualquiera | https://git-scm.com/ |

---

## 1. Instalacion

### Paso 1 - Clonar el repositorio

```bash
git clone https://github.com/USUARIO/REPO.git
cd REPO/PROYECTO/doctor-byte
```

### Paso 2 - Configurar la variable de entorno de SWI-Prolog (Windows)

Abrir PowerShell y ejecutar una sola vez:

```powershell
# Encontrar la ruta de instalacion de SWI-Prolog
(Get-Command swipl).Source

# Configurar la variable (reemplazar la ruta con la encontrada arriba)
[System.Environment]::SetEnvironmentVariable("SWI_HOME_DIR", "D:\ruta\a\swipl", "User")
```

Cerrar y abrir la terminal para que el cambio surta efecto.

### Paso 3 - Crear el entorno virtual e instalar dependencias

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 4 - Configurar las variables de entorno del proyecto

Copiar el archivo de ejemplo:

```powershell
cd ..
copy .env.example .env
```

Abrir `.env` y completar con el token del bot de Telegram:

```
TELEGRAM_TOKEN=tu_token_aqui
```

Si no se usara Telegram, dejar el archivo como esta. El sistema funciona sin notificaciones.

---

## 2. Ejecucion del sistema

Desde la carpeta `backend/` con el venv activado:

```powershell
python app.py
```

Se vera en la terminal:

```
INFO telegram_bot: Hilo del bot de Telegram iniciado
 * Running on http://0.0.0.0:5000
INFO prolog_bridge: Base de conocimiento cargada desde ...knowledge_base.pl
```

---

## 3. Interfaz de usuario principal

Abrir en el navegador: `http://localhost:5000`

### Seleccionar sintomas

La pagina muestra una cuadricula con los 15 sintomas disponibles. Hacer clic en uno o mas para seleccionarlos (se resaltan en azul).

### Solicitar el diagnostico

Presionar **Diagnosticar**. El sistema consulta Prolog y muestra:
- La falla detectada
- La recomendacion de accion

Si no se encuentra ninguna falla, se indica que no hay resultado para esa combinacion.

### Limpiar y reiniciar

- **Limpiar seleccion**: desmarca todos los sintomas y oculta el resultado.
- **Nuevo diagnostico**: limpia todo y sube al inicio de la pagina.

### Historial

La seccion inferior muestra todos los diagnosticos anteriores con fecha, sintomas y fallas detectadas. Presionar **Actualizar** para refrescar sin recargar la pagina.

---

## 4. Panel de administracion

Acceder desde el enlace **Administracion** en el encabezado de la pagina principal, o directamente en: `http://localhost:5000/admin`

### Sintomas

Permite ver, agregar, editar y eliminar sintomas. Al guardar cualquier cambio, la base de conocimiento Prolog se regenera automaticamente.

- Los nombres de sintomas deben ser atomos Prolog validos: solo letras minusculas, digitos y guion bajo, comenzando con letra.
- Ejemplos validos: `pantalla_negra`, `sin_sonido2`
- Ejemplos invalidos: `Pantalla Negra`, `2sintoma`, `sintoma-feo`

### Fallas

Igual que sintomas. Cada falla puede tener una recomendacion asociada.

### Recomendaciones

Permite ver, agregar, editar y eliminar el texto de recomendacion de cada falla.

- **Agregar**: presionar el boton, seleccionar la falla del listado y escribir el texto.
- **Editar**: presionar Editar en la fila correspondiente y modificar el texto.
- **Eliminar**: presionar Eliminar en la fila correspondiente.

### Reglas de inferencia

Permite crear, editar y eliminar las reglas que Prolog usa para diagnosticar.

Cada regla tiene:
- **Falla**: la falla que se diagnostica si se cumple la regla
- **Sintomas requeridos**: TODOS deben estar presentes
- **Sintomas negados**: NINGUNO debe estar presente
- **Usar corte (!)**: evita que Prolog busque otras reglas cuando esta se cumple

Ejemplo: "Si hay pantalla negra Y no enciende Y NO hay sobrecalentamiento, entonces es falla de fuente de poder."

### Asociaciones

Vista de solo lectura que muestra como se relacionan los sintomas con las fallas y sus recomendaciones. Util para verificar la coherencia de la base de conocimiento.

### Bot Telegram

Permite configurar:
- **ID del chat de destino**: el numero de chat al que se envian las notificaciones automaticas
- **Bot habilitado**: activa o desactiva el envio sin necesidad de cambiar el codigo
- **Mensaje de bienvenida**: texto del comando /start del bot
- **Mensaje sin diagnostico**: texto cuando no se detectan fallas

---

## 5. Bot de Telegram

### Configurar el bot

1. Abrir Telegram y buscar **@BotFather**
2. Escribirle `/newbot`
3. Seguir las instrucciones para elegir nombre y username
4. Copiar el token y pegarlo en el archivo `.env` como `TELEGRAM_TOKEN=...`
5. Reiniciar el servidor

### Obtener el Chat ID

1. Buscar **@userinfobot** en Telegram
2. Escribirle cualquier mensaje
3. Copiar el numero del campo `Id:` en su respuesta
4. Pegarlo en el panel admin (seccion Bot Telegram, campo "ID del chat de destino")

### Comandos del bot

Una vez configurado, buscar el bot en Telegram por su username y escribir:

| Comando | Descripcion |
|---|---|
| /start | Muestra el mensaje de bienvenida |
| /sintomas | Lista los 15 sintomas disponibles |
| /diagnosticar s1,s2,... | Realiza un diagnostico |
| /ayuda | Muestra los comandos disponibles |

Ejemplo de uso:
```
/diagnosticar pantalla_negra,no_enciende
```

El bot responde con la falla detectada y la recomendacion.

---

## 6. Verificar la base de conocimiento en SWI-Prolog

```powershell
swipl prolog\knowledge_base.pl
```

Consultas de ejemplo:

```prolog
% Listar sintomas
?- listar_sintomas(S).

% Diagnosticar
?- obtener_diagnosticos([pantalla_negra, no_enciende], D).

% Obtener recomendacion
?- recomendacion(falla_fuente_poder, R).

% Salir
?- halt.
```

---

## 7. Probar los endpoints directamente

```powershell
# Lista de sintomas
curl http://localhost:5000/sintomas

# Diagnostico
curl -X POST http://localhost:5000/diagnostico `
  -H "Content-Type: application/json" `
  -d '{"sintomas": ["pantalla_negra", "no_enciende"]}'

# Historial
curl http://localhost:5000/historial

# Config del bot (admin)
curl http://localhost:5000/admin/configuracion
```

---

## 8. Solucion de problemas comunes

| Problema | Causa probable | Solucion |
|---|---|---|
| FATAL: could not find SWI-Prolog home | SWI_HOME_DIR no configurada | Ejecutar el comando de SetEnvironmentVariable y abrir terminal nueva |
| OSError: access violation | pyswip desactualizado | Ejecutar `pip install pyswip --upgrade` (version 0.3.3+) |
| Pagina no carga | Servidor Flask no activo | Verificar que `python app.py` este corriendo |
| GET /sintomas retorna 500 | Prolog no puede cargarse | Verificar SWI_HOME_DIR y que swipl este en PATH |
| Telegram no envia mensajes | Token no configurado o bot deshabilitado | Verificar .env y el panel admin seccion Bot Telegram |
| Sin diagnostico para los sintomas | Combinacion no cubierta por reglas | Agregar una regla nueva desde el panel admin |
