const API = '';

function obtenerToken() {
  const token = sessionStorage.getItem('token');
  if (!token) {
    window.location.href = 'login.html';
    return null;
  }
  return token;
}

async function apiFetch(ruta, opciones = {}) {
  const token = obtenerToken();
  if (!token) return null;

  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${token}`, ...(opciones.headers || {}) };
  const respuesta = await fetch(`${API}${ruta}`, { ...opciones, headers });

  if (respuesta.status === 401) {
    sessionStorage.removeItem('token');
    window.location.href = 'login.html';
    return null;
  }

  if (!respuesta.ok) {
    const error = await respuesta.json().catch(() => ({ detail: 'Error desconocido' }));
    throw new Error(error.detail || `Error ${respuesta.status}`);
  }

  if (respuesta.status === 204) return null;
  return respuesta.json();
}

// --- Seccion activa en sidebar ---
function marcarSeccionActiva(seccion) {
  document.querySelectorAll('.sidebar nav a').forEach(a => {
    a.classList.toggle('activo', a.dataset.seccion === seccion);
  });
  document.querySelectorAll('.seccion').forEach(s => {
    s.classList.toggle('hidden', s.id !== `seccion-${seccion}`);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  if (!obtenerToken()) return;

  // Logout
  document.getElementById('btn-logout')?.addEventListener('click', () => {
    sessionStorage.removeItem('token');
    window.location.href = 'login.html';
  });

  // Navegacion
  document.querySelectorAll('.sidebar nav a[data-seccion]').forEach(a => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const sec = a.dataset.seccion;
      marcarSeccionActiva(sec);
      cargarSeccion(sec);
    });
  });

  marcarSeccionActiva('estadisticas');
  cargarSeccion('estadisticas');
});

function cargarSeccion(nombre) {
  switch (nombre) {
    case 'estadisticas': cargarEstadisticas(); break;
    case 'categorias': cargarCategorias(); break;
    case 'preguntas': cargarPreguntas(); break;
    case 'consultas': cargarConsultas(); break;
    case 'configuracion': cargarConfiguracion(); break;
  }
}

// --- Estadisticas ---
async function cargarEstadisticas() {
  try {
    const datos = await apiFetch('/estadisticas');
    if (!datos) return;

    document.getElementById('stat-total').textContent = datos.total_consultas;
    document.getElementById('stat-encontradas').textContent = datos.consultas_encontradas;
    document.getElementById('stat-no-encontradas').textContent = datos.consultas_no_encontradas;
    document.getElementById('stat-usuarios').textContent = datos.total_usuarios_unicos;
    document.getElementById('stat-preguntas').textContent = datos.total_preguntas;
    document.getElementById('stat-categorias').textContent = datos.total_categorias;

    const tablaTop = document.getElementById('tabla-top-preguntas');
    tablaTop.innerHTML = datos.preguntas_mas_consultadas.map(p =>
      `<tr><td>${escHtml(p.pregunta)}</td><td>${p.total}</td></tr>`
    ).join('') || '<tr><td colspan="2">Sin datos</td></tr>';
  } catch (err) {
    console.error('Error al cargar estadisticas:', err);
  }
}

// --- Categorias ---
let categorias = [];

async function cargarCategorias() {
  try {
    categorias = await apiFetch('/categorias') || [];
    renderizarCategorias();
  } catch (err) {
    mostrarAlerta('error-categorias', err.message);
  }
}

function renderizarCategorias() {
  const tbody = document.getElementById('tbody-categorias');
  tbody.innerHTML = categorias.map(c => `
    <tr>
      <td>${c.id}</td>
      <td>${escHtml(c.nombre)}</td>
      <td>${escHtml(c.descripcion || '')}</td>
      <td>
        <button class="btn btn-sm btn-secondary" onclick="abrirModalCategoria(${c.id})">Editar</button>
        <button class="btn btn-sm btn-danger" onclick="eliminarCategoria(${c.id})">Eliminar</button>
      </td>
    </tr>
  `).join('') || '<tr><td colspan="4">Sin categorias</td></tr>';
}

function abrirModalCategoria(id = null) {
  const modal = document.getElementById('modal-categoria');
  const cat = id ? categorias.find(c => c.id === id) : null;
  document.getElementById('modal-cat-titulo').textContent = id ? 'Editar categoria' : 'Nueva categoria';
  document.getElementById('cat-id').value = id || '';
  document.getElementById('cat-nombre').value = cat?.nombre || '';
  document.getElementById('cat-descripcion').value = cat?.descripcion || '';
  modal.classList.remove('hidden');
}

document.getElementById('modal-categoria')?.addEventListener('click', (e) => {
  if (e.target === e.currentTarget) e.currentTarget.classList.add('hidden');
});

document.getElementById('form-categoria')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('cat-id').value;
  const datos = {
    nombre: document.getElementById('cat-nombre').value.trim(),
    descripcion: document.getElementById('cat-descripcion').value.trim(),
  };

  try {
    if (id) {
      await apiFetch(`/categorias/${id}`, { method: 'PUT', body: JSON.stringify(datos) });
    } else {
      await apiFetch('/categorias', { method: 'POST', body: JSON.stringify(datos) });
    }
    document.getElementById('modal-categoria').classList.add('hidden');
    cargarCategorias();
  } catch (err) {
    mostrarAlerta('error-modal-cat', err.message);
  }
});

async function eliminarCategoria(id) {
  if (!confirm('Eliminar esta categoria?')) return;
  try {
    await apiFetch(`/categorias/${id}`, { method: 'DELETE' });
    cargarCategorias();
  } catch (err) {
    mostrarAlerta('error-categorias', err.message);
  }
}

// --- Preguntas ---
let preguntas = [];

async function cargarPreguntas() {
  try {
    [preguntas, categorias] = await Promise.all([
      apiFetch('/preguntas') || [],
      apiFetch('/categorias') || [],
    ]);
    llenarSelectCategorias('filtro-cat-pregunta');
    llenarSelectCategorias('pregunta-categoria');
    renderizarPreguntas(preguntas);
  } catch (err) {
    mostrarAlerta('error-preguntas', err.message);
  }
}

function llenarSelectCategorias(selectId) {
  const sel = document.getElementById(selectId);
  if (!sel) return;
  const valorActual = sel.value;
  const esOpcional = sel.id === 'filtro-cat-pregunta';
  sel.innerHTML = (esOpcional ? '<option value="">Todas las categorias</option>' : '<option value="">Sin categoria</option>') +
    categorias.map(c => `<option value="${c.id}">${escHtml(c.nombre)}</option>`).join('');
  sel.value = valorActual;
}

function renderizarPreguntas(lista) {
  const tbody = document.getElementById('tbody-preguntas');
  tbody.innerHTML = lista.map(p => `
    <tr>
      <td>${p.id}</td>
      <td>${escHtml(p.texto)}</td>
      <td>${escHtml(p.respuesta.substring(0, 80))}${p.respuesta.length > 80 ? '...' : ''}</td>
      <td>${escHtml(p.categoria?.nombre || '-')}</td>
      <td><span class="badge ${p.activa ? 'badge-verde' : 'badge-rojo'}">${p.activa ? 'Activa' : 'Inactiva'}</span></td>
      <td>
        <button class="btn btn-sm btn-secondary" onclick="abrirModalPregunta(${p.id})">Editar</button>
        <button class="btn btn-sm btn-danger" onclick="eliminarPregunta(${p.id})">Eliminar</button>
      </td>
    </tr>
  `).join('') || '<tr><td colspan="6">Sin preguntas</td></tr>';
}

document.getElementById('filtro-cat-pregunta')?.addEventListener('change', (e) => {
  const catId = e.target.value;
  const filtradas = catId ? preguntas.filter(p => String(p.categoria_id) === catId) : preguntas;
  renderizarPreguntas(filtradas);
});

function abrirModalPregunta(id = null) {
  const modal = document.getElementById('modal-pregunta');
  const p = id ? preguntas.find(x => x.id === id) : null;
  document.getElementById('modal-preg-titulo').textContent = id ? 'Editar pregunta' : 'Nueva pregunta';
  document.getElementById('pregunta-id').value = id || '';
  document.getElementById('pregunta-texto').value = p?.texto || '';
  document.getElementById('pregunta-respuesta').value = p?.respuesta || '';
  document.getElementById('pregunta-categoria').value = p?.categoria_id || '';
  document.getElementById('pregunta-activa').checked = p?.activa ?? true;
  modal.classList.remove('hidden');
}

document.getElementById('modal-pregunta')?.addEventListener('click', (e) => {
  if (e.target === e.currentTarget) e.currentTarget.classList.add('hidden');
});

document.getElementById('form-pregunta')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('pregunta-id').value;
  const catVal = document.getElementById('pregunta-categoria').value;
  const datos = {
    texto: document.getElementById('pregunta-texto').value.trim(),
    respuesta: document.getElementById('pregunta-respuesta').value.trim(),
    categoria_id: catVal ? parseInt(catVal) : null,
    activa: document.getElementById('pregunta-activa').checked,
  };

  try {
    if (id) {
      await apiFetch(`/preguntas/${id}`, { method: 'PUT', body: JSON.stringify(datos) });
    } else {
      await apiFetch('/preguntas', { method: 'POST', body: JSON.stringify(datos) });
    }
    document.getElementById('modal-pregunta').classList.add('hidden');
    cargarPreguntas();
  } catch (err) {
    mostrarAlerta('error-modal-preg', err.message);
  }
});

async function eliminarPregunta(id) {
  if (!confirm('Eliminar esta pregunta?')) return;
  try {
    await apiFetch(`/preguntas/${id}`, { method: 'DELETE' });
    cargarPreguntas();
  } catch (err) {
    mostrarAlerta('error-preguntas', err.message);
  }
}

// --- Consultas ---
async function cargarConsultas() {
  try {
    const consultas = await apiFetch('/consultas') || [];
    const tbody = document.getElementById('tbody-consultas');
    tbody.innerHTML = consultas.map(c => `
      <tr>
        <td>${c.id}</td>
        <td>${escHtml(c.telegram_user || '-')}</td>
        <td>${escHtml(c.texto_consulta)}</td>
        <td>${escHtml((c.texto_respuesta || '').substring(0, 60))}${(c.texto_respuesta || '').length > 60 ? '...' : ''}</td>
        <td><span class="badge ${c.encontrada ? 'badge-verde' : 'badge-rojo'}">${c.encontrada ? 'Si' : 'No'}</span></td>
        <td>${new Date(c.consultado_en).toLocaleString('es-GT')}</td>
      </tr>
    `).join('') || '<tr><td colspan="6">Sin consultas</td></tr>';
  } catch (err) {
    mostrarAlerta('error-consultas', err.message);
  }
}

// --- Configuracion ---
async function cargarConfiguracion() {
  try {
    const configs = await apiFetch('/configuracion') || [];
    const contenedor = document.getElementById('configuracion-lista');
    contenedor.innerHTML = configs.map(c => `
      <div class="form-group">
        <label>${escHtml(c.clave)}</label>
        <small style="display:block;color:var(--color-texto-suave);margin-bottom:.3rem">${escHtml(c.descripcion || '')}</small>
        <div style="display:flex;gap:.5rem">
          <input type="text" id="config-${escHtml(c.clave)}" value="${escHtml(c.valor || '')}" />
          <button class="btn btn-primary" onclick="guardarConfig('${escHtml(c.clave)}')">Guardar</button>
        </div>
      </div>
    `).join('');
  } catch (err) {
    mostrarAlerta('error-configuracion', err.message);
  }
}

async function guardarConfig(clave) {
  const valor = document.getElementById(`config-${clave}`).value;
  try {
    await apiFetch(`/configuracion/${clave}`, { method: 'PUT', body: JSON.stringify({ valor }) });
    mostrarAlerta('exito-configuracion', 'Configuracion guardada correctamente', 'success');
  } catch (err) {
    mostrarAlerta('error-configuracion', err.message);
  }
}

// --- Utilidades ---
function escHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function mostrarAlerta(id, mensaje, tipo = 'error') {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = mensaje;
  el.className = `alert alert-${tipo}`;
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 4000);
}
