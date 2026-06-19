# Modulo OCR y Computer Vision - SmartInvoice

## Descripcion

El modulo OCR implementa un pipeline de extraccion automatica de informacion desde documentos de facturas en formatos PDF, JPG, JPEG y PNG.

## Pipeline de procesamiento

```
Archivo (PDF/JPG/PNG)
        |
        v
  [vision.py] Cargar imagen
        |
        v
  [vision.py] Escalar 150%
        |
        v
  [vision.py] Convertir a grises
        |
        v
  [vision.py] Reducir ruido (medianBlur)
        |
        v
  [vision.py] Umbralizar (adaptativeThreshold)
        |
        v
  [procesador.py] EasyOCR readtext()
        |
        v
  [procesador.py] Ordenar bloques por posicion
        |
        v
  [extractor.py] Extraer campos con regex
        |
        v
  [extractor.py] Validar montos
        |
        v
  Resultado con campos y estado de validacion
```

## Librerias utilizadas

| Libreria | Version | Razon de uso |
|----------|---------|--------------|
| EasyOCR | 1.7.1 | Mejor precision en texto impreso y soporte multi-idioma sin configuracion adicional |
| OpenCV | 4.9 | Preprocesamiento de imagen: umbralizacion, reduccion de ruido, escalado |
| pdf2image | 1.17 | Conversion de PDF a imagen usando poppler |
| Pillow | 10.3 | Manejo de formatos de imagen y conversion a numpy array |

## Patrones de extraccion

| Campo | Patron regex | Ejemplo |
|-------|-------------|---------|
| Numero de factura | `FAC-\d+` o `No. Factura: XXXX` | FAC-00001 |
| Fecha | `\d{1,2}/\d{1,2}/\d{2,4}` | 15/06/2026 |
| NIT | `NIT: (\d+[-K]?)` | NIT: 12345678-9 |
| Subtotal | `Subtotal: Q?[\d,.]+` | Subtotal: 892.86 |
| IVA | `IVA.*Q?[\d,.]+` | IVA (12%): 107.14 |
| Total | mayor valor en lineas con "TOTAL" | TOTAL: Q1,000.00 |

## Validacion automatica

Antes de marcar la factura como "Procesado", el sistema verifica:
1. Que numero de factura y fecha fueron extraidos.
2. Que todos los montos sean numericos y positivos.
3. Que `subtotal + IVA - total <= 1.00` (tolerancia de redondeo).

Si alguna verificacion falla, la factura queda en estado "Rechazado" con el detalle del error en la bitacora.

## Limitaciones conocidas

- El OCR puede fallar si la imagen tiene muy baja resolucion (menor a 100 DPI).
- Facturas con formatos muy distintos al estandar pueden requerir ajuste de los patrones regex.
- El procesamiento de EasyOCR toma entre 3-15 segundos dependiendo del tamano de la imagen y el hardware.
- No se utiliza GPU por defecto; activarla mejoraria significativamente el rendimiento.

## Ejemplos de extraccion exitosa

Texto OCR tipico de una factura del sistema:
```
FACTURA
No. Factura: FAC-00001
Fecha: 15/06/2026
Proveedor: Servicios Tecnologicos SA
NIT: 12345678-9
...
Subtotal: Q892.86
IVA (12%): Q107.14
TOTAL: Q1,000.00
```

Resultado de extraccion:
```json
{
    "numero_factura": "FAC-00001",
    "fecha_factura": "15/06/2026",
    "proveedor_nombre": "Servicios Tecnologicos SA",
    "proveedor_nit": "12345678-9",
    "subtotal": 892.86,
    "impuesto": 107.14,
    "total": 1000.0,
    "validacion": { "valido": true, "error": null }
}
```
