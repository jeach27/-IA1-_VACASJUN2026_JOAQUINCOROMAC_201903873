# Manual de Usuario - SmartBot

## 1. Requisitos previos

Antes de ejecutar el proyecto asegurate de tener instalado:

- Docker Desktop (Windows/Mac) o Docker Engine + Docker Compose (Linux)
- Git
- Un token de bot de Telegram (obtenido desde @BotFather)

## 2. Instalacion y configuracion

### 2.1 Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd smartbot
```

### 2.2 Configurar variables de entorno

Copia el archivo de ejemplo y completa los valores:

```bash
cp .env.example .env
```

Edita el archivo `.env` con un editor de texto y reemplaza los valores:

```
POSTGRES_USER=smartbot_user
POSTGRES_PASSWORD=una_contrasena_segura
POSTGRES_DB=smartbot_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=una_clave_secreta_larga_y_aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

TELEGRAM_TOKEN=el_token_de_tu_bot_de_botfather
API_URL=http://backend:8000
```

### 2.3 Obtener el token de Telegram

1. Abre Telegram y busca el usuario `@BotFather`.
2. Escribe `/newbot` y sigue las instrucciones.
3. BotFather te entregara un token con el formato `123456789:ABC-DEF1234...`.
4. Copia ese token en el campo `TELEGRAM_TOKEN` del archivo `.env`.

## 3. Ejecucion

Levanta todos los servicios con un solo comando:

```bash
docker compose up -d
```

Para ver los logs en tiempo real:

```bash
docker compose logs -f
```

Para detener el proyecto:

```bash
docker compose down
```

## 4. Acceso al panel administrativo

Una vez levantado el proyecto, abre tu navegador y navega a:

```
http://localhost:8000/login.html
```

Usa las credenciales preconfiguradas:

- **Usuario**: `IA1-User`
- **Contrasena**: `IA1-password@_new`

## 5. Uso del panel administrativo

### 5.1 Estadisticas

Al iniciar sesion se muestra el panel de estadisticas con:

- Total de consultas realizadas al bot.
- Consultas con respuesta y sin respuesta.
- Usuarios unicos que han interactuado con el bot.
- Total de preguntas y categorias registradas.
- Ranking de las preguntas mas consultadas.

### 5.2 Gestion de categorias

1. Haz clic en **Categorias** en el menu lateral.
2. Para crear una categoria: haz clic en **Nueva categoria**, completa el nombre y descripcion, luego **Guardar**.
3. Para editar: haz clic en **Editar** en la fila correspondiente, modifica los datos y **Guardar**.
4. Para eliminar: haz clic en **Eliminar** y confirma la accion.

### 5.3 Gestion de preguntas y respuestas

1. Haz clic en **Preguntas** en el menu lateral.
2. Puedes filtrar las preguntas por categoria usando el selector.
3. Para crear: haz clic en **Nueva pregunta**, completa la pregunta, la respuesta y selecciona una categoria.
4. Activa o desactiva preguntas usando el checkbox **Activa** en el formulario de edicion.
5. El bot solo responde preguntas marcadas como activas.

### 5.4 Historial de consultas

En la seccion **Historial** puedes ver todas las consultas realizadas al bot con:

- Usuario de Telegram que realizo la consulta.
- Texto de la consulta enviada.
- Respuesta proporcionada.
- Si se encontro o no una respuesta.
- Fecha y hora de la consulta.

### 5.5 Configuracion del sistema

1. Haz clic en **Configuracion** en el menu lateral.
2. Al tope de la seccion veras la **tarjeta de estado del bot**:
   - Un indicador verde significa que el bot esta activo y responde mensajes.
   - Un indicador rojo significa que el bot esta inactivo.
   - Haz clic en **Desactivar bot** para suspender las respuestas temporalmente.
   - Haz clic en **Activar bot** para reanudar las respuestas.
   - El cambio toma efecto de inmediato en la proxima consulta de cualquier usuario.
3. Debajo puedes modificar los parametros del sistema:
   - `telegram_chat_id`: ID del grupo o chat donde el bot puede enviar mensajes proactivos.
   - `bot_nombre`: Nombre del bot mostrado en algunos mensajes.
   - `mensaje_no_encontrado`: Mensaje que el bot responde cuando no encuentra una respuesta.
4. Haz clic en **Guardar** junto a cada campo para aplicar el cambio.

## 6. Uso del bot de Telegram

1. Busca tu bot en Telegram por el nombre que le asignaste en BotFather.
2. Inicia una conversacion con `/start`.
3. Escribe tu pregunta en lenguaje natural. Por ejemplo: `cuales son los horarios de atencion?`
4. El bot buscara la pregunta mas similar en la base de datos y respondera automaticamente.
5. Si no encuentra una respuesta, recibiras el mensaje configurado en el panel administrativo.

### Comandos disponibles del bot

| Comando   | Descripcion                         |
|-----------|-------------------------------------|
| `/start`  | Mensaje de bienvenida               |
| `/ayuda`  | Informacion sobre como usar el bot  |

## 7. Solucion de problemas comunes

| Problema                              | Solucion                                                                 |
|---------------------------------------|--------------------------------------------------------------------------|
| El bot no responde                    | Verifica que `TELEGRAM_TOKEN` este correctamente configurado en `.env`   |
| Error de conexion a la base de datos  | Verifica que el servicio `db` este corriendo con `docker compose ps`     |
| No puedo acceder al panel             | Asegurate de que el puerto 8000 no este ocupado por otro proceso         |
| Las respuestas del bot son incorrectas| Revisa y actualiza las preguntas en el panel administrativo              |
