# Despliegue en la Nube - SmartInvoice

## Proveedor recomendado: Railway

Railway permite desplegar aplicaciones Docker Compose directamente con configuracion minima y ofrece plan gratuito suficiente para demostracion.

### Pasos para desplegar en Railway

1. Crear cuenta en railway.app.
2. Instalar Railway CLI:
   ```bash
   npm install -g @railway/cli
   railway login
   ```
3. Crear nuevo proyecto:
   ```bash
   railway init
   ```
4. Configurar variables de entorno en el dashboard de Railway (las mismas del `.env.example`).
5. Desplegar:
   ```bash
   railway up
   ```
6. Obtener URL publica desde el dashboard.

### Variables de entorno a configurar en Railway

```
DATABASE_URL=postgresql://...
SECRET_KEY=<clave-segura-32-chars>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=correo@gmail.com
SMTP_PASSWORD=<app-password>
UPLOAD_DIR=/app/uploads
REPORTS_DIR=/app/reports
SCREENSHOTS_DIR=/app/screenshots
FRONTEND_URL=https://<url-del-frontend>.railway.app
```

## Alternativa: Render

1. Crear cuenta en render.com.
2. Nuevo servicio > Docker.
3. Conectar el repositorio GitHub.
4. Configurar variables de entorno.
5. Deploy automatico en cada push a main.

## Verificacion del despliegue

Una vez desplegado, verificar el flujo completo:

1. Acceder a la URL publica del frontend.
2. Login con usuario `admin` y contrasena `admin123`.
3. Cargar una factura de prueba.
4. Verificar que el OCR extrae los datos correctamente.
5. Generar un reporte en formato PDF.
6. Enviar el reporte por correo electronico.
7. Verificar la bitacora.
8. Ejecutar RPA en al menos una factura.

## URL publica del sistema

*Pendiente de configurar. Actualizar este documento despues del despliegue.*

## Como actualizar el despliegue

```bash
git push origin main
```

El despliegue automatico se actualiza en Railway/Render al detectar cambios en el repositorio.
