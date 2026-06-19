# Modulo de Correo Electronico - SmartInvoice

## Descripcion

El modulo de correo permite enviar reportes administrativos por correo electronico de forma automatica usando smtplib con STARTTLS.

## Configuracion SMTP

Editar las siguientes variables en `backend/.env`:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=mi_correo@gmail.com
SMTP_PASSWORD=mi_contrasena_de_aplicacion
```

### Configuracion para Gmail

1. Activar verificacion en dos pasos en la cuenta de Google.
2. Ir a Seguridad > Contrasenas de aplicaciones.
3. Generar una contrasena de aplicacion para "Correo".
4. Usar esa contrasena generada en `SMTP_PASSWORD` (no la contrasena normal de Gmail).

### Otros proveedores SMTP

| Proveedor | SMTP_HOST | SMTP_PORT |
|-----------|-----------|-----------|
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp.office365.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 587 |
| SendGrid | smtp.sendgrid.net | 587 |

## Probar el envio

Desde la interfaz web:
1. Ir a la pagina de Reportes.
2. Generar un reporte en cualquier formato.
3. Hacer clic en "Enviar" junto al reporte.
4. Ingresar el correo del destinatario y hacer clic en "Enviar".

Desde la API:
```bash
curl -X POST http://localhost:8000/reportes/1/enviar \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"destinatario": "destino@ejemplo.com"}'
```

## Manejo de errores

El modulo detecta y reporta los siguientes errores:
- Credenciales SMTP incorrectas (SMTPAuthenticationError).
- Servidor SMTP inaccesible (SMTPException).
- Variables de entorno no configuradas.

Todos los intentos de envio se registran en la bitacora con estado "Enviado" o "Error envio".
