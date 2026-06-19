let facturaSeleccionadaId = null;

async function cargarFacturas() {
    const tbody = document.getElementById("tabla-facturas-body");
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="8" class="cargador">Cargando facturas...</td></tr>';

    try {
        const facturas = await get("/facturas/");
        if (!facturas || facturas.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="sin-datos">No hay facturas registradas</td></tr>';
            return;
        }
        tbody.innerHTML = facturas.map(f => `
            <tr>
                <td>${f.id}</td>
                <td>${f.numero_factura || "-"}</td>
                <td>${f.fecha_factura || "-"}</td>
                <td>${f.proveedor_nombre || "-"}</td>
                <td>${formatearMoneda(f.total)}</td>
                <td>${badgeEstado(f.estado)}</td>
                <td>${formatearFecha(f.fecha_carga)}</td>
                <td>
                    <button class="btn btn-secundario" onclick="verDetalle(${f.id})" style="padding:4px 10px;font-size:12px;">Ver</button>
                    <button class="btn btn-advertencia" onclick="ejecutarRPA(${f.id})" style="padding:4px 10px;font-size:12px;margin-left:4px;" ${f.rpa_ejecutado ? 'title="RPA ya ejecutado"' : ''}>RPA</button>
                </td>
            </tr>
        `).join("");
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="8" class="sin-datos">Error: ${err.message}</td></tr>`;
    }
}

async function subirFactura(evento) {
    evento.preventDefault();
    const archivoInput = document.getElementById("archivo-factura");
    const archivo = archivoInput.files[0];
    if (!archivo) {
        mostrarAlerta("alerta-carga", "Seleccione un archivo", "error");
        return;
    }

    const btnSubir = document.getElementById("btn-subir");
    btnSubir.disabled = true;
    btnSubir.textContent = "Procesando...";

    const resultadoDiv = document.getElementById("resultado-carga");
    resultadoDiv.innerHTML = "";

    const formData = new FormData();
    formData.append("archivo", archivo);

    try {
        const respuesta = await postArchivo("/facturas/cargar", formData);
        const f = respuesta.factura;
        const campos = respuesta.campos_extraidos;

        resultadoDiv.innerHTML = `
            <div class="alerta alerta-${f.estado === 'Procesado' ? 'exito' : 'error'} visible">${respuesta.mensaje}</div>
            <div class="campos-extraidos">
                <div class="campo-extraido"><div class="campo-extraido-nombre">Numero Factura</div><div class="campo-extraido-valor">${campos.numero_factura || "-"}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Fecha</div><div class="campo-extraido-valor">${campos.fecha_factura || "-"}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Proveedor</div><div class="campo-extraido-valor">${campos.proveedor_nombre || "-"}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">NIT</div><div class="campo-extraido-valor">${campos.proveedor_nit || "-"}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Subtotal</div><div class="campo-extraido-valor">${formatearMoneda(campos.subtotal)}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">IVA</div><div class="campo-extraido-valor">${formatearMoneda(campos.impuesto)}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Total</div><div class="campo-extraido-valor">${formatearMoneda(campos.total)}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Estado</div><div class="campo-extraido-valor">${badgeEstado(f.estado)}</div></div>
            </div>
        `;

        archivoInput.value = "";
        await cargarFacturas();
    } catch (err) {
        mostrarAlerta("alerta-carga", err.message, "error");
    } finally {
        btnSubir.disabled = false;
        btnSubir.textContent = "Cargar y Procesar";
    }
}

async function verDetalle(id) {
    facturaSeleccionadaId = id;
    try {
        const f = await get(`/facturas/${id}`);
        document.getElementById("modal-factura-titulo").textContent = `Factura ${f.numero_factura || id}`;
        document.getElementById("modal-factura-contenido").innerHTML = `
            <div class="campos-extraidos">
                <div class="campo-extraido"><div class="campo-extraido-nombre">ID</div><div class="campo-extraido-valor">${f.id}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Numero Factura</div><div class="campo-extraido-valor">${f.numero_factura || "-"}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Fecha</div><div class="campo-extraido-valor">${f.fecha_factura || "-"}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Proveedor</div><div class="campo-extraido-valor">${f.proveedor_nombre || "-"}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">NIT</div><div class="campo-extraido-valor">${f.proveedor_nit || "-"}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Subtotal</div><div class="campo-extraido-valor">${formatearMoneda(f.subtotal)}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">IVA</div><div class="campo-extraido-valor">${formatearMoneda(f.impuesto)}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Total</div><div class="campo-extraido-valor">${formatearMoneda(f.total)}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">Estado</div><div class="campo-extraido-valor">${badgeEstado(f.estado)}</div></div>
                <div class="campo-extraido"><div class="campo-extraido-nombre">RPA Ejecutado</div><div class="campo-extraido-valor">${f.rpa_ejecutado ? "Si" : "No"}</div></div>
            </div>
            ${f.errores_validacion ? `<div class="alerta alerta-error visible mt-16"><strong>Errores:</strong> ${f.errores_validacion}</div>` : ""}
            ${f.texto_extraido ? `<div class="mt-16"><div class="campo-extraido-nombre">Texto extraido por OCR:</div><pre style="font-size:11px;background:#F8F9FA;padding:10px;border-radius:4px;overflow:auto;max-height:200px;margin-top:6px;">${f.texto_extraido.substring(0, 1000)}...</pre></div>` : ""}
        `;
        document.getElementById("modal-factura").classList.add("visible");
    } catch (err) {
        alert("Error al cargar detalle: " + err.message);
    }
}

function cerrarModalFactura() {
    document.getElementById("modal-factura").classList.remove("visible");
    facturaSeleccionadaId = null;
}

async function ejecutarRPA(id) {
    if (!confirm(`Ejecutar automatizacion RPA para la factura ID ${id}?`)) return;
    try {
        const res = await post(`/facturas/${id}/rpa`);
        alert(res.mensaje || "RPA ejecutado correctamente");
        await cargarFacturas();
    } catch (err) {
        alert("Error RPA: " + err.message);
    }
}
