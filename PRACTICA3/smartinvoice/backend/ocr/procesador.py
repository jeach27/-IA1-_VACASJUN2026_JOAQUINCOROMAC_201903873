import easyocr
import numpy as np
from typing import List, Tuple, Dict, Any
from ocr.vision import preprocesar_para_ocr

_reader = None


def obtener_reader() -> easyocr.Reader:
    """Instancia unica de EasyOCR para evitar recargar el modelo repetidamente."""
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["es", "en"], gpu=False)
    return _reader


def extraer_texto(ruta_archivo: str) -> Dict[str, Any]:
    """
    Ejecuta el pipeline completo de OCR sobre una factura.

    Retorna un diccionario con:
    - texto_completo: string con todo el texto extraido linea por linea
    - bloques: lista de tuplas (bbox, texto, confianza)
    - lineas: lista de strings con las lineas de texto ordenadas
    """
    imagen_procesada = preprocesar_para_ocr(ruta_archivo)

    reader = obtener_reader()
    resultados = reader.readtext(imagen_procesada, detail=1, paragraph=False)

    bloques = []
    for bbox, texto, confianza in resultados:
        bloques.append({
            "bbox": bbox,
            "texto": texto.strip(),
            "confianza": round(float(confianza), 4),
        })

    bloques_ordenados = sorted(bloques, key=lambda b: (b["bbox"][0][1], b["bbox"][0][0]))

    lineas = [b["texto"] for b in bloques_ordenados if b["texto"]]
    texto_completo = "\n".join(lineas)

    return {
        "texto_completo": texto_completo,
        "bloques": bloques_ordenados,
        "lineas": lineas,
    }
