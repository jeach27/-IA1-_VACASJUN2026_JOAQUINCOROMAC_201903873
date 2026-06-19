# Requerimientos No Funcionales - SmartInvoice

## RNF-01 Rendimiento
- El procesamiento OCR de una factura no debe exceder los 30 segundos en condiciones normales.
- La API REST debe responder en menos de 500ms para endpoints que no involucren OCR.
- La base de datos debe soportar al menos 1000 facturas sin degradacion de rendimiento.

## RNF-02 Seguridad
- Las contrasenas se almacenan con hash bcrypt (costo minimo 12).
- Todos los endpoints protegidos requieren token JWT valido.
- El token expira en 8 horas por defecto.
- Las credenciales SMTP no se exponen en los logs.
- El directorio `.env` no se sube al repositorio.

## RNF-03 Disponibilidad
- El sistema debe estar disponible 99% del tiempo en entornos de produccion.
- Docker Compose configura `restart: always` para reinicio automatico de contenedores.
- PostgreSQL usa healthcheck para garantizar que el backend no inicie antes de que la base de datos este lista.

## RNF-04 Mantenibilidad
- El codigo esta organizado por modulos independientes (auth, facturas, proveedores, etc.).
- Cada modulo tiene sus propios schemas Pydantic y router.
- Las migraciones de base de datos se manejan con Alembic para permitir evolucionar el esquema sin perdida de datos.
- El codigo no usa comentarios superfluos; los nombres de funciones y variables son descriptivos.

## RNF-05 Portabilidad
- El sistema se ejecuta completamente mediante Docker Compose sin dependencias de sistema operativo especificas.
- La imagen base `python:3.11-slim` garantiza compatibilidad entre Linux, macOS y Windows.

## RNF-06 Usabilidad
- La interfaz web funciona en navegadores modernos (Chrome, Firefox, Edge).
- La interfaz no usa emojis ni iconos; todos los elementos tienen texto descriptivo.
- Los mensajes de error son claros y orientados al usuario final.
- El formulario de carga de facturas muestra inmediatamente el resultado del procesamiento OCR.

## RNF-07 Escalabilidad
- La arquitectura permite escalar el backend horizontalmente agregando mas instancias.
- El almacenamiento de archivos (uploads, reports, screenshots) usa volumenes Docker que pueden montarse en almacenamiento compartido.
