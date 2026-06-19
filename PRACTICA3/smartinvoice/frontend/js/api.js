const API_BASE = "/api";

function obtenerToken() {
    return localStorage.getItem("token");
}

function guardarToken(token) {
    localStorage.setItem("token", token);
}

function borrarToken() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
}

async function peticion(metodo, ruta, cuerpo = null, esArchivo = false) {
    const token = obtenerToken();
    const cabeceras = {};

    if (token) {
        cabeceras["Authorization"] = `Bearer ${token}`;
    }

    const opciones = { method: metodo, headers: cabeceras };

    if (cuerpo && !esArchivo) {
        cabeceras["Content-Type"] = "application/json";
        opciones.body = JSON.stringify(cuerpo);
    } else if (cuerpo && esArchivo) {
        opciones.body = cuerpo;
    }

    const respuesta = await fetch(`${API_BASE}${ruta}`, opciones);

    if (respuesta.status === 401) {
        borrarToken();
        window.location.href = "/index.html";
        return;
    }

    if (!respuesta.ok) {
        let mensajeError = `Error ${respuesta.status}`;
        try {
            const datos = await respuesta.json();
            mensajeError = datos.detail || mensajeError;
        } catch (_) {}
        throw new Error(mensajeError);
    }

    const tipoContenido = respuesta.headers.get("content-type") || "";
    if (tipoContenido.includes("application/json")) {
        return respuesta.json();
    }

    return respuesta;
}

function get(ruta) { return peticion("GET", ruta); }
function post(ruta, cuerpo) { return peticion("POST", ruta, cuerpo); }
function put(ruta, cuerpo) { return peticion("PUT", ruta, cuerpo); }
function del(ruta) { return peticion("DELETE", ruta); }
function postArchivo(ruta, formData) { return peticion("POST", ruta, formData, true); }

function mostrarAlerta(elementoId, mensaje, tipo = "info") {
    const el = document.getElementById(elementoId);
    if (!el) return;
    el.textContent = mensaje;
    el.className = `alerta alerta-${tipo} visible`;
    setTimeout(() => { el.className = "alerta"; }, 5000);
}

function badgeEstado(estado) {
    const mapa = {
        "Procesado": "procesado",
        "Pendiente": "pendiente",
        "Error": "error",
        "Rechazado": "rechazado",
    };
    const clase = mapa[estado] || "pendiente";
    return `<span class="badge badge-${clase}">${estado}</span>`;
}

function formatearFecha(fechaStr) {
    if (!fechaStr) return "-";
    try {
        const d = new Date(fechaStr);
        return d.toLocaleDateString("es-GT", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" });
    } catch (_) {
        return fechaStr;
    }
}

function formatearMoneda(valor) {
    if (valor === null || valor === undefined) return "-";
    return `Q${parseFloat(valor).toFixed(2)}`;
}
