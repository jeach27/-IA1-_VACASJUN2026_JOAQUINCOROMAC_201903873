import os
from datetime import datetime
from typing import Dict, Any

SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "/app/screenshots")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")


def ejecutar_automatizacion(datos_factura: Dict[str, Any]) -> Dict[str, Any]:
    """
    Automatizacion RPA con Playwright.
    Abre el formulario de registro, rellena los campos de la factura
    y toma una captura de pantalla como evidencia.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    num_factura = datos_factura.get("numero_factura", "desconocida").replace("/", "-")
    nombre_captura = f"rpa_{num_factura}_{timestamp}.png"
    ruta_captura = os.path.join(SCREENSHOTS_DIR, nombre_captura)

    try:
        from playwright.sync_api import sync_playwright

        url_formulario = f"{FRONTEND_URL}/formulario_registro.html"

        with sync_playwright() as p:
            navegador = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            contexto = navegador.new_context(viewport={"width": 1280, "height": 800})
            pagina = contexto.new_page()

            pagina.goto(url_formulario, wait_until="networkidle", timeout=15000)

            _rellenar_campo(pagina, "#num_factura", datos_factura.get("numero_factura", ""))
            _rellenar_campo(pagina, "#fecha_factura", datos_factura.get("fecha_factura", ""))
            _rellenar_campo(pagina, "#proveedor", datos_factura.get("proveedor", ""))
            _rellenar_campo(pagina, "#nit", datos_factura.get("nit", ""))
            _rellenar_campo(pagina, "#subtotal", datos_factura.get("subtotal", "0"))
            _rellenar_campo(pagina, "#impuesto", datos_factura.get("impuesto", "0"))
            _rellenar_campo(pagina, "#total", datos_factura.get("total", "0"))

            pagina.click("#btn_registrar")
            pagina.wait_for_timeout(800)

            pagina.screenshot(path=ruta_captura, full_page=True)

            navegador.close()

        return {
            "exito": True,
            "captura": ruta_captura,
            "mensaje": f"Automatizacion RPA completada. Factura {datos_factura.get('numero_factura', '')} registrada en formulario.",
        }

    except Exception as e:
        return {
            "exito": False,
            "captura": None,
            "mensaje": f"Error en automatizacion RPA: {str(e)}",
        }


def _rellenar_campo(pagina, selector: str, valor: str):
    """Rellena un campo del formulario si el selector existe en la pagina."""
    try:
        pagina.fill(selector, str(valor))
    except Exception:
        pass
