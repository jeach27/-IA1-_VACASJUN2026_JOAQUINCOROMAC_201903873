import cv2
import numpy as np
from PIL import Image
import os
from typing import List


def cargar_imagen(ruta_archivo: str) -> np.ndarray:
    """Carga una imagen desde disco. Convierte PNG/JPG directamente; PDF via pdf2image."""
    extension = os.path.splitext(ruta_archivo)[1].lower()

    if extension == ".pdf":
        return _pdf_a_imagen(ruta_archivo)

    imagen = cv2.imread(ruta_archivo)
    if imagen is None:
        pil_img = Image.open(ruta_archivo).convert("RGB")
        imagen = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return imagen


def _pdf_a_imagen(ruta_pdf: str) -> np.ndarray:
    """Convierte la primera pagina de un PDF a imagen numpy."""
    from pdf2image import convert_from_path

    paginas = convert_from_path(ruta_pdf, dpi=200, first_page=1, last_page=1)
    if not paginas:
        raise ValueError(f"No se pudo convertir el PDF: {ruta_pdf}")

    pil_img = paginas[0].convert("RGB")
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def convertir_escala_grises(imagen: np.ndarray) -> np.ndarray:
    """Convierte la imagen a escala de grises."""
    if len(imagen.shape) == 3:
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    return imagen


def aplicar_umbralizado(imagen_gris: np.ndarray) -> np.ndarray:
    """Aplica umbralizado adaptativo para mejorar el contraste del texto."""
    return cv2.adaptiveThreshold(
        imagen_gris,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
    )


def reducir_ruido(imagen: np.ndarray) -> np.ndarray:
    """Aplica filtro mediano para reducir ruido de la imagen."""
    return cv2.medianBlur(imagen, 3)


def escalar_imagen(imagen: np.ndarray, factor: float = 1.5) -> np.ndarray:
    """Aumenta el tamano de la imagen para mejorar la lectura OCR."""
    alto, ancho = imagen.shape[:2]
    nuevo_ancho = int(ancho * factor)
    nuevo_alto = int(alto * factor)
    return cv2.resize(imagen, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_LINEAR)


def preprocesar_para_ocr(ruta_archivo: str) -> np.ndarray:
    """Pipeline completo de preprocesamiento antes de OCR."""
    imagen = cargar_imagen(ruta_archivo)
    imagen = escalar_imagen(imagen, factor=1.5)
    imagen_gris = convertir_escala_grises(imagen)
    imagen_sin_ruido = reducir_ruido(imagen_gris)
    imagen_umbral = aplicar_umbralizado(imagen_sin_ruido)
    return imagen_umbral
