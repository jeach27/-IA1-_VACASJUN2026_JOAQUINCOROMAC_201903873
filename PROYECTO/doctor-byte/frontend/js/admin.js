// admin.js
// Logica del panel de administracion de Doctor Byte.
// Gestionamos CRUD de sintomas, fallas, recomendaciones y reglas de inferencia,
// ademas de la configuracion del bot de Telegram.

const API = '';

// Estado interno
let seccionActiva = 'sintomas';
let editandoSintoma = null;
let editandoFalla = null;
let editandoRegla = null;
let cacheSintomas = [];
let cacheFallas = [];


// =============================================================================
// UTILIDADES
// =============================================================================

function mostrarNotificacion(mensaje, tipo = 'exito') {
  const el = document.getElementById('notificacion');
  el.textContent = mensaje;
  el.className = `notificacion notificacion--${tipo}`;
  setTimeout(() => {
    el.className = 'notificacion notificacion--oculta';
  }, 3500);
}

async function apiFetch(url, opciones = {}) {
  const respuesta = await fetch(API + url, {
    headers: { 'Content-Type': 'application/json' },
    ...opciones,
  });
  const datos = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(datos.error || `Error HTTP ${respuesta.status}`);
  }
  return datos;
}

function confirmar(mensaje) {
  return window.confirm(mensaje);
}

function validarNombreProlog(nombre) {
  return /^[a-z][a-z0-9_]*$/.test(nombre);
}


// =============================================================================
// NAVEGACION
// =============================================================================

function cambiarSeccion(nombre) {
  document.querySelectorAll('.admin-seccion').forEach(s => s.classList.add('admin-seccion--oculta'));
  document.querySelectorAll('.sidebar-btn').forEach(b => b.classList.remove('active'));

  const seccion = document.getElementById(`seccion-${nombre}`);
  if (seccion) seccion.classList.remove('admin-seccion--oculta');

  const btn = document.querySelector(`.sidebar-btn[data-seccion="${nombre}"]`);
  if (btn) btn.classList.add('active');

  seccionActiva = nombre;
  cargarSeccion(nombre);
}

function cargarSeccion(nombre) {
  switch (nombre) {
    case 'sintomas':        cargarSintomas(); break;
    case 'fallas':          cargarFallas(); break;
    case 'recomendaciones': cargarRecomendaciones(); break;
    case 'reglas':          cargarReglas(); break;
    case 'asociaciones':    cargarAsociaciones(); break;
    case 'configuracion':   cargarConfiguracion(); break;
  }
}


// =============================================================================
// SINTOMAS
// =============================================================================

async function cargarSintomas() {
  const wrapper = document.getElementById('tabla-sintomas');
  wrapper.innerHTML = '<p class="cargando">Cargando sintomas...</p>';
  try {
    const datos = await apiFetch('/admin/sintomas');
    cacheSintomas = datos.sintomas;
    renderizarTablaSintomas(datos.sintomas);
  } catch (e) {
    wrapper.innerHTML = `<p class="error">${e.message}</p>`;
  }
}

function renderizarTablaSintomas(sintomas) {
  const wrapper = document.getElementById('tabla-sintomas');
  if (!sintomas.length) {
    wrapper.innerHTML = '<p class="admin-vacio">No hay sintomas registrados.</p>';
    return;
  }
  const tabla = document.createElement('table');
  tabla.className = 'admin-tabla';
  tabla.innerHTML = `
    <thead><tr>
      <th>Nombre (Prolog)</th>
      <th>Etiqueta visible</th>
      <th>Acciones</th>
    </tr></thead>`;
  const tbody = document.createElement('tbody');
  sintomas.forEach(s => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><code>${s.nombre}</code></td>
      <td>${s.etiqueta}</td>
      <td class="acciones-celda">
        <button class="btn-accion btn-accion--editar" data-nombre="${s.nombre}">Editar</button>
        <button class="btn-accion btn-accion--eliminar" data-nombre="${s.nombre}">Eliminar</button>
      </td>`;
    tbody.appendChild(tr);
  });
  tabla.appendChild(tbody);
  wrapper.innerHTML = '';
  wrapper.appendChild(tabla);

  wrapper.querySelectorAll('.btn-accion--editar').forEach(btn => {
    btn.addEventListener('click', () => abrirFormSintoma('editar', btn.dataset.nombre));
  });
  wrapper.querySelectorAll('.btn-accion--eliminar').forEach(btn => {
    btn.addEventListener('click', () => eliminarSintoma(btn.dataset.nombre));
  });
}

function abrirFormSintoma(modo, nombre = null) {
  const form = document.getElementById('form-sintoma');
  const titulo = document.getElementById('form-sintoma-titulo');

  if (modo === 'crear') {
    titulo.textContent = 'Nuevo sintoma';
    document.getElementById('sintoma-nombre-original').value = '';
    document.getElementById('sintoma-nombre').value = '';
    document.getElementById('sintoma-etiqueta').value = '';
    editandoSintoma = null;
  } else {
    const s = cacheSintomas.find(x => x.nombre === nombre);
    if (!s) return;
    titulo.textContent = 'Editar sintoma';
    document.getElementById('sintoma-nombre-original').value = s.nombre;
    document.getElementById('sintoma-nombre').value = s.nombre;
    document.getElementById('sintoma-etiqueta').value = s.etiqueta;
    editandoSintoma = s.nombre;
  }
  form.classList.remove('admin-form--oculto');
  document.getElementById('sintoma-nombre').focus();
}

function cerrarFormSintoma() {
  document.getElementById('form-sintoma').classList.add('admin-form--oculto');
  editandoSintoma = null;
}

async function guardarSintoma() {
  const nombre = document.getElementById('sintoma-nombre').value.trim();
  const etiqueta = document.getElementById('sintoma-etiqueta').value.trim();
  const nombreOriginal = document.getElementById('sintoma-nombre-original').value;

  if (!nombre || !etiqueta) {
    mostrarNotificacion('El nombre y la etiqueta son obligatorios.', 'error');
    return;
  }
  if (!validarNombreProlog(nombre)) {
    mostrarNotificacion('El nombre debe empezar con letra minuscula y solo contener letras, digitos y guion bajo.', 'error');
    return;
  }

  try {
    if (editandoSintoma) {
      await apiFetch(`/admin/sintomas/${nombreOriginal}`, {
        method: 'PUT',
        body: JSON.stringify({ nombre, etiqueta }),
      });
      mostrarNotificacion('Sintoma actualizado correctamente.');
    } else {
      await apiFetch('/admin/sintomas', {
        method: 'POST',
        body: JSON.stringify({ nombre, etiqueta }),
      });
      mostrarNotificacion('Sintoma creado correctamente.');
    }
    cerrarFormSintoma();
    cargarSintomas();
  } catch (e) {
    mostrarNotificacion(e.message, 'error');
  }
}

async function eliminarSintoma(nombre) {
  if (!confirmar(`¿Eliminar el sintoma "${nombre}"? Las reglas que lo usen tambien se veran afectadas.`)) return;
  try {
    await apiFetch(`/admin/sintomas/${nombre}`, { method: 'DELETE' });
    mostrarNotificacion('Sintoma eliminado.');
    cargarSintomas();
  } catch (e) {
    mostrarNotificacion(e.message, 'error');
  }
}


// =============================================================================
// FALLAS
// =============================================================================

async function cargarFallas() {
  const wrapper = document.getElementById('tabla-fallas');
  wrapper.innerHTML = '<p class="cargando">Cargando fallas...</p>';
  try {
    const datos = await apiFetch('/admin/fallas');
    cacheFallas = datos.fallas;
    renderizarTablaFallas(datos.fallas);
  } catch (e) {
    wrapper.innerHTML = `<p class="error">${e.message}</p>`;
  }
}

function renderizarTablaFallas(fallas) {
  const wrapper = document.getElementById('tabla-fallas');
  if (!fallas.length) {
    wrapper.innerHTML = '<p class="admin-vacio">No hay fallas registradas.</p>';
    return;
  }
  const tabla = document.createElement('table');
  tabla.className = 'admin-tabla';
  tabla.innerHTML = `
    <thead><tr>
      <th>Nombre (Prolog)</th>
      <th>Etiqueta visible</th>
      <th>Acciones</th>
    </tr></thead>`;
  const tbody = document.createElement('tbody');
  fallas.forEach(f => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><code>${f.nombre}</code></td>
      <td>${f.etiqueta}</td>
      <td class="acciones-celda">
        <button class="btn-accion btn-accion--editar" data-nombre="${f.nombre}">Editar</button>
        <button class="btn-accion btn-accion--eliminar" data-nombre="${f.nombre}">Eliminar</button>
      </td>`;
    tbody.appendChild(tr);
  });
  tabla.appendChild(tbody);
  wrapper.innerHTML = '';
  wrapper.appendChild(tabla);

  wrapper.querySelectorAll('.btn-accion--editar').forEach(btn => {
    btn.addEventListener('click', () => abrirFormFalla('editar', btn.dataset.nombre));
  });
  wrapper.querySelectorAll('.btn-accion--eliminar').forEach(btn => {
    btn.addEventListener('click', () => eliminarFalla(btn.dataset.nombre));
  });
}

function abrirFormFalla(modo, nombre = null) {
  const form = document.getElementById('form-falla');
  const titulo = document.getElementById('form-falla-titulo');

  if (modo === 'crear') {
    titulo.textContent = 'Nueva falla';
    document.getElementById('falla-nombre-original').value = '';
    document.getElementById('falla-nombre').value = '';
    document.getElementById('falla-etiqueta').value = '';
    editandoFalla = null;
  } else {
    const f = cacheFallas.find(x => x.nombre === nombre);
    if (!f) return;
    titulo.textContent = 'Editar falla';
    document.getElementById('falla-nombre-original').value = f.nombre;
    document.getElementById('falla-nombre').value = f.nombre;
    document.getElementById('falla-etiqueta').value = f.etiqueta;
    editandoFalla = f.nombre;
  }
  form.classList.remove('admin-form--oculto');
  document.getElementById('falla-nombre').focus();
}

function cerrarFormFalla() {
  document.getElementById('form-falla').classList.add('admin-form--oculto');
  editandoFalla = null;
}

async function guardarFalla() {
  const nombre = document.getElementById('falla-nombre').value.trim();
  const etiqueta = document.getElementById('falla-etiqueta').value.trim();
  const nombreOriginal = document.getElementById('falla-nombre-original').value;

  if (!nombre || !etiqueta) {
    mostrarNotificacion('El nombre y la etiqueta son obligatorios.', 'error');
    return;
  }
  if (!validarNombreProlog(nombre)) {
    mostrarNotificacion('El nombre debe empezar con letra minuscula y solo contener letras, digitos y guion bajo.', 'error');
    return;
  }

  try {
    if (editandoFalla) {
      await apiFetch(`/admin/fallas/${nombreOriginal}`, {
        method: 'PUT',
        body: JSON.stringify({ nombre, etiqueta }),
      });
      mostrarNotificacion('Falla actualizada correctamente.');
    } else {
      await apiFetch('/admin/fallas', {
        method: 'POST',
        body: JSON.stringify({ nombre, etiqueta }),
      });
      mostrarNotificacion('Falla creada correctamente.');
    }
    cerrarFormFalla();
    cargarFallas();
  } catch (e) {
    mostrarNotificacion(e.message, 'error');
  }
}

async function eliminarFalla(nombre) {
  if (!confirmar(`¿Eliminar la falla "${nombre}"? Las reglas asociadas tambien se veran afectadas.`)) return;
  try {
    await apiFetch(`/admin/fallas/${nombre}`, { method: 'DELETE' });
    mostrarNotificacion('Falla eliminada.');
    cargarFallas();
  } catch (e) {
    mostrarNotificacion(e.message, 'error');
  }
}


// =============================================================================
// RECOMENDACIONES
// =============================================================================

async function cargarRecomendaciones() {
  const wrapper = document.getElementById('tabla-recomendaciones');
  wrapper.innerHTML = '<p class="cargando">Cargando recomendaciones...</p>';
  try {
    const datos = await apiFetch('/admin/recomendaciones');
    renderizarTablaRecomendaciones(datos.recomendaciones);
  } catch (e) {
    wrapper.innerHTML = `<p class="error">${e.message}</p>`;
  }
}

function renderizarTablaRecomendaciones(recomendaciones) {
  const wrapper = document.getElementById('tabla-recomendaciones');
  if (!recomendaciones.length) {
    wrapper.innerHTML = '<p class="admin-vacio">No hay recomendaciones registradas.</p>';
    return;
  }
  const tabla = document.createElement('table');
  tabla.className = 'admin-tabla';
  tabla.innerHTML = `
    <thead><tr>
      <th>Falla</th>
      <th>Recomendacion</th>
      <th>Acciones</th>
    </tr></thead>`;
  const tbody = document.createElement('tbody');
  recomendaciones.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><code>${r.falla}</code></td>
      <td class="celda-texto">${r.texto}</td>
      <td class="acciones-celda">
        <button class="btn-accion btn-accion--editar" data-falla="${r.falla}">Editar</button>
      </td>`;
    tbody.appendChild(tr);
  });
  tabla.appendChild(tbody);
  wrapper.innerHTML = '';
  wrapper.appendChild(tabla);

  wrapper.querySelectorAll('.btn-accion--editar').forEach(btn => {
    btn.addEventListener('click', () => abrirFormRecomendacion(btn.dataset.falla));
  });
}

function abrirFormRecomendacion(falla) {
  const wrapper = document.getElementById('tabla-recomendaciones');
  const filas = wrapper.querySelectorAll('tbody tr');
  let textoActual = '';
  filas.forEach(tr => {
    const cod = tr.querySelector('code');
    if (cod && cod.textContent === falla) {
      textoActual = tr.querySelector('.celda-texto').textContent;
    }
  });

  document.getElementById('rec-falla').value = falla;
  document.getElementById('rec-falla-nombre').textContent = falla;
  document.getElementById('rec-texto').value = textoActual;
  document.getElementById('form-recomendacion').classList.remove('admin-form--oculto');
  document.getElementById('rec-texto').focus();
}

function cerrarFormRecomendacion() {
  document.getElementById('form-recomendacion').classList.add('admin-form--oculto');
}

async function guardarRecomendacion() {
  const falla = document.getElementById('rec-falla').value;
  const texto = document.getElementById('rec-texto').value.trim();

  if (!texto) {
    mostrarNotificacion('El texto de la recomendacion no puede estar vacio.', 'error');
    return;
  }

  try {
    await apiFetch(`/admin/recomendaciones/${falla}`, {
      method: 'PUT',
      body: JSON.stringify({ texto }),
    });
    mostrarNotificacion('Recomendacion actualizada correctamente.');
    cerrarFormRecomendacion();
    cargarRecomendaciones();
  } catch (e) {
    mostrarNotificacion(e.message, 'error');
  }
}


// =============================================================================
// REGLAS
// =============================================================================

async function cargarReglas() {
  const wrapper = document.getElementById('tabla-reglas');
  wrapper.innerHTML = '<p class="cargando">Cargando reglas...</p>';
  try {
    // Cargamos sintomas y fallas en paralelo para los selectores del formulario
    const [datosReglas, datosSintomas, datosFallas] = await Promise.all([
      apiFetch('/admin/reglas'),
      apiFetch('/admin/sintomas'),
      apiFetch('/admin/fallas'),
    ]);
    cacheSintomas = datosSintomas.sintomas;
    cacheFallas = datosFallas.fallas;
    renderizarTablaReglas(datosReglas.reglas);
  } catch (e) {
    wrapper.innerHTML = `<p class="error">${e.message}</p>`;
  }
}

function renderizarTablaReglas(reglas) {
  const wrapper = document.getElementById('tabla-reglas');
  if (!reglas.length) {
    wrapper.innerHTML = '<p class="admin-vacio">No hay reglas de inferencia registradas.</p>';
    return;
  }

  wrapper.innerHTML = '';
  reglas.forEach(r => {
    const card = document.createElement('div');
    card.className = 'regla-card';

    const reqTexto = r.sintomas_requeridos.length
      ? r.sintomas_requeridos.map(s => `<code>${s}</code>`).join(', ')
      : '<em>ninguno</em>';
    const negTexto = r.sintomas_negados.length
      ? r.sintomas_negados.map(s => `<code>${s}</code>`).join(', ')
      : '<em>ninguno</em>';

    card.innerHTML = `
      <div class="regla-card__encabezado">
        <span class="regla-card__id">${r.id}</span>
        <span class="regla-card__falla">${r.falla}</span>
        <div class="regla-card__acciones">
          <button class="btn-accion btn-accion--editar" data-id="${r.id}">Editar</button>
          <button class="btn-accion btn-accion--eliminar" data-id="${r.id}">Eliminar</button>
        </div>
      </div>
      <p class="regla-card__descripcion">${r.descripcion || '(sin descripcion)'}</p>
      <div class="regla-card__detalle">
        <span><strong>Requeridos:</strong> ${reqTexto}</span>
        <span><strong>Negados:</strong> ${negTexto}</span>
        <span><strong>Corte:</strong> ${r.usa_corte ? 'si' : 'no'}</span>
      </div>`;

    wrapper.appendChild(card);
  });

  wrapper.querySelectorAll('.btn-accion--editar').forEach(btn => {
    btn.addEventListener('click', () => abrirFormRegla('editar', btn.dataset.id));
  });
  wrapper.querySelectorAll('.btn-accion--eliminar').forEach(btn => {
    btn.addEventListener('click', () => eliminarRegla(btn.dataset.id));
  });
}

async function abrirFormRegla(modo, idRegla = null) {
  // Aseguramos que los caches esten cargados
  if (!cacheSintomas.length || !cacheFallas.length) {
    const [ds, df] = await Promise.all([apiFetch('/admin/sintomas'), apiFetch('/admin/fallas')]);
    cacheSintomas = ds.sintomas;
    cacheFallas = df.fallas;
  }

  const form = document.getElementById('form-regla');
  const titulo = document.getElementById('form-regla-titulo');

  // Poblar select de fallas
  const selectFalla = document.getElementById('regla-falla');
  selectFalla.innerHTML = '';
  cacheFallas.forEach(f => {
    const opt = document.createElement('option');
    opt.value = f.nombre;
    opt.textContent = `${f.nombre} — ${f.etiqueta}`;
    selectFalla.appendChild(opt);
  });

  // Poblar checkboxes de sintomas requeridos y negados
  poblarSelectorSintomas('regla-sintomas-req', []);
  poblarSelectorSintomas('regla-sintomas-neg', []);

  if (modo === 'crear') {
    titulo.textContent = 'Nueva regla de inferencia';
    document.getElementById('regla-id').value = '';
    document.getElementById('regla-corte').checked = true;
    document.getElementById('regla-descripcion').value = '';
    editandoRegla = null;
  } else {
    const datos = await apiFetch('/admin/reglas');
    const regla = datos.reglas.find(r => r.id === idRegla);
    if (!regla) return;

    titulo.textContent = 'Editar regla de inferencia';
    document.getElementById('regla-id').value = regla.id;
    selectFalla.value = regla.falla;
    document.getElementById('regla-corte').checked = regla.usa_corte;
    document.getElementById('regla-descripcion').value = regla.descripcion;

    poblarSelectorSintomas('regla-sintomas-req', regla.sintomas_requeridos);
    poblarSelectorSintomas('regla-sintomas-neg', regla.sintomas_negados);
    editandoRegla = regla.id;
  }

  form.classList.remove('admin-form--oculto');
  document.getElementById('regla-descripcion').focus();
}

function poblarSelectorSintomas(contenedorId, seleccionados) {
  const contenedor = document.getElementById(contenedorId);
  contenedor.innerHTML = '';
  cacheSintomas.forEach(s => {
    const item = document.createElement('label');
    item.className = 'selector-item';
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.value = s.nombre;
    cb.checked = seleccionados.includes(s.nombre);
    item.appendChild(cb);
    item.appendChild(document.createTextNode(` ${s.etiqueta}`));
    contenedor.appendChild(item);
  });
}

function obtenerSeleccionados(contenedorId) {
  const contenedor = document.getElementById(contenedorId);
  return Array.from(contenedor.querySelectorAll('input[type="checkbox"]:checked'))
    .map(cb => cb.value);
}

function cerrarFormRegla() {
  document.getElementById('form-regla').classList.add('admin-form--oculto');
  editandoRegla = null;
}

async function guardarRegla() {
  const falla = document.getElementById('regla-falla').value;
  const usaCorte = document.getElementById('regla-corte').checked;
  const descripcion = document.getElementById('regla-descripcion').value.trim();
  const sintomasReq = obtenerSeleccionados('regla-sintomas-req');
  const sintomasNeg = obtenerSeleccionados('regla-sintomas-neg');

  if (!falla) {
    mostrarNotificacion('Debes seleccionar una falla.', 'error');
    return;
  }
  if (!sintomasReq.length && !sintomasNeg.length) {
    mostrarNotificacion('La regla debe tener al menos un sintoma requerido o negado.', 'error');
    return;
  }

  const cuerpo = {
    falla,
    sintomas_requeridos: sintomasReq,
    sintomas_negados: sintomasNeg,
    usa_corte: usaCorte,
    descripcion,
  };

  try {
    if (editandoRegla) {
      await apiFetch(`/admin/reglas/${editandoRegla}`, {
        method: 'PUT',
        body: JSON.stringify(cuerpo),
      });
      mostrarNotificacion('Regla actualizada correctamente.');
    } else {
      await apiFetch('/admin/reglas', {
        method: 'POST',
        body: JSON.stringify(cuerpo),
      });
      mostrarNotificacion('Regla creada correctamente.');
    }
    cerrarFormRegla();
    cargarReglas();
  } catch (e) {
    mostrarNotificacion(e.message, 'error');
  }
}

async function eliminarRegla(id) {
  if (!confirmar(`¿Eliminar la regla "${id}"? Esta accion no se puede deshacer.`)) return;
  try {
    await apiFetch(`/admin/reglas/${id}`, { method: 'DELETE' });
    mostrarNotificacion('Regla eliminada.');
    cargarReglas();
  } catch (e) {
    mostrarNotificacion(e.message, 'error');
  }
}


// =============================================================================
// ASOCIACIONES
// =============================================================================

async function cargarAsociaciones() {
  const wrapper = document.getElementById('contenido-asociaciones');
  wrapper.innerHTML = '<p class="cargando">Cargando asociaciones...</p>';
  try {
    const datos = await apiFetch('/admin/asociaciones');
    renderizarAsociaciones(datos.asociaciones);
  } catch (e) {
    wrapper.innerHTML = `<p class="error">${e.message}</p>`;
  }
}

function renderizarAsociaciones(asociaciones) {
  const wrapper = document.getElementById('contenido-asociaciones');
  if (!asociaciones.length) {
    wrapper.innerHTML = '<p class="admin-vacio">No hay asociaciones definidas todavia.</p>';
    return;
  }
  wrapper.innerHTML = '';
  asociaciones.forEach(a => {
    const card = document.createElement('div');
    card.className = 'asoc-card';

    const reglasHtml = a.reglas.map(r => {
      const reqHtml = r.sintomas_requeridos.length
        ? r.sintomas_requeridos.map(s => `<span class="etiqueta-sintoma etiqueta-sintoma--req" title="${s.nombre}">${s.etiqueta}</span>`).join('')
        : '<em>ninguno</em>';
      const negHtml = r.sintomas_negados.length
        ? r.sintomas_negados.map(s => `<span class="etiqueta-sintoma etiqueta-sintoma--neg" title="${s.nombre}">NO ${s.etiqueta}</span>`).join('')
        : '';
      return `<div class="asoc-regla">
        <span class="asoc-regla__id">${r.id}</span>
        <div class="asoc-regla__sintomas">${reqHtml}${negHtml}</div>
      </div>`;
    }).join('');

    card.innerHTML = `
      <div class="asoc-card__encabezado">
        <span class="asoc-card__falla">${a.etiqueta_falla}</span>
        <code class="asoc-card__falla-id">${a.falla}</code>
      </div>
      <div class="asoc-card__reglas">${reglasHtml}</div>
      ${a.recomendacion
        ? `<div class="asoc-card__rec"><strong>Recomendacion:</strong> ${a.recomendacion}</div>`
        : '<div class="asoc-card__rec asoc-card__rec--vacia">Sin recomendacion configurada</div>'
      }`;
    wrapper.appendChild(card);
  });
}


// =============================================================================
// CONFIGURACION DEL BOT
// =============================================================================

async function cargarConfiguracion() {
  try {
    const cfg = await apiFetch('/admin/configuracion');
    document.getElementById('cfg-chat-id').value = cfg.chat_id || '';
    document.getElementById('cfg-habilitado').checked = cfg.habilitado !== false;
    document.getElementById('cfg-msg-bienvenida').value = cfg.mensajes?.bienvenida || '';
    document.getElementById('cfg-msg-sin-diagnostico').value = cfg.mensajes?.sin_diagnostico || '';
  } catch (e) {
    mostrarNotificacion('No se pudo cargar la configuracion del bot.', 'error');
  }
}

async function guardarConfiguracion() {
  const chatId = document.getElementById('cfg-chat-id').value.trim();
  const habilitado = document.getElementById('cfg-habilitado').checked;
  const msgBienvenida = document.getElementById('cfg-msg-bienvenida').value.trim();
  const msgSinDiag = document.getElementById('cfg-msg-sin-diagnostico').value.trim();

  try {
    await apiFetch('/admin/configuracion', {
      method: 'PUT',
      body: JSON.stringify({
        chat_id: chatId,
        habilitado,
        mensajes: {
          bienvenida: msgBienvenida,
          sin_diagnostico: msgSinDiag,
        },
      }),
    });
    mostrarNotificacion('Configuracion del bot guardada correctamente.');
  } catch (e) {
    mostrarNotificacion(e.message, 'error');
  }
}


// =============================================================================
// EVENTOS
// =============================================================================

document.querySelectorAll('.sidebar-btn').forEach(btn => {
  btn.addEventListener('click', () => cambiarSeccion(btn.dataset.seccion));
});

// Sintomas
document.getElementById('btn-nuevo-sintoma').addEventListener('click', () => abrirFormSintoma('crear'));
document.getElementById('btn-guardar-sintoma').addEventListener('click', guardarSintoma);
document.getElementById('btn-cancelar-sintoma').addEventListener('click', cerrarFormSintoma);

// Fallas
document.getElementById('btn-nueva-falla').addEventListener('click', () => abrirFormFalla('crear'));
document.getElementById('btn-guardar-falla').addEventListener('click', guardarFalla);
document.getElementById('btn-cancelar-falla').addEventListener('click', cerrarFormFalla);

// Recomendaciones
document.getElementById('btn-guardar-rec').addEventListener('click', guardarRecomendacion);
document.getElementById('btn-cancelar-rec').addEventListener('click', cerrarFormRecomendacion);

// Reglas
document.getElementById('btn-nueva-regla').addEventListener('click', () => abrirFormRegla('crear'));
document.getElementById('btn-guardar-regla').addEventListener('click', guardarRegla);
document.getElementById('btn-cancelar-regla').addEventListener('click', cerrarFormRegla);

// Configuracion
document.getElementById('btn-guardar-config').addEventListener('click', guardarConfiguracion);


// =============================================================================
// INICIO
// =============================================================================

cargarSintomas();
