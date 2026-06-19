# Instalacion y Ejecucion - SmartInvoice

## Requisitos previos

- Docker 24.x o superior
- Docker Compose 2.x o superior
- Git

## Clonar el repositorio

```bash
git clone <URL_REPOSITORIO>
cd smartinvoice
```

## Configurar variables de entorno

```bash
cp backend/.env.example backend/.env
```

Editar `backend/.env` con los valores reales:

| Variable | Descripcion | Ejemplo |
|----------|-------------|---------|
| DATABASE_URL | URL de conexion PostgreSQL | postgresql://user:pass@db:5432/smartinvoice |
| SECRET_KEY | Clave secreta para JWT | cadena aleatoria de 32+ caracteres |
| ALGORITHM | Algoritmo JWT | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Minutos de validez del token | 480 |
| SMTP_HOST | Servidor SMTP | smtp.gmail.com |
| SMTP_PORT | Puerto SMTP | 587 |
| SMTP_USER | Correo electronico remitente | usuario@gmail.com |
| SMTP_PASSWORD | Contrasena SMTP o App Password | contrasena |
| UPLOAD_DIR | Directorio de facturas subidas | /app/uploads |
| REPORTS_DIR | Directorio de reportes generados | /app/reports |
| SCREENSHOTS_DIR | Directorio de capturas RPA | /app/screenshots |

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

Esperar a que todos los servicios inicien. El backend ejecuta las migraciones automaticamente al arrancar.

## Acceso al sistema

| Servicio | URL |
|----------|-----|
| Frontend web | http://localhost:8080 |
| API REST | http://localhost:8000 |
| Documentacion API (Swagger) | http://localhost:8000/docs |
| Base de datos PostgreSQL | localhost:5432 |

## Usuario inicial

Al primer arranque se crea automaticamente el usuario administrador:

- **Usuario:** admin
- **Contrasena:** admin123

Se recomienda cambiar la contrasena al primer inicio de sesion.

## Detener los servicios

```bash
docker compose down
```

Para eliminar tambien los volumenes de datos:

```bash
docker compose down -v
```

## Reconstruir sin cache

```bash
docker compose build --no-cache
docker compose up
```