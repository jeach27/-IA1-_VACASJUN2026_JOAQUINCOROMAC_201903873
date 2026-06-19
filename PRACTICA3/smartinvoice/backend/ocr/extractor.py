import re
from typing import Optional, Dict, Any, List


def _limpiar_numero(texto: str) -> Optional[float]:
    """Convierte un string de numero con formato monetario a float."""
    if not texto:
        return None
    limpio = re.sub(r"[Q$,\s]", "", texto)
    limpio = limpio.replace(",", ".")
    try:
        return float(limpio)
    except ValueError:
        return None


def extraer_numero_factura(lineas: List[str]) -> Optional[str]:
    """Busca el numero de factura en las lineas de texto."""
    patron_fac = re.compile(r"(?:No\.?\s*Factura[:\s]*|Factura[:\s#]*|FACTURA[:\s#]*|FAC[-\s]*)([A-Z0-9\-]+)", re.IGNORECASE)
    patron_directo = re.compile(r"\bFAC[-\s]?(\d{4,})\b", re.IGNORECASE)

    for linea in lineas:
        m = patron_fac.search(linea)
        if m:
            return m.group(1).strip()
        m = patron_directo.search(linea)
        if m:
            return f"FAC-{m.group(1)}"

    for linea in lineas:
        m = re.search(r"\b([A-Z]{2,4}-\d{3,})\b", linea)
        if m:
            return m.group(1)

    return None


def extraer_fecha(lineas: List[str]) -> Optional[str]:
    """Busca una fecha en formato DD/MM/YYYY o variantes."""
    patron_fecha = re.compile(r"\b(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})\b")
    for linea in lineas:
        if re.search(r"(?i)fecha", linea):
            m = patron_fecha.search(linea)
            if m:
                return m.group(1)

    for linea in lineas:
        m = patron_fecha.search(linea)
        if m:
            return m.group(1)

    return None


def extraer_proveedor(lineas: List[str]) -> Optional[str]:
    """Extrae el nombre del proveedor buscando la linea siguiente a 'Proveedor:'."""
    for i, linea in enumerate(lineas):
        if re.search(r"(?i)proveedor\s*:", linea):
            parte = re.sub(r"(?i)proveedor\s*:", "", linea).strip()
            if parte:
                return parte
            if i + 1 < len(lineas):
                return lineas[i + 1].strip()

    for i, linea in enumerate(lineas):
        if re.search(r"(?i)empresa\s*:|razon\s+social\s*:", linea):
            parte = re.sub(r"(?i)empresa\s*:|razon\s+social\s*:", "", linea).strip()
            if parte:
                return parte
            if i + 1 < len(lineas):
                return lineas[i + 1].strip()

    return None


def extraer_nit(lineas: List[str]) -> Optional[str]:
    """Extrae el NIT buscando el patron en lineas relevantes."""
    patron_nit = re.compile(r"(?i)nit\s*[:\-]?\s*([0-9\-]+[Kk]?)")
    for linea in lineas:
        m = patron_nit.search(linea)
        if m:
            return m.group(1).strip()
    return None


def extraer_subtotal(lineas: List[str]) -> Optional[float]:
    """Extrae el subtotal de la factura."""
    patron = re.compile(r"(?i)sub\s*total\s*[:\-]?\s*([Q$]?\s*[\d,\.]+)", re.IGNORECASE)
    for linea in lineas:
        m = patron.search(linea)
        if m:
            return _limpiar_numero(m.group(1))
    return None


def extraer_impuesto(lineas: List[str]) -> Optional[float]:
    """Extrae el IVA o impuesto de la factura."""
    patron = re.compile(r"(?i)(?:iva|impuesto|tax)\s*(?:\(12%\))?\s*[:\-]?\s*([Q$]?\s*[\d,\.]+)", re.IGNORECASE)
    for linea in lineas:
        m = patron.search(linea)
        if m:
            return _limpiar_numero(m.group(1))
    return None


def extraer_total(lineas: List[str]) -> Optional[float]:
    """Extrae el total de la factura buscando el mayor monto en contexto de 'TOTAL'."""
    patron = re.compile(r"(?i)total\s*[:\-]?\s*([Q$]?\s*[\d,\.]+)")
    candidatos = []
    for linea in lineas:
        for m in patron.finditer(linea):
            valor = _limpiar_numero(m.group(1))
            if valor is not None:
                candidatos.append(valor)

    if not candidatos:
        return None
    return max(candidatos)


def validar_montos(subtotal: Optional[float], impuesto: Optional[float], total: Optional[float]) -> Dict[str, Any]:
    """
    Verifica que subtotal + impuesto sea aproximadamente igual al total.
    Tolerancia de Q1.00 para diferencias de redondeo.
    """
    if subtotal is None or impuesto is None or total is None:
        campos_faltantes = [c for c, v in [("subtotal", subtotal), ("impuesto", impuesto), ("total", total)] if v is None]
        return {
            "valido": False,
            "error": f"Campos numericos faltantes: {', '.join(campos_faltantes)}",
        }

    suma = subtotal + impuesto
    diferencia = abs(suma - total)
    if diferencia > 1.0:
        return {
            "valido": False,
            "error": f"Subtotal ({subtotal}) + IVA ({impuesto}) = {suma} no coincide con Total ({total}). Diferencia: {diferencia:.2f}",
        }

    return {"valido": True, "error": None}


def extraer_campos(resultado_ocr: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recibe el resultado del procesador OCR y extrae todos los campos de la factura.
    Retorna un diccionario con los campos extraidos y un resultado de validacion.
    """
    lineas = resultado_ocr.get("lineas", [])

    numero_factura = extraer_numero_factura(lineas)
    fecha = extraer_fecha(lineas)
    proveedor = extraer_proveedor(lineas)
    nit = extraer_nit(lineas)
    subtotal = extraer_subtotal(lineas)
    impuesto = extraer_impuesto(lineas)
    total = extraer_total(lineas)

    validacion = validar_montos(subtotal, impuesto, total)

    campos_obligatorios_faltantes = []
    if not numero_factura:
        campos_obligatorios_faltantes.append("numero_factura")
    if not fecha:
        campos_obligatorios_faltantes.append("fecha")

    if campos_obligatorios_faltantes:
        validacion["valido"] = False
        mensaje_campos = f"Campos obligatorios no encontrados: {', '.join(campos_obligatorios_faltantes)}"
        validacion["error"] = f"{validacion.get('error', '')}; {mensaje_campos}".strip("; ")

    return {
        "numero_factura": numero_factura,
        "fecha_factura": fecha,
        "proveedor_nombre": proveedor,
        "proveedor_nit": nit,
        "subtotal": subtotal or 0.0,
        "impuesto": impuesto or 0.0,
        "total": total or 0.0,
        "validacion": validacion,
        "texto_completo": resultado_ocr.get("texto_completo", ""),
    }
