# Manual Tecnico - SmartInvoice

## 1. Descripcion general

SmartInvoice es un sistema de procesamiento inteligente de facturas que integra Computer Vision, OCR y automatizacion RPA para automatizar el ciclo completo de procesamiento: carga, extraccion, validacion, almacenamiento, generacion de reportes y notificacion por correo electronico.

## 2. Arquitectura del sistema

```
+------------------+       HTTP        +------------------+
|   Frontend       | <---------------> |   Backend        |
|   (nginx)        |    REST API       |   (FastAPI)      |
|   :8080          |                   |   :8000          |
+------------------+                   +--------+---------+
                                                |
                              +-----------------+------------------+
                              |                 |                  |
                    +---------+---+   +---------+---+   +---------+---+
                    | PostgreSQL  |   | Modulo OCR  |   | Modulo RPA  |
                    | :5432       |   | EasyOCR     |   | Playwright  |
                    +-------------+   | OpenCV      |   +-------------+
                                      +-------------+
```

### Patron de arquitectura

El sistema utiliza una arquitectura de tres capas con separacion por modulos:

- **Capa de presentacion:** Frontend HTML/CSS/JS vanilla servido por nginx.
- **Capa de logica de negocio:** Backend FastAPI con modulos independientes por dominio (auth, proveedores, facturas, bitacora, reportes, OCR, RPA, correo).
- **Capa de datos:** PostgreSQL con SQLAlchemy como ORM y Alembic para migraciones.

La comunicacion entre el frontend y el backend ocurre a traves de una API REST con autenticacion JWT. El nginx actua como proxy inverso, redirigiendo `/api/` al backend.

## 3. Componentes del sistema

### 3.1 Backend (Python/FastAPI)

| Modulo | Responsabilidad |
|--------|-----------------|
| `auth/` | Autenticacion JWT, login, registro, verificacion de tokens |
| `proveedores/` | CRUD de proveedores con borrado logico |
| `facturas/` | Carga de archivos, disparador de OCR, gestion de estados |
| `bitacora/` | Registro historico de todas las operaciones |
| `reportes/` | Generacion de PDF/Excel/CSV y envio por correo |
| `ocr/` | Pipeline de Computer Vision y extraccion de texto |
| `rpa/` | Automatizacion con Playwright para formularios web |
| `correo/` | Envio de correos via SMTP con archivos adjuntos |
| `database.py` | Configuracion de la conexion SQLAlchemy |
| `models.py` | Modelos de la base de datos |
| `main.py` | Punto de entrada FastAPI, registro de routers, startup |

### 3.2 Modulo OCR y Computer Vision

El modulo OCR implementa un pipeline de tres etapas:

**Etapa 1 - Preprocesamiento (vision.py):**
1. Carga de imagen: soporte para JPG, PNG y PDF (via pdf2image y poppler).
2. Escalado: ampliacion al 150% para mejorar precision del OCR.
3. Conversion a escala de grises con `cv2.cvtColor`.
4. Reduccion de ruido con filtro mediano `cv2.medianBlur`.
5. Umbralizado adaptativo gaussiano `cv2.adaptiveThreshold` para binarizar el texto.

**Etapa 2 - Reconocimiento (procesador.py):**
- EasyOCR con soporte de idiomas espanol e ingles.
- Extraccion con coordenadas bbox y nivel de confianza por segmento.
- Ordenamiento de bloques por posicion vertical (Y) para reconstruir el orden de lectura.

**Etapa 3 - Extraccion de campos (extractor.py):**
- Numero de factura: patron regex `FAC-XXXXX` o `No. Factura: XXXX`.
- Fecha: patron `DD/MM/YYYY` con prioridad a lineas con la palabra "Fecha".
- Proveedor: linea siguiente a "Proveedor:" o "Empresa:".
- NIT: patron `NIT: XXXXXXXXX`.
- Subtotal, IVA, Total: busqueda de patrones con montos numericos.
- Validacion de montos: verificacion de que `subtotal + IVA = total` con tolerancia de Q1.00.

### 3.3 Modulo RPA

Implementado con Playwright en modo headless (Chromium). El flujo es:
1. Apertura del formulario `formulario_registro.html` en el navegador.
2. Relleno automatico de cada campo con `page.fill()`.
3. Envio del formulario con `page.click()`.
4. Captura de pantalla como evidencia con `page.screenshot()`.
5. Las capturas se guardan en `/app/screenshots/`.

### 3.4 Modulo de Reportes

| Formato | Libreria | Contenido |
|---------|----------|-----------|
| PDF | ReportLab | Tabla con todas las facturas, totales y fecha de generacion |
| Excel | openpyxl | Hoja con encabezados estilizados, datos y fila de totales |
| CSV | stdlib csv | Filas planas con todos los campos |

### 3.5 Frontend

Implementado con HTML, CSS y JavaScript vanilla sin dependencias externas.

| Pagina | Ruta | Funcion |
|--------|------|---------|
| Login | `/index.html` | Autenticacion de usuario |
| Dashboard | `/dashboard.html` | Estadisticas y ultimas facturas |
| Facturas | `/facturas.html` | Carga OCR y gestion de facturas |
| Proveedores | `/proveedores.html` | CRUD de proveedores |
| Bitacora | `/bitacora.html` | Historial con filtros |
| Reportes | `/reportes.html` | Generacion y envio de reportes |
| Formulario RPA | `/formulario_registro.html` | Sistema simulado para RPA |

## 4. API REST

Ver documentacion completa en `docs/api_rest.md` y en `/docs` (Swagger UI).

## 5. Base de datos

Ver esquema completo en `docs/base_de_datos.md`.

## 6. Tecnologias utilizadas

| Tecnologia | Version | Uso |
|------------|---------|-----|
| Python | 3.11 | Backend, OCR, RPA, reportes |
| FastAPI | 0.111 | Framework REST |
| SQLAlchemy | 2.0 | ORM |
| Alembic | 1.13 | Migraciones |
| PostgreSQL | 15 | Base de datos |
| EasyOCR | 1.7.1 | Reconocimiento de texto |
| OpenCV | 4.9 | Preprocesamiento de imagenes |
| Playwright | 1.44 | Automatizacion RPA |
| ReportLab | 4.2 | Generacion de PDF |
| openpyxl | 3.1 | Generacion de Excel |
| python-jose | 3.3 | Tokens JWT |
| passlib/bcrypt | 1.7 / 4.1 | Hash de contrasenas |
| Docker | 24+ | Contenedorizacion |
| Docker Compose | 2+ | Orquestacion |
| nginx | alpine | Servidor web y proxy reverso |

## 7. Despliegue

Ver `docs/despliegue.md` para instrucciones completas de despliegue en la nube.

## 8. Posibles mejoras futuras

1. **Dashboard con graficas:** Integrar Chart.js para visualizacion de estadisticas de procesamiento por periodo.
2. **Procesamiento en cola:** Implementar Celery con Redis para procesar facturas en segundo plano sin bloquear la API.
3. **Deteccion de duplicados:** Comparar numero de factura + NIT para detectar facturas ya procesadas.
4. **Clasificacion automatica:** Usar ML para categorizar facturas por tipo de gasto.
5. **Mejora del OCR:** Entrenar modelos especificos para facturas guatemaltecas.
6. **Exportacion masiva:** Permitir descargar todas las facturas en ZIP.
7. **Notificaciones en tiempo real:** WebSockets para notificar el progreso del OCR.
8. **Roles granulares:** Sistema de permisos mas detallado por modulo.
9. **Procesamiento masivo:** Endpoint para subir y procesar multiples facturas a la vez.
10. **Integracion SAT:** Validacion del NIT contra el servicio del SAT de Guatemala.
