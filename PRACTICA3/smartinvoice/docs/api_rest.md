# Documentacion API REST - SmartInvoice

Base URL: `http://localhost:8000`

Todos los endpoints excepto `/auth/login` y `/auth/registro` requieren el header:
```
Authorization: Bearer <token_jwt>
```

## Autenticacion

### POST /auth/login
Inicia sesion y obtiene un token JWT.

**Body:**
```json
{ "username": "admin", "password": "admin123" }
```

**Respuesta exitosa (200):**
```json
{ "access_token": "eyJhbGc...", "token_type": "bearer" }
```

### POST /auth/registro
Registra un nuevo usuario en el sistema.

**Body:**
```json
{ "username": "usuario1", "email": "u1@ejemplo.com", "password": "clave123", "rol": "usuario" }
```

### GET /auth/me
Retorna los datos del usuario autenticado.

---

## Proveedores

### GET /proveedores/
Lista todos los proveedores activos.

### GET /proveedores/{id}
Obtiene un proveedor por ID.

### POST /proveedores/
Crea un nuevo proveedor.

**Body:**
```json
{ "nombre": "Empresa ABC", "nit": "12345678-9", "email": "abc@empresa.com", "telefono": "2222-3333" }
```

### PUT /proveedores/{id}
Actualiza un proveedor existente (campos opcionales).

### DELETE /proveedores/{id}
Desactiva un proveedor (borrado logico). Retorna 200 con mensaje de confirmacion.

---

## Facturas

### POST /facturas/cargar
Carga una factura y la procesa con OCR automaticamente.

**Content-Type:** `multipart/form-data`

**Campos:**
- `archivo`: archivo PDF, JPG, JPEG o PNG

**Respuesta:**
```json
{
    "factura": { "id": 1, "numero_factura": "FAC-00001", "estado": "Procesado", ... },
    "campos_extraidos": { "numero_factura": "FAC-00001", "subtotal": 100.0, ... },
    "mensaje": "Factura FAC-00001 procesada. Total: Q112.00"
}
```

### GET /facturas/
Lista todas las facturas ordenadas por fecha de carga descendente.

### GET /facturas/{id}
Obtiene el detalle completo de una factura incluyendo texto OCR e items.

### PUT /facturas/{id}/estado
Actualiza el estado de una factura.

**Body:**
```json
{ "estado": "Procesado" }
```

Estados validos: `Procesado`, `Pendiente`, `Error`, `Rechazado`

### GET /facturas/{id}/items
Lista los items de detalle de una factura.

### POST /facturas/{id}/rpa
Ejecuta la automatizacion RPA para una factura especifica.

---

## Bitacora

### GET /bitacora/
Lista el historial completo con filtros opcionales.

**Query params opcionales:**
- `fecha_inicio`: YYYY-MM-DD
- `fecha_fin`: YYYY-MM-DD
- `estado`: texto a buscar en el estado
- `usuario_id`: ID del usuario

### GET /bitacora/{id}
Obtiene el detalle de un registro de bitacora.

---

## Reportes

### POST /reportes/generar
Genera un reporte administrativo.

**Body:**
```json
{ "formato": "pdf" }
```

Formatos validos: `pdf`, `excel`, `csv`

### GET /reportes/
Lista todos los reportes generados.

### GET /reportes/{id}/descargar
Descarga el archivo del reporte. Retorna el archivo directamente.

### POST /reportes/{id}/enviar
Envia el reporte por correo electronico.

**Body:**
```json
{
    "destinatario": "correo@ejemplo.com",
    "asunto": "Reporte SmartInvoice",
    "mensaje": "Se adjunta el reporte."
}
```

---

## Endpoints de sistema

### GET /
Retorna informacion basica de la API y version.

### GET /health
Verifica el estado de la API y la conexion a la base de datos.
