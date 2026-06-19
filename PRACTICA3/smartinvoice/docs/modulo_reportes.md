# Modulo de Reportes - SmartInvoice

## Descripcion

El modulo de reportes genera documentos administrativos con la informacion de todas las facturas procesadas en el sistema. Soporta tres formatos de salida.

## Formatos disponibles

### PDF (ReportLab)
- Tabla con numero de factura, fecha, proveedor, NIT, subtotal, IVA, total y estado.
- Encabezado con titulo del reporte y fecha de generacion.
- Fila de totales al final de la tabla.
- Pagina en formato horizontal (landscape) para acomodar todas las columnas.

### Excel (openpyxl)
- Encabezados con fondo oscuro y texto blanco.
- Filas alternadas en blanco y gris claro.
- Columnas con ancho automatico.
- Fila de totales en negrita.

### CSV (stdlib csv)
- Filas planas con todos los campos.
- Encoding UTF-8.
- Separador de coma estandar.

## Archivos generados

Los reportes se guardan en el volumen `reports_data` montado en `/app/reports/`.

El nombre del archivo sigue el patron: `reporte_{YYYYMMDD_HHMMSS}.{extension}`

## Envio por correo

Los reportes pueden enviarse directamente por correo electronico desde la interfaz web o via el endpoint `POST /reportes/{id}/enviar`. Ver `docs/modulo_correo.md` para configuracion SMTP.
