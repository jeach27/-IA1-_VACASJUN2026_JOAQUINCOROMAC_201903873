# Modulo RPA - SmartInvoice

## Descripcion

El modulo RPA (Robotic Process Automation) automatiza el registro de informacion de facturas procesadas en un formulario web simulado, tomando capturas de pantalla como evidencia del proceso.

## Tecnologia

**Playwright** (version 1.44) con navegador Chromium en modo headless.

Se eligio Playwright sobre Selenium por su mejor soporte para paginas modernas, API mas simple y mayor estabilidad en entornos Docker headless.

## Flujo de automatizacion

1. Recepcion de datos de la factura (numero, fecha, proveedor, NIT, subtotal, IVA, total).
2. Inicializacion de Playwright en modo headless con `--no-sandbox` para Docker.
3. Navegacion al formulario en `http://frontend:80/formulario_registro.html`.
4. Relleno automatico de cada campo usando `page.fill(selector, valor)`.
5. Click en el boton de registro.
6. Espera de 800ms para que la pagina procese.
7. Captura de pantalla completa de la pagina.
8. Cierre del navegador y retorno del resultado.

## Como ejecutar

La automatizacion se ejecuta via el endpoint:
```
POST /facturas/{id}/rpa
```

Requiere que la factura exista en la base de datos y que el contenedor frontend este accesible.

## Como verificar la ejecucion

1. El campo `rpa_ejecutado` de la factura cambia a `true`.
2. La captura de pantalla se guarda en `/app/screenshots/rpa_{num_factura}_{timestamp}.png`.
3. Se registra en la bitacora con estado "RPA Ejecutado".
4. La ruta de la captura queda en el campo `rpa_captura` de la factura.

## Donde se guardan las capturas

En el volumen Docker `screenshots_data` montado en `/app/screenshots/` del contenedor backend.

El nombre del archivo sigue el patron: `rpa_{numero_factura}_{YYYYMMDD_HHMMSS}.png`

## Notas de configuracion

- La variable `FRONTEND_URL` en `.env` debe apuntar a la URL accesible del frontend desde el contenedor backend.
- En Docker Compose se usa `http://frontend:80` (nombre del servicio).
- En despliegue en nube, cambiar a la URL publica correspondiente.
