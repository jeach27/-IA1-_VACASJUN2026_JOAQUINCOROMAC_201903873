# Plan de Pruebas - SmartInvoice

## Facturas de prueba disponibles

El directorio `facturas_generadas/` en la raiz de PRACTICA3 contiene 10 facturas de prueba:
- factura_001.pdf a factura_004.pdf (formato PDF)
- factura_005.png a factura_010.png (formato PNG)

Para completar las 20 facturas requeridas, se deben cargar las 10 disponibles y generar 10 adicionales con el mismo generador de pruebas.

## Checklist de pruebas

### Prueba 1: Autenticacion
- [ ] Login con admin/admin123 funciona correctamente
- [ ] El token JWT se guarda en localStorage
- [ ] El acceso sin token redirige al login
- [ ] El logout limpia el token y redirige al login

### Prueba 2: CRUD de Proveedores
- [ ] Crear proveedor con nombre, NIT, email y telefono
- [ ] Editar nombre y email de proveedor existente
- [ ] Desactivar proveedor (no aparece en la lista)
- [ ] Intentar crear proveedor con NIT duplicado devuelve error

### Prueba 3: Carga y procesamiento OCR
- [ ] Cargar factura_001.pdf: extrae numero, fecha, proveedor, NIT, montos
- [ ] Cargar factura_005.png: extrae todos los campos
- [ ] Verificar que el estado sea "Procesado"
- [ ] Verificar que el texto OCR aparece en el detalle de la factura
- [ ] Cargar archivo con formato invalido (.docx): debe mostrar error

### Prueba 4: Validacion automatica
- [ ] Factura valida: estado = Procesado
- [ ] Factura con montos inconsistentes: estado = Rechazado con detalle de error
- [ ] Campo NIT faltante: estado puede ser Rechazado si no extrae montos

### Prueba 5: Bitacora
- [ ] Cada carga de factura genera un registro en la bitacora
- [ ] El filtro por fecha funciona correctamente
- [ ] El filtro por estado filtra los registros

### Prueba 6: Generacion de reportes
- [ ] Generar reporte PDF: se descarga correctamente
- [ ] Generar reporte Excel: se abre en LibreOffice/Excel
- [ ] Generar reporte CSV: contiene todos los campos correctos
- [ ] Los reportes aparecen en la lista con fecha de generacion

### Prueba 7: Envio de correo
- [ ] Configurar credenciales SMTP en .env
- [ ] Enviar reporte PDF a correo de prueba
- [ ] El correo llega con el archivo adjunto
- [ ] El intento de envio queda registrado en la bitacora

### Prueba 8: Automatizacion RPA
- [ ] Ejecutar RPA en factura procesada
- [ ] El formulario se rellena automaticamente con los datos de la factura
- [ ] La captura de pantalla se guarda en /app/screenshots/
- [ ] El campo rpa_ejecutado de la factura cambia a true
- [ ] El registro de RPA aparece en la bitacora

### Prueba 9: Dashboard
- [ ] Los contadores muestran los totales correctos por estado
- [ ] La tabla de ultimas facturas se actualiza al cargar nuevas

### Prueba 10: Capacidad de 20 facturas
- [ ] Cargar las 10 facturas de prueba disponibles
- [ ] Generar 10 facturas adicionales de prueba
- [ ] Verificar que el sistema procesa las 20 correctamente
- [ ] Generar reporte final con las 20 facturas

## Resultados esperados

Todos los items del checklist deben completarse exitosamente para aprobar la evaluacion presencial.

## Notas

- El tiempo de procesamiento OCR depende del hardware. En maquinas sin GPU puede tomar hasta 15-20 segundos por factura.
- Las primeras cargas pueden ser mas lentas porque EasyOCR descarga los modelos en el primer uso.
