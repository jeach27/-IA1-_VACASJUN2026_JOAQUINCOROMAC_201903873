const API = 'http://localhost:5000/api';

let estadoActual = null;
let modoSimulacion = 'automatico';
let intervaloAuto = null;
let pasoEnCurso = false;

// ---------------------------------------------------------------------------
// Inicializacion
// ---------------------------------------------------------------------------

window.addEventListener('load', async () => {
    await cargarDificultadActual();
    await cargarMapaInicial();
    await cargarHistorial();
});

async function cargarDificultadActual() {
    try {
        const resp = await fetch(`${API}/dificultad`);
        const data = await resp.json();
        const radio = document.querySelector(`input[name="dificultad"][value="${data.actual}"]`);
        if (radio) radio.checked = true;
    } catch (e) {}
}

async function cambiarDificultad(nivel) {
    if (estadoActual && estadoActual.activa) {
        mostrarMensaje('Detiene la simulacion antes de cambiar la dificultad.');
        const radio = document.querySelector(`input[name="dificultad"][value="${estadoActual._dificultad || 'medio'}"]`);
        if (radio) radio.checked = true;
        return;
    }
    try {
        const resp = await fetch(`${API}/dificultad`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nivel })
        });
        if (!resp.ok) {
            const err = await resp.json();
            mostrarMensaje(err.error || 'Error al cambiar dificultad.');
            return;
        }
        mostrarMensaje(`Dificultad cambiada a: ${nivel.toUpperCase()}`);
        await cargarMapaInicial();
    } catch (e) {
        mostrarMensaje('Error al cambiar la dificultad.');
    }
}

async function cargarMapaInicial() {
    try {
        const resp = await fetch(`${API}/mapa/inicial`);
        const data = await resp.json();
        estadoActual = {
            dimension: data.dimension,
            robots: data.robots.map(r => ({ ...r, lleva_paquete: false, paquete_id: null })),
            paquetes: data.paquetes.map(p => ({ ...p, entregado: false, recogido: false })),
            obstaculos: data.obstaculos,
            zonas_entrega: data.zonas_entrega,
            movimientos: 0,
            entregas: 0,
            activa: false,
            pausada: false,
            completada: false
        };
        renderizarMapa(estadoActual);
        actualizarEstadoRobots(estadoActual.robots);
    } catch (e) {
        mostrarMensaje('No se pudo conectar con el backend. Verifica que este corriendo en el puerto 5000.');
    }
}

// ---------------------------------------------------------------------------
// Controles principales
// ---------------------------------------------------------------------------

async function iniciarSimulacion() {
    try {
        const resp = await fetch(`${API}/simulacion/iniciar`, { method: 'POST' });
        const data = await resp.json();
        estadoActual = data.estado;

        renderizarMapa(estadoActual);
        actualizarEstadoRobots(estadoActual.robots);
        actualizarEstadisticasDesdeEstado(estadoActual);

        document.getElementById('btn-iniciar').disabled = true;
        document.getElementById('btn-pausar').disabled = false;
        document.getElementById('btn-reiniciar').disabled = false;
        document.getElementById('btn-paso').disabled = modoSimulacion !== 'paso_a_paso';

        limpiarLog();
        mostrarMensaje('Simulacion iniciada.');

        if (modoSimulacion === 'automatico') {
            iniciarAutomatico();
        }
    } catch (e) {
        mostrarMensaje('Error al iniciar la simulacion.');
    }
}

async function ejecutarPaso() {
    if (pasoEnCurso) return;
    pasoEnCurso = true;

    try {
        const resp = await fetch(`${API}/simulacion/paso`);
        const data = await resp.json();

        estadoActual = data.estado;
        renderizarMapa(estadoActual);
        actualizarEstadoRobots(estadoActual.robots);
        await actualizarEstadisticas();
        registrarAccionesEnLog(data.acciones);

        if (data.completado) {
            detenerAutomatico();
            mostrarMensaje('Simulacion completada. Todos los paquetes entregados.', true);
            document.getElementById('btn-iniciar').disabled = false;
            document.getElementById('btn-pausar').disabled = true;
            document.getElementById('btn-paso').disabled = true;
            await cargarHistorial();
        }
    } catch (e) {
        mostrarMensaje('Error al ejecutar paso.');
        detenerAutomatico();
    } finally {
        pasoEnCurso = false;
    }
}

function iniciarAutomatico() {
    detenerAutomatico();
    const velocidad = parseInt(document.getElementById('velocidad').value) || 600;
    intervaloAuto = setInterval(async () => {
        if (estadoActual && !estadoActual.pausada) {
            await ejecutarPaso();
        }
    }, velocidad);
}

function detenerAutomatico() {
    if (intervaloAuto) {
        clearInterval(intervaloAuto);
        intervaloAuto = null;
    }
}

async function pausarSimulacion() {
    try {
        const resp = await fetch(`${API}/simulacion/pausar`, { method: 'POST' });
        const data = await resp.json();
        estadoActual.pausada = data.pausado;

        const btnPausar = document.getElementById('btn-pausar');
        btnPausar.textContent = data.pausado ? 'Reanudar' : 'Pausar';
        mostrarMensaje(data.pausado ? 'Simulacion pausada.' : 'Simulacion reanudada.');
    } catch (e) {
        mostrarMensaje('Error al pausar.');
    }
}

async function reiniciarSimulacion() {
    detenerAutomatico();

    try {
        const resp = await fetch(`${API}/simulacion/reiniciar`, { method: 'POST' });
        const data = await resp.json();
        estadoActual = data.estado;

        renderizarMapa(estadoActual);
        actualizarEstadoRobots(estadoActual.robots);
        actualizarEstadisticasDesdeEstado(estadoActual);
        limpiarLog();

        document.getElementById('btn-iniciar').disabled = true;
        document.getElementById('btn-pausar').disabled = false;
        document.getElementById('btn-pausar').textContent = 'Pausar';
        document.getElementById('btn-paso').disabled = modoSimulacion !== 'paso_a_paso';

        mostrarMensaje('Simulacion reiniciada.');
        await cargarHistorial();

        if (modoSimulacion === 'automatico') {
            iniciarAutomatico();
        }
    } catch (e) {
        mostrarMensaje('Error al reiniciar.');
    }
}

async function cambiarModo(modo) {
    modoSimulacion = modo;
    const btnPaso = document.getElementById('btn-paso');
    const btnPausar = document.getElementById('btn-pausar');

    if (modo === 'paso_a_paso') {
        detenerAutomatico();
        btnPausar.disabled = true;
        btnPausar.textContent = 'Pausar';

        // Si la simulacion estaba pausada en automatico, despausar para que
        // paso a paso pueda ejecutar; el backend rechaza pasos cuando pausada=true
        if (estadoActual && estadoActual.pausada) {
            try {
                const resp = await fetch(`${API}/simulacion/pausar`, { method: 'POST' });
                const data = await resp.json();
                estadoActual.pausada = data.pausado;
            } catch (e) {}
        }

        const simulacionActiva = estadoActual && estadoActual.activa && !estadoActual.completada;
        btnPaso.disabled = !simulacionActiva;

    } else {
        // modo automatico
        btnPaso.disabled = true;

        const simulacionActiva = estadoActual && estadoActual.activa && !estadoActual.completada;
        if (simulacionActiva) {
            btnPausar.disabled = false;
            btnPausar.textContent = 'Pausar';

            // Si por algun motivo el backend quedara pausado al entrar en automatico,
            // sincronizar para que el loop pueda ejecutar pasos
            if (estadoActual.pausada) {
                try {
                    const resp = await fetch(`${API}/simulacion/pausar`, { method: 'POST' });
                    const data = await resp.json();
                    estadoActual.pausada = data.pausado;
                } catch (e) {}
            }

            iniciarAutomatico();
        }
    }
}

// ---------------------------------------------------------------------------
// Renderizado del mapa
// ---------------------------------------------------------------------------

function renderizarMapa(estado) {
    const contenedor = document.getElementById('mapa');
    const filas = estado.dimension.filas;
    const columnas = estado.dimension.columnas;

    contenedor.style.gridTemplateColumns = `repeat(${columnas}, 46px)`;
    contenedor.style.gridTemplateRows = `repeat(${filas}, 46px)`;
    contenedor.innerHTML = '';

    const mapaClases = construirMatrizMapa(estado, filas, columnas);

    for (let f = 1; f <= filas; f++) {
        for (let c = 1; c <= columnas; c++) {
            const celda = document.createElement('div');
            const info = mapaClases[f][c];
            celda.className = `celda ${info.clase}`;
            celda.textContent = info.texto;
            celda.title = `Fila ${f}, Col ${c}${info.titulo ? ' - ' + info.titulo : ''}`;
            contenedor.appendChild(celda);
        }
    }
}

function construirMatrizMapa(estado, filas, columnas) {
    const mapa = {};
    for (let f = 1; f <= filas; f++) {
        mapa[f] = {};
        for (let c = 1; c <= columnas; c++) {
            mapa[f][c] = { clase: 'celda-vacia', texto: '.', titulo: '' };
        }
    }

    for (const obs of estado.obstaculos) {
        mapa[obs.fila][obs.columna] = { clase: 'celda-obstaculo', texto: 'X', titulo: 'Obstaculo' };
    }

    for (const zona of estado.zonas_entrega) {
        mapa[zona.fila][zona.columna] = { clase: 'celda-zona', texto: 'E', titulo: `Zona ${zona.id}` };
    }

    for (const paq of estado.paquetes) {
        if (!paq.entregado && !paq.recogido) {
            mapa[paq.fila][paq.columna] = { clase: 'celda-paquete', texto: paq.id.toUpperCase(), titulo: `Paquete ${paq.id}` };
        }
    }

    for (const robot of estado.robots) {
        const actual = mapa[robot.fila][robot.columna];
        if (actual.clase === 'celda-zona') {
            mapa[robot.fila][robot.columna] = {
                clase: 'celda-robot-zona',
                texto: robot.lleva_paquete ? 'R+P' : 'R',
                titulo: `Robot ${robot.id}${robot.lleva_paquete ? ' (lleva ' + robot.paquete_id + ')' : ''}`
            };
        } else if (robot.lleva_paquete) {
            mapa[robot.fila][robot.columna] = {
                clase: 'celda-robot-paquete',
                texto: 'R+P',
                titulo: `Robot ${robot.id} lleva ${robot.paquete_id}`
            };
        } else {
            mapa[robot.fila][robot.columna] = {
                clase: 'celda-robot',
                texto: robot.id.toUpperCase(),
                titulo: `Robot ${robot.id}`
            };
        }
    }

    return mapa;
}

// ---------------------------------------------------------------------------
// Estadisticas
// ---------------------------------------------------------------------------

async function actualizarEstadisticas() {
    try {
        const resp = await fetch(`${API}/estadisticas`);
        const stats = await resp.json();
        document.getElementById('stat-movimientos').textContent = stats.movimientos;
        document.getElementById('stat-entregas').textContent = stats.entregas;
        document.getElementById('stat-pendientes').textContent = stats.pendientes;
        document.getElementById('stat-tiempo').textContent = `${stats.tiempo_segundos}s`;
        document.getElementById('stat-eficiencia').textContent = `${stats.eficiencia}%`;
    } catch (e) {}
}

function actualizarEstadisticasDesdeEstado(estado) {
    const total = estado.paquetes ? estado.paquetes.length : 5;
    document.getElementById('stat-movimientos').textContent = estado.movimientos || 0;
    document.getElementById('stat-entregas').textContent = estado.entregas || 0;
    document.getElementById('stat-pendientes').textContent = total - (estado.entregas || 0);
    document.getElementById('stat-tiempo').textContent = '0s';
    document.getElementById('stat-eficiencia').textContent = '0%';
}

// ---------------------------------------------------------------------------
// Log de acciones
// ---------------------------------------------------------------------------

function registrarAccionesEnLog(acciones) {
    const contenedor = document.getElementById('log-acciones');
    for (const acc of acciones) {
        const linea = document.createElement('div');
        const clase = `log-linea accion-${acc.accion.replace('_paquete', '')}`;
        linea.className = clase;
        const paq = acc.paquete ? ` [${acc.paquete}]` : '';
        linea.textContent = `${acc.robot}: ${acc.accion}${paq}`;
        contenedor.prepend(linea);
    }
}

function limpiarLog() {
    document.getElementById('log-acciones').innerHTML = '';
}

// ---------------------------------------------------------------------------
// Estado de robots
// ---------------------------------------------------------------------------

function actualizarEstadoRobots(robots) {
    const contenedor = document.getElementById('estado-robots');
    contenedor.innerHTML = '';
    for (const r of robots) {
        const div = document.createElement('div');
        div.className = 'robot-info';
        const paquete = r.lleva_paquete ? `Lleva: ${r.paquete_id}` : 'Sin carga';
        div.textContent = `${r.id.toUpperCase()} | Fila: ${r.fila} Col: ${r.columna} | ${paquete}`;
        contenedor.appendChild(div);
    }
}

// ---------------------------------------------------------------------------
// Historial
// ---------------------------------------------------------------------------

async function cargarHistorial() {
    try {
        const resp = await fetch(`${API}/historial`);
        const lista = await resp.json();
        const tbody = document.getElementById('historial-body');
        tbody.innerHTML = '';

        if (lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="sin-datos">Sin simulaciones registradas</td></tr>';
            return;
        }

        for (const sim of lista.reverse()) {
            const tr = document.createElement('tr');
            const claseResultado = sim.resultado === 'completada' ? 'resultado-completada' : 'resultado-cancelada';
            const claseDif = `dif-${sim.dificultad || 'medio'}`;
            tr.innerHTML = `
                <td>${sim.id.substring(0, 8)}...</td>
                <td>${sim.fecha}</td>
                <td class="${claseDif}">${sim.dificultad || 'medio'}</td>
                <td>${sim.movimientos}</td>
                <td>${sim.entregas}</td>
                <td>${sim.tiempo_segundos}</td>
                <td class="${claseResultado}">${sim.resultado}</td>
            `;
            tbody.appendChild(tr);
        }
    } catch (e) {}
}

// ---------------------------------------------------------------------------
// Reporte PDF
// ---------------------------------------------------------------------------

async function descargarReporte() {
    const btn = document.getElementById('btn-reporte');
    btn.disabled = true;
    btn.textContent = 'Generando...';
    try {
        const resp = await fetch(`${API}/reporte`);
        if (!resp.ok) {
            mostrarMensaje('Error al generar el reporte.');
            return;
        }
        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `reporte_smart_warehouse_${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        mostrarMensaje('Reporte descargado correctamente.');
    } catch (e) {
        mostrarMensaje('Error al descargar el reporte.');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Descargar Reporte PDF';
    }
}

// ---------------------------------------------------------------------------
// Mensaje de estado
// ---------------------------------------------------------------------------

let timeoutMensaje = null;

function mostrarMensaje(texto, esCompletado = false) {
    const el = document.getElementById('mensaje-estado');
    el.textContent = texto;
    el.className = `mensaje-estado${esCompletado ? ' completado' : ''}`;

    if (timeoutMensaje) clearTimeout(timeoutMensaje);
    timeoutMensaje = setTimeout(() => {
        el.classList.add('oculto');
    }, 3500);
}