async function cargarBitacora() {
    const tbody = document.getElementById("tabla-bitacora-body");
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="6" class="cargador">Cargando bitacora...</td></tr>';

    const fechaInicio = document.getElementById("filtro-fecha-inicio")?.value || "";
    const fechaFin = document.getElementById("filtro-fecha-fin")?.value || "";
    const estado = document.getElementById("filtro-estado")?.value || "";

    let ruta = "/bitacora/?";
    if (fechaInicio) ruta += `fecha_inicio=${fechaInicio}&`;
    if (fechaFin) ruta += `fecha_fin=${fechaFin}&`;
    if (estado) ruta += `estado=${encodeURIComponent(estado)}&`;

    try {
        const registros = await get(ruta.replace(/\?$/, "").replace(/&$/, ""));
        if (!registros || registros.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="sin-datos">No hay registros en la bitacora</td></tr>';
            return;
        }
        tbody.innerHTML = registros.map(r => `
            <tr>
                <td>${r.id}</td>
                <td>${formatearFecha(r.fecha_hora)}</td>
                <td>${r.documento_nombre || "-"}</td>
                <td><span class="badge badge-${(r.estado || "").toLowerCase().replace(/\s/g,'-')}">${r.estado || "-"}</span></td>
                <td>${r.resultado || "-"}</td>
                <td>${r.usuario_id || "-"}</td>
            </tr>
        `).join("");
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="6" class="sin-datos">Error: ${err.message}</td></tr>`;
    }
}

function aplicarFiltros() {
    cargarBitacora();
}

function limpiarFiltros() {
    document.getElementById("filtro-fecha-inicio").value = "";
    document.getElementById("filtro-fecha-fin").value = "";
    document.getElementById("filtro-estado").value = "";
    cargarBitacora();
}
