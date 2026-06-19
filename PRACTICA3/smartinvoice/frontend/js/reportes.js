async function cargarReportes() {
    const tbody = document.getElementById("tabla-reportes-body");
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="5" class="cargador">Cargando reportes...</td></tr>';

    try {
        const reportes = await get("/reportes/");
        if (!reportes || reportes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="sin-datos">No hay reportes generados</td></tr>';
            return;
        }
        tbody.innerHTML = reportes.map(r => `
            <tr>
                <td>${r.id}</td>
                <td>${r.nombre}</td>
                <td>${r.formato.toUpperCase()}</td>
                <td>${formatearFecha(r.fecha_generacion)}</td>
                <td>
                    <button class="btn btn-primario" onclick="descargarReporte(${r.id})" style="padding:4px 10px;font-size:12px;">Descargar</button>
                    <button class="btn btn-acento" onclick="abrirEnviarCorreo(${r.id})" style="padding:4px 10px;font-size:12px;margin-left:4px;background:#8E44AD;color:white;">Enviar</button>
                </td>
            </tr>
        `).join("");
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="5" class="sin-datos">Error: ${err.message}</td></tr>`;
    }
}

async function generarReporte() {
    const formato = document.getElementById("formato-reporte").value;
    const btn = document.getElementById("btn-generar");
    btn.disabled = true;
    btn.textContent = "Generando...";

    try {
        await post("/reportes/generar", { formato });
        mostrarAlerta("alerta-reportes", `Reporte ${formato.toUpperCase()} generado exitosamente`, "exito");
        await cargarReportes();
    } catch (err) {
        mostrarAlerta("alerta-reportes", err.message, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Generar Reporte";
    }
}

async function descargarReporte(id) {
    try {
        const respuesta = await peticion("GET", `/reportes/${id}/descargar`);
        const blob = await respuesta.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `reporte_${id}`;
        a.click();
        URL.revokeObjectURL(url);
    } catch (err) {
        mostrarAlerta("alerta-reportes", "Error al descargar: " + err.message, "error");
    }
}

let reporteEnviarId = null;

function abrirEnviarCorreo(id) {
    reporteEnviarId = id;
    document.getElementById("form-enviar-correo").reset();
    document.getElementById("modal-correo").classList.add("visible");
}

function cerrarModalCorreo() {
    document.getElementById("modal-correo").classList.remove("visible");
    reporteEnviarId = null;
}

async function enviarCorreo(evento) {
    evento.preventDefault();
    if (!reporteEnviarId) return;

    const destinatario = document.getElementById("correo-destinatario").value.trim();
    const asunto = document.getElementById("correo-asunto").value.trim();
    const mensaje = document.getElementById("correo-mensaje").value.trim();

    const btn = document.getElementById("btn-enviar-correo");
    btn.disabled = true;
    btn.textContent = "Enviando...";

    try {
        const res = await post(`/reportes/${reporteEnviarId}/enviar`, { destinatario, asunto, mensaje });
        cerrarModalCorreo();
        mostrarAlerta("alerta-reportes", res.mensaje || "Correo enviado exitosamente", "exito");
    } catch (err) {
        mostrarAlerta("alerta-reportes", err.message, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Enviar";
    }
}
