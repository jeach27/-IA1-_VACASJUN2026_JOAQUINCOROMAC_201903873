# Documentacion Frontend - SmartInvoice

## Acceso al sistema

URL: `http://localhost:8080`

## Paginas disponibles

### Login (`/index.html`)
Pagina de inicio de sesion. Requiere usuario y contrasena. Al autenticarse exitosamente redirige al dashboard. El token JWT se guarda en `localStorage`.

**Usuario inicial:** admin / admin123

### Dashboard (`/dashboard.html`)
Panel principal con:
- Contadores de facturas por estado (Total, Procesadas, Pendientes, Con Error, Rechazadas).
- Tabla de las ultimas 10 facturas procesadas con estado y fecha.
- Enlace para ir a cargar una nueva factura.

### Facturas (`/facturas.html`)
Modulo principal de carga y gestion:
- Formulario de carga de archivo (PDF, JPG, JPEG, PNG).
- Visualizacion inmediata de los datos extraidos por OCR.
- Tabla con todas las facturas, estado y acciones.
- Boton "Ver" abre modal con detalle completo incluyendo texto OCR.
- Boton "RPA" ejecuta la automatizacion Playwright para esa factura.

### Proveedores (`/proveedores.html`)
CRUD completo de proveedores:
- Lista de proveedores activos.
- Boton "Nuevo Proveedor" abre modal de creacion.
- Boton "Editar" carga datos del proveedor en el modal.
- Boton "Desactivar" realiza borrado logico con confirmacion.

### Bitacora (`/bitacora.html`)
Historial de operaciones del sistema:
- Tabla con todos los registros de la bitacora.
- Filtros por fecha inicio, fecha fin y estado.
- Actualizacion manual con boton "Actualizar".

### Reportes (`/reportes.html`)
Generacion y distribucion de reportes:
- Selector de formato: PDF, Excel o CSV.
- Boton "Generar Reporte" crea el reporte y lo muestra en la lista.
- Boton "Descargar" descarga el archivo directamente.
- Boton "Enviar" abre modal para ingresar correo destinatario y enviar el reporte adjunto.

### Formulario de Registro RPA (`/formulario_registro.html`)
Formulario web simple usado como sistema simulado por la automatizacion RPA.
No requiere autenticacion. Los campos son rellenados automaticamente por Playwright.

## Tecnologias del frontend

- HTML5 semantico
- CSS3 personalizado (sin frameworks)
- JavaScript ES6+ vanilla (sin jQuery ni React)
- Fetch API para comunicacion con el backend
- LocalStorage para persistencia del token JWT

## Estructura de archivos

```
frontend/
    index.html            Login
    dashboard.html        Panel principal
    facturas.html         Gestion de facturas
    proveedores.html      CRUD de proveedores
    bitacora.html         Historial
    reportes.html         Generacion y envio de reportes
    formulario_registro.html  Sistema simulado RPA
    css/
        estilos.css       Estilos globales del sistema
    js/
        api.js            Funciones base de comunicacion con la API
        auth.js           Login, logout, verificacion de sesion
        facturas.js       Logica de carga y gestion de facturas
        proveedores.js    Logica CRUD de proveedores
        bitacora.js       Carga y filtrado de bitacora
        reportes.js       Generacion, descarga y envio de reportes
```
