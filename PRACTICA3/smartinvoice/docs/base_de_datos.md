# Esquema de Base de Datos - SmartInvoice

## Motor de base de datos

PostgreSQL 15

## Tablas

### usuarios

Almacena los usuarios del sistema con autenticacion.

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| id | INTEGER PK | Identificador unico |
| username | VARCHAR(100) UNIQUE | Nombre de usuario para login |
| email | VARCHAR(200) UNIQUE | Correo electronico |
| password_hash | VARCHAR(255) | Hash bcrypt de la contrasena |
| rol | VARCHAR(50) | Rol del usuario: admin o usuario |
| fecha_creacion | TIMESTAMP | Fecha y hora de registro |
| activo | BOOLEAN | Estado de la cuenta |

### proveedores

Catalogo de proveedores de facturas.

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| id | INTEGER PK | Identificador unico |
| nombre | VARCHAR(200) | Razon social del proveedor |
| nit | VARCHAR(20) UNIQUE | Numero de Identificacion Tributaria |
| direccion | VARCHAR(300) | Direccion fiscal |
| email | VARCHAR(200) | Correo de contacto |
| telefono | VARCHAR(30) | Telefono de contacto |
| fecha_creacion | TIMESTAMP | Fecha de registro |
| activo | BOOLEAN | Estado (borrado logico) |

### facturas

Registro de facturas procesadas por el sistema.

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| id | INTEGER PK | Identificador unico |
| numero_factura | VARCHAR(50) | Numero extraido por OCR |
| fecha_factura | VARCHAR(20) | Fecha de la factura (DD/MM/YYYY) |
| proveedor_id | INTEGER FK | Referencia a proveedores (nullable) |
| proveedor_nombre | VARCHAR(200) | Nombre del proveedor extraido |
| proveedor_nit | VARCHAR(20) | NIT extraido por OCR |
| subtotal | FLOAT | Monto subtotal |
| impuesto | FLOAT | Monto de IVA |
| total | FLOAT | Total de la factura |
| archivo_nombre | VARCHAR(300) | Nombre original del archivo |
| archivo_ruta | VARCHAR(500) | Ruta en disco del archivo guardado |
| estado | VARCHAR(20) | Procesado / Pendiente / Error / Rechazado |
| fecha_carga | TIMESTAMP | Cuando se subio al sistema |
| usuario_id | INTEGER FK | Usuario que cargo la factura |
| texto_extraido | TEXT | Texto completo obtenido por OCR |
| errores_validacion | TEXT | Descripcion de errores si estado=Rechazado |
| rpa_ejecutado | BOOLEAN | Si se ejecuto la automatizacion RPA |
| rpa_captura | VARCHAR(500) | Ruta de la captura de pantalla RPA |

### items_factura

Lineas de detalle de cada factura.

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| id | INTEGER PK | Identificador unico |
| factura_id | INTEGER FK | Referencia a facturas |
| descripcion | VARCHAR(300) | Descripcion del item |
| cantidad | FLOAT | Cantidad |
| precio_unitario | FLOAT | Precio por unidad |
| total | FLOAT | Total del item |

### bitacora

Historial de todas las operaciones realizadas en el sistema.

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| id | INTEGER PK | Identificador unico |
| fecha_hora | TIMESTAMP | Momento del evento |
| usuario_id | INTEGER FK | Usuario que ejecuto la accion |
| documento_nombre | VARCHAR(300) | Nombre del documento procesado |
| estado | VARCHAR(50) | Estado resultante de la operacion |
| resultado | VARCHAR(500) | Resumen del resultado |
| detalles | TEXT | Informacion detallada del procesamiento |

### reportes

Registro de reportes administrativos generados.

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| id | INTEGER PK | Identificador unico |
| nombre | VARCHAR(300) | Nombre descriptivo del reporte |
| formato | VARCHAR(10) | pdf / excel / csv |
| ruta_archivo | VARCHAR(500) | Ruta del archivo generado en disco |
| fecha_generacion | TIMESTAMP | Cuando se genero el reporte |
| usuario_id | INTEGER FK | Usuario que solicito el reporte |

## Diagrama de relaciones

```
usuarios ----< facturas >---- proveedores
    |               |
    |               +----< items_factura
    |
    +----------< bitacora
    +----------< reportes
```
