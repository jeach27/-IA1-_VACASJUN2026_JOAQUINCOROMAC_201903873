let proveedorEditandoId = null;

async function cargarProveedores() {
    const tbody = document.getElementById("tabla-proveedores-body");
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="6" class="cargador">Cargando proveedores...</td></tr>';

    try {
        const proveedores = await get("/proveedores/");
        if (!proveedores || proveedores.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="sin-datos">No hay proveedores registrados</td></tr>';
            return;
        }
        tbody.innerHTML = proveedores.map(p => `
            <tr>
                <td>${p.id}</td>
                <td class="negrita">${p.nombre}</td>
                <td>${p.nit}</td>
                <td>${p.email || "-"}</td>
                <td>${p.telefono || "-"}</td>
                <td>
                    <button class="btn btn-primario" onclick="abrirEditar(${p.id})" style="padding:4px 10px;font-size:12px;">Editar</button>
                    <button class="btn btn-peligro" onclick="desactivarProveedor(${p.id})" style="padding:4px 10px;font-size:12px;margin-left:4px;">Desactivar</button>
                </td>
            </tr>
        `).join("");
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="6" class="sin-datos">Error: ${err.message}</td></tr>`;
    }
}

function abrirNuevoProveedor() {
    proveedorEditandoId = null;
    document.getElementById("modal-prov-titulo").textContent = "Nuevo Proveedor";
    document.getElementById("form-proveedor").reset();
    document.getElementById("modal-proveedor").classList.add("visible");
}

async function abrirEditar(id) {
    try {
        const p = await get(`/proveedores/${id}`);
        proveedorEditandoId = id;
        document.getElementById("modal-prov-titulo").textContent = "Editar Proveedor";
        document.getElementById("prov-nombre").value = p.nombre || "";
        document.getElementById("prov-nit").value = p.nit || "";
        document.getElementById("prov-direccion").value = p.direccion || "";
        document.getElementById("prov-email").value = p.email || "";
        document.getElementById("prov-telefono").value = p.telefono || "";
        document.getElementById("modal-proveedor").classList.add("visible");
    } catch (err) {
        alert("Error al cargar proveedor: " + err.message);
    }
}

function cerrarModalProveedor() {
    document.getElementById("modal-proveedor").classList.remove("visible");
    proveedorEditandoId = null;
}

async function guardarProveedor(evento) {
    evento.preventDefault();
    const datos = {
        nombre: document.getElementById("prov-nombre").value.trim(),
        nit: document.getElementById("prov-nit").value.trim(),
        direccion: document.getElementById("prov-direccion").value.trim() || null,
        email: document.getElementById("prov-email").value.trim() || null,
        telefono: document.getElementById("prov-telefono").value.trim() || null,
    };

    const btn = document.getElementById("btn-guardar-prov");
    btn.disabled = true;
    btn.textContent = "Guardando...";

    try {
        if (proveedorEditandoId) {
            await put(`/proveedores/${proveedorEditandoId}`, datos);
            mostrarAlerta("alerta-proveedores", "Proveedor actualizado correctamente", "exito");
        } else {
            await post("/proveedores/", datos);
            mostrarAlerta("alerta-proveedores", "Proveedor creado correctamente", "exito");
        }
        cerrarModalProveedor();
        await cargarProveedores();
    } catch (err) {
        mostrarAlerta("alerta-proveedores", err.message, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Guardar";
    }
}

async function desactivarProveedor(id) {
    if (!confirm("Desactivar este proveedor?")) return;
    try {
        await del(`/proveedores/${id}`);
        mostrarAlerta("alerta-proveedores", "Proveedor desactivado", "info");
        await cargarProveedores();
    } catch (err) {
        mostrarAlerta("alerta-proveedores", err.message, "error");
    }
}
