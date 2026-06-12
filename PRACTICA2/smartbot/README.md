# SmartBot

Sistema de respuestas automatizadas con bot de Telegram, API REST en Python (FastAPI) y panel administrativo web.

## Requisitos

- Docker Desktop o Docker Engine con Docker Compose
- Token de bot de Telegram (obtenido desde @BotFather)

## Instalacion rapida

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd smartbot

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con los valores reales (TELEGRAM_TOKEN obligatorio)

# 3. Levantar el proyecto
docker compose up -d
```

## Acceso

- **Panel administrativo**: http://localhost:8000/login.html
- **API REST**: http://localhost:8000
- **Documentacion de la API**: http://localhost:8000/docs

## Credenciales preconfiguradas

- **Usuario**: `IA1-User`
- **Contrasena**: `IA1-password@_new`

## Comandos utiles

```bash
# Ver logs de todos los servicios
docker compose logs -f

# Ver logs de un servicio especifico
docker compose logs -f backend
docker compose logs -f bot

# Detener el proyecto
docker compose down

# Detener y eliminar datos
docker compose down -v
```

## Documentacion

- [Arquitectura y API](docs/arquitectura.md)
- [Manual tecnico](docs/manual_tecnico.md)
- [Manual de usuario](docs/manual_usuario.md)
- [Casos de prueba](docs/casos_de_prueba.md)

## Estructura del proyecto

```
smartbot/
├── backend/          # API REST + bot de Telegram
├── admin/            # Panel administrativo web
├── db/               # Esquema inicial de la base de datos
├── docs/             # Documentacion
├── docker-compose.yml
└── .env.example
```
