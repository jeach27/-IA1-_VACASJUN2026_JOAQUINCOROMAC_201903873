# Arquitectura del Sistema - SmartBot

## 1. Descripcion general

SmartBot es un sistema de respuestas automatizadas compuesto por tres componentes principales que se comunican a traves de una API REST:

- **Bot de Telegram**: recibe mensajes de los usuarios y consulta la API para obtener respuestas.
- **API REST (FastAPI)**: nucleo del sistema; gestiona preguntas, respuestas, categorias, autenticacion y estadisticas.
- **Panel administrativo web**: interfaz HTML/CSS/JS que consume la API para la gestion de contenido.

Todos los componentes se ejecutan dentro de contenedores Docker orquestados con Docker Compose.

## 2. Patron de arquitectura

Se utiliza una arquitectura de **capas (Layered Architecture)** combinada con el patron **API Gateway**:

```
[Usuario Telegram]              [Administrador]
        |                              |
        v                             v
  [Bot Telegram]            [Panel Web (HTML/JS)]
        |                             |
        +-----------> [API REST] <----+
                           |
                    [Base de datos]
                     (PostgreSQL)
```

- La capa de presentacion incluye tanto el bot como el panel web.
- La capa de negocio reside completamente en la API REST.
- La capa de datos es PostgreSQL, accedida unicamente a traves de SQLAlchemy desde la API.

## 3. Stack tecnologico

| Componente         | Tecnologia                       |
|--------------------|----------------------------------|
| Backend / API REST | Python 3.11 + FastAPI            |
| Base de datos      | PostgreSQL 16                    |
| Bot                | python-telegram-bot 21           |
| Panel admin        | HTML5 + CSS3 + JavaScript        |
| Autenticacion      | JWT (python-jose + passlib/bcrypt)|
| Orquestacion       | Docker + Docker Compose          |
| Control de versiones | Git + GitHub                   |

## 4. Estructura del proyecto

```
smartbot/
├── backend/
│   ├── app/
│   │   ├── main.py            # Punto de entrada de la API (FastAPI)
│   │   ├── config.py          # Variables de entorno con pydantic-settings
│   │   ├── database.py        # Engine y sesion de SQLAlchemy
│   │   ├── models.py          # Modelos ORM
│   │   ├── schemas.py         # Esquemas Pydantic (request/response)
│   │   ├── auth.py            # JWT y dependencias de autenticacion
│   │   └── routers/
│   │       ├── categorias.py
│   │       ├── preguntas.py
│   │       ├── consultas.py
│   │       ├── configuracion.py
│   │       └── estadisticas.py
│   ├── bot/
│   │   └── telegram_bot.py    # Proceso del bot (consume la API)
│   ├── requirements.txt
│   └── Dockerfile
├── admin/                     # Panel web estatico
│   ├── login.html
│   ├── index.html
│   ├── css/styles.css
│   └── js/app.js
├── db/
│   └── init.sql               # Esquema + seed inicial
├── docs/
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## 5. Modelo de datos

### Entidades

| Entidad         | Descripcion                                               |
|-----------------|-----------------------------------------------------------|
| `categoria`     | Agrupa preguntas frecuentes por tema                      |
| `pregunta`      | Pregunta frecuente con su respuesta, asociada a categoria |
| `usuario_admin` | Usuarios con acceso al panel administrativo               |
| `consulta`      | Historial de cada consulta hecha desde Telegram           |
| `configuracion` | Parametros del sistema (chat ID, mensajes, etc.)          |

### Relaciones

- Una `categoria` agrupa muchas `pregunta` (1:N).
- Una `pregunta` puede tener muchas `consulta` asociadas (1:N).
- `configuracion` almacena pares clave-valor del sistema.

### Diagrama ER (descripcion textual)

```
categoria(id PK, nombre, descripcion, creado_en)
pregunta(id PK, texto, respuesta, categoria_id FK, activa, creado_en, actualizado_en)
usuario_admin(id PK, username, password_hash, creado_en)
consulta(id PK, telegram_user, telegram_user_id, texto_consulta, texto_respuesta, pregunta_id FK, encontrada, consultado_en)
configuracion(id PK, clave UNIQUE, valor, descripcion, actualizado_en)
```

## 6. API REST

### Autenticacion

| Metodo | Ruta          | Descripcion                                     | Auth |
|--------|---------------|-------------------------------------------------|------|
| POST   | /auth/login   | Recibe {username, password}, retorna JWT        | No   |

Request:
```json
{ "username": "IA1-User", "password": "IA1-password@_new" }
```
Response:
```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```

### Categorias

| Metodo | Ruta                   | Descripcion            | Auth |
|--------|------------------------|------------------------|------|
| GET    | /categorias            | Lista todas            | No   |
| POST   | /categorias            | Crea una categoria     | Si   |
| PUT    | /categorias/{id}       | Actualiza una categoria| Si   |
| DELETE | /categorias/{id}       | Elimina una categoria  | Si   |

### Preguntas

| Metodo | Ruta               | Descripcion                            | Auth |
|--------|--------------------|----------------------------------------|------|
| GET    | /preguntas         | Lista preguntas (filtro por categoria) | No   |
| POST   | /preguntas         | Crea pregunta con respuesta            | Si   |
| PUT    | /preguntas/{id}    | Actualiza pregunta o respuesta         | Si   |
| DELETE | /preguntas/{id}    | Elimina pregunta                       | Si   |

### Consulta del bot

| Metodo | Ruta       | Descripcion                                     | Auth |
|--------|------------|-------------------------------------------------|------|
| POST   | /consultar | Busca respuesta para el texto enviado por el bot| No   |
| GET    | /consultas | Historial de consultas                          | Si   |

Request /consultar:
```json
{ "texto": "cuales son los horarios?", "telegram_user": "pepe", "telegram_user_id": 12345 }
```
Response:
```json
{ "respuesta": "Atendemos de lunes a viernes...", "encontrada": true, "pregunta_id": 1 }
```

### Configuracion

| Metodo | Ruta                    | Descripcion                      | Auth |
|--------|-------------------------|----------------------------------|------|
| GET    | /configuracion          | Lista todas las configuraciones  | Si   |
| GET    | /configuracion/{clave}  | Obtiene una configuracion        | No   |
| PUT    | /configuracion/{clave}  | Actualiza una configuracion      | Si   |

### Estadisticas

| Metodo | Ruta           | Descripcion                      | Auth |
|--------|----------------|----------------------------------|------|
| GET    | /estadisticas  | Totales y rankings de consultas  | Si   |

## 7. Bot de Telegram

El bot se implementa con `python-telegram-bot` en modo polling. Flujo de una consulta:

1. El usuario envia un mensaje al bot en Telegram.
2. El handler `manejar_mensaje` captura el texto.
3. Se realiza un `POST /consultar` a la API con el texto y los datos del usuario.
4. La API busca la pregunta mas similar usando `difflib.SequenceMatcher` con un umbral de 0.45.
5. Si la similitud supera el umbral, retorna la respuesta; si no, retorna el mensaje de no encontrado.
6. La API registra la consulta en el historial.
7. El bot responde al usuario con el resultado.

El token del bot se lee exclusivamente desde la variable de entorno `TELEGRAM_TOKEN`.

## 8. Panel administrativo

El panel es una SPA estatica (HTML/CSS/JS vanilla) servida desde el mismo contenedor del backend.

- La autenticacion se realiza contra `POST /auth/login` y el token JWT se guarda en `sessionStorage`.
- Cada llamada a la API incluye el header `Authorization: Bearer <token>`.
- Si la API retorna 401, se redirige automaticamente a `login.html`.
- Las secciones disponibles son: Estadisticas, Categorias, Preguntas, Historial y Configuracion.

## 9. Docker Compose

El proyecto se levanta con tres servicios:

| Servicio  | Imagen base        | Puerto | Descripcion                              |
|-----------|--------------------|--------|------------------------------------------|
| db        | postgres:16-alpine | -      | Base de datos con carga del init.sql     |
| backend   | python:3.11-slim   | 8000   | API REST + panel admin estatico          |
| bot       | python:3.11-slim   | -      | Proceso del bot de Telegram              |

El servicio `backend` depende de `db` con health check. El servicio `bot` depende de `backend` y `db`.

Comando de arranque:
```bash
cp .env.example .env   # completar con valores reales
docker compose up -d
```
