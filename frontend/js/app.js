/**
 * Logica del frontend: consume la API REST del backend Python/FastAPI.
 * No implementa ningun algoritmo de rutas; toda la logica reside en Prolog.
 */

const API_BASE = "http://localhost:8000/api";

// ------------------------------------------------------------------
// Navegacion entre pestanas
// ------------------------------------------------------------------

document.querySelectorAll("nav button[data-pestana]").forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll("nav button").forEach((b) => b.classList.remove("activo"));
        document.querySelectorAll(".pestana").forEach((p) => p.classList.remove("activo"));
        btn.classList.add("activo");
        document.getElementById(btn.dataset.pestana).classList.add("activo");
    });
});

// ------------------------------------------------------------------
// Carga inicial de ciudades en los selectores
// ------------------------------------------------------------------

async function cargarCiudades() {
    try {
        const resp = await fetch(`${API_BASE}/ciudades`);
        if (!resp.ok) throw new Error("No se pudo obtener la lista de ciudades.");
        const datos = await resp.json();
        const ciudades = datos.ciudades;

        // Actualizar todos los selectores del DOM
        const selectores = document.querySelectorAll("select.selector-ciudad");
        selectores.forEach((sel) => {
            const valorActual = sel.value;
            sel.innerHTML = '<option value="">-- Seleccionar ciudad --</option>';
            ciudades.forEach((c) => {
                const op = document.createElement("option");
                op.value = c;
                op.textContent = formatearCiudad(c);
                sel.appendChild(op);
            });
            if (valorActual) sel.value = valorActual;
        });

        // Actualizar contador en la pestana de ciudades
        const contadorEl = document.getElementById("contador-ciudades");
        if (contadorEl) contadorEl.textContent = ciudades.length;

        return ciudades;
    } catch (err) {
        mostrarError("error-ciudades", err.message);
        return [];
    }
}

// ------------------------------------------------------------------
// Pestana 1: Ruta mas corta
// ------------------------------------------------------------------

document.getElementById("btn-ruta-corta").addEventListener("click", async () => {
    const origen = document.getElementById("origen-corta").value;
    const destino = document.getElementById("destino-corta").value;
    const contenedor = document.getElementById("resultado-ruta-corta");

    limpiarMensajes(contenedor);

    if (!origen || !destino) {
        contenedor.innerHTML = '<p class="mensaje-error">Debe seleccionar origen y destino.</p>';
        return;
    }

    contenedor.innerHTML = '<p class="cargando">Consultando Prolog...</p>';

    try {
        const resp = await fetch(`${API_BASE}/ruta-mas-corta`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ origen, destino }),
        });
        const datos = await resp.json();
        if (!resp.ok) {
            contenedor.innerHTML = `<p class="mensaje-error">${datos.detail}</p>`;
            return;
        }
        contenedor.innerHTML = renderizarRutaOptima(datos.ruta, datos.distancia);
    } catch (err) {
        contenedor.innerHTML = `<p class="mensaje-error">Error de conexion con el servidor: ${err.message}</p>`;
    }
});

document.getElementById("btn-limpiar-corta").addEventListener("click", () => {
    document.getElementById("origen-corta").value = "";
    document.getElementById("destino-corta").value = "";
    document.getElementById("resultado-ruta-corta").innerHTML =
        '<p class="resultado-vacio">Seleccione origen y destino para calcular la ruta.</p>';
});

// ------------------------------------------------------------------
// Pestana 2: Todas las rutas
// ------------------------------------------------------------------

document.getElementById("btn-todas-rutas").addEventListener("click", async () => {
    const origen = document.getElementById("origen-todas").value;
    const destino = document.getElementById("destino-todas").value;
    const contenedor = document.getElementById("resultado-todas-rutas");

    limpiarMensajes(contenedor);

    if (!origen || !destino) {
        contenedor.innerHTML = '<p class="mensaje-error">Debe seleccionar origen y destino.</p>';
        return;
    }

    contenedor.innerHTML = '<p class="cargando">Consultando Prolog...</p>';

    try {
        const resp = await fetch(`${API_BASE}/todas-las-rutas`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ origen, destino }),
        });
        const datos = await resp.json();
        if (!resp.ok) {
            contenedor.innerHTML = `<p class="mensaje-error">${datos.detail}</p>`;
            return;
        }
        contenedor.innerHTML = renderizarTablaRutas(datos.rutas, datos.total_rutas);
    } catch (err) {
        contenedor.innerHTML = `<p class="mensaje-error">Error de conexion con el servidor: ${err.message}</p>`;
    }
});

document.getElementById("btn-limpiar-todas").addEventListener("click", () => {
    document.getElementById("origen-todas").value = "";
    document.getElementById("destino-todas").value = "";
    document.getElementById("resultado-todas-rutas").innerHTML =
        '<p class="resultado-vacio">Seleccione origen y destino para ver todas las rutas disponibles.</p>';
});

// ------------------------------------------------------------------
// Pestana 3: Administrar ciudades y conexiones
// ------------------------------------------------------------------

document.getElementById("btn-agregar-conexion").addEventListener("click", async () => {
    const ciudad1 = document.getElementById("nueva-ciudad1").value.trim();
    const ciudad2 = document.getElementById("nueva-ciudad2").value.trim();
    const distancia = parseInt(document.getElementById("nueva-distancia").value, 10);
    const msgEl = document.getElementById("msg-conexion");

    msgEl.innerHTML = "";

    if (!ciudad1 || !ciudad2) {
        msgEl.innerHTML = '<p class="mensaje-error">Complete los nombres de ambas ciudades.</p>';
        return;
    }
    if (!distancia || distancia <= 0) {
        msgEl.innerHTML = '<p class="mensaje-error">La distancia debe ser un numero mayor a 0.</p>';
        return;
    }

    try {
        const resp = await fetch(`${API_BASE}/conexion`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ciudad1, ciudad2, distancia }),
        });
        const datos = await resp.json();
        if (!resp.ok) {
            msgEl.innerHTML = `<p class="mensaje-error">${datos.detail}</p>`;
            return;
        }
        msgEl.innerHTML = `<p class="mensaje-exito">${datos.mensaje}</p>`;
        document.getElementById("nueva-ciudad1").value = "";
        document.getElementById("nueva-ciudad2").value = "";
        document.getElementById("nueva-distancia").value = "";
        // Recargar ciudades y conexiones
        await cargarCiudades();
        await cargarConexiones();
    } catch (err) {
        msgEl.innerHTML = `<p class="mensaje-error">Error de conexion: ${err.message}</p>`;
    }
});

// ------------------------------------------------------------------
// Pestana 4: Ciudades registradas
// ------------------------------------------------------------------

async function cargarListaCiudades() {
    const contenedor = document.getElementById("lista-ciudades-panel");
    contenedor.innerHTML = '<p class="cargando">Cargando...</p>';
    try {
        const resp = await fetch(`${API_BASE}/ciudades`);
        const datos = await resp.json();
        if (!resp.ok) throw new Error(datos.detail);

        const lista = datos.ciudades
            .map((c) => `<span class="ciudad-tag">${formatearCiudad(c)}</span>`)
            .join("");
        contenedor.innerHTML = `<div class="lista-ciudades">${lista}</div>`;

        document.getElementById("total-ciudades").textContent = datos.total;
    } catch (err) {
        contenedor.innerHTML = `<p class="mensaje-error">${err.message}</p>`;
    }
}

async function cargarConexiones() {
    const contenedor = document.getElementById("tabla-conexiones-panel");
    contenedor.innerHTML = '<p class="cargando">Cargando...</p>';
    try {
        const resp = await fetch(`${API_BASE}/conexiones`);
        const datos = await resp.json();
        if (!resp.ok) throw new Error(datos.detail);

        if (datos.conexiones.length === 0) {
            contenedor.innerHTML = '<p class="resultado-vacio">No hay conexiones registradas.</p>';
            return;
        }

        const filas = datos.conexiones
            .map(
                (c) =>
                    `<tr>
                        <td>${formatearCiudad(c.origen)}</td>
                        <td>${formatearCiudad(c.destino)}</td>
                        <td>${c.distancia} km</td>
                    </tr>`
            )
            .join("");

        contenedor.innerHTML = `
            <table class="tabla-conexiones">
                <thead><tr><th>Origen</th><th>Destino</th><th>Distancia</th></tr></thead>
                <tbody>${filas}</tbody>
            </table>`;

        document.getElementById("total-conexiones").textContent = datos.total;
    } catch (err) {
        contenedor.innerHTML = `<p class="mensaje-error">${err.message}</p>`;
    }
}

// Cargar datos al activar la pestana de administracion
document.querySelector('[data-pestana="tab-admin"]').addEventListener("click", () => {
    cargarListaCiudades();
    cargarConexiones();
});

// ------------------------------------------------------------------
// Funciones de renderizado
// ------------------------------------------------------------------

function renderizarRutaOptima(ciudades, distancia) {
    const chips = ciudades
        .map((c) => `<span class="ciudad-chip">${formatearCiudad(c)}</span>`)
        .join('<span class="flecha"> > </span>');

    return `
        <div class="ruta-optima">
            <span class="distancia-badge">Distancia: ${distancia} km</span>
            <div class="ruta-ciudades">${chips}</div>
        </div>`;
}

function renderizarTablaRutas(rutas, total) {
    if (rutas.length === 0) {
        return '<p class="resultado-vacio">No se encontraron rutas.</p>';
    }

    const filas = rutas
        .map((r, i) => {
            const ciudadesTexto = r.ciudades.map(formatearCiudad).join(" > ");
            const esMejor = i === 0 ? '<span class="badge-mejor">Optima</span>' : "";
            return `<tr>
                <td>${i + 1}</td>
                <td>${ciudadesTexto}${esMejor}</td>
                <td>${r.distancia} km</td>
            </tr>`;
        })
        .join("");

    return `
        <p style="font-size:0.85rem; color:#64748b; margin-bottom:0.75rem;">
            Se encontraron ${total} ruta(s). Ordenadas de menor a mayor distancia.
        </p>
        <table class="tabla-rutas">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Ruta</th>
                    <th>Distancia</th>
                </tr>
            </thead>
            <tbody>${filas}</tbody>
        </table>`;
}

// ------------------------------------------------------------------
// Utilidades
// ------------------------------------------------------------------

function formatearCiudad(nombre) {
    return nombre
        .replace(/_/g, " ")
        .replace(/\b\w/g, (l) => l.toUpperCase());
}

function limpiarMensajes(contenedor) {
    const errores = contenedor.querySelectorAll(".mensaje-error, .mensaje-exito");
    errores.forEach((el) => el.remove());
}

function mostrarError(idContenedor, mensaje) {
    const el = document.getElementById(idContenedor);
    if (el) el.innerHTML = `<p class="mensaje-error">${mensaje}</p>`;
}

// ------------------------------------------------------------------
// Inicializacion
// ------------------------------------------------------------------

(async () => {
    await cargarCiudades();
})();
