# Requerimientos Funcionales - SmartInvoice

## RF-01 Autenticacion de usuarios
El sistema permite a los usuarios iniciar sesion con usuario y contrasena. Se genera un token JWT valido por 8 horas.

## RF-02 Carga de facturas
El sistema acepta archivos en formato PDF, JPG, JPEG y PNG de hasta cualquier tamano razonable.

## RF-03 Procesamiento OCR automatico
Al cargar una factura, el sistema ejecuta automaticamente el pipeline de Computer Vision y OCR para extraer los campos de la factura.

## RF-04 Extraccion de campos
El sistema extrae automaticamente: numero de factura, fecha, nombre del proveedor, NIT, subtotal, impuesto/IVA y total.

## RF-05 Validacion automatica
Antes de almacenar definitivamente, el sistema verifica que subtotal + IVA sea igual al total (tolerancia Q1.00). Si falla, marca la factura como "Rechazado".

## RF-06 Almacenamiento en base de datos
Toda la informacion extraida se almacena en PostgreSQL con estado, fecha de carga y usuario responsable.

## RF-07 Gestion de estados de factura
Cada factura puede tener uno de cuatro estados: Procesado, Pendiente, Error, Rechazado. El estado se actualiza automaticamente durante el procesamiento y puede cambiarse manualmente.

## RF-08 CRUD de proveedores
El sistema permite crear, consultar, actualizar y desactivar proveedores (borrado logico).

## RF-09 Bitacora de procesamiento
Cada operacion relevante (carga, procesamiento OCR, cambio de estado, generacion de reporte, envio de correo, RPA) queda registrada en la bitacora con fecha, hora, usuario, documento y resultado.

## RF-10 Generacion de reportes
El sistema genera reportes administrativos en formato PDF, Excel y CSV con toda la informacion de las facturas procesadas.

## RF-11 Envio de reportes por correo
El sistema envia reportes generados como adjunto de correo electronico a cualquier destinatario configurado.

## RF-12 Automatizacion RPA
El sistema ejecuta una automatizacion que abre un formulario web, rellena los datos de la factura y toma una captura de pantalla como evidencia.

## RF-13 Consulta de facturas
El sistema permite listar y consultar el detalle de todas las facturas procesadas desde la interfaz web.

## RF-14 Dashboard administrativo
La interfaz muestra un resumen con contadores de facturas por estado y la tabla de las ultimas 10 facturas procesadas.
