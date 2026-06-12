// app.js
// Logica del frontend de Doctor Byte.
// Consumimos los endpoints del backend para cargar sintomas, enviar diagnosticos
// y mostrar el historial.

const API_BASE = '';

// Mapa de nombres legibles para los sintomas retornados por la API
const ETIQUETAS_SINTOMAS = {
  pantalla_negra: 'Pantalla negra',
  reinicio_inesperado: 'Reinicio inesperado',
  lentitud_extrema: 'Lentitud extrema',
  no_enciende: 'El equipo no enciende',
  sonido_pitidos_arranque: 'Sonidos de pitidos al arranque',
  sobrecalentamiento: 'Sobrecalentamiento',
  pantalla_azul_muerte: 'Pantalla azul de la muerte (BSOD)',
  no_reconoce_disco: 'No reconoce el disco duro',
  aplicaciones_se_cierran_solas: 'Las aplicaciones se cierran solas',
  sin_sonido: 'Sin sonido',
  red_no_conecta: 'La red no conecta',
  teclado_no_responde: 'El teclado no responde',
  mouse_no_responde: 'El mouse no responde',
  bateria_no_carga: 'La bateria no carga',
  ventilador_muy_ruidoso: 'Ventilador muy ruidoso'
};

// Mapa de nombres legibles para las fallas diagnosticadas
const ETIQUETAS_FALLAS = {
  falla_ram: 'Falla en la memoria RAM',
  falla_disco_duro: 'Falla en el disco duro',
  falla_fuente_poder: 'Falla en la fuente de poder',
  sobrecalentamiento_cpu: 'Sobrecalentamiento del CPU',
  falla_sistema_operativo: 'Falla en el sistema operativo',
  virus_malware: 'Virus o malware',
  falla_tarjeta_grafica: 'Falla en la tarjeta grafica',
  falla_placa_madre: 'Falla en la placa madre',
  falla_drivers: 'Falla en los drivers',
  falla_bateria: 'Falla en la bateria'
};

// Obtenemos los elementos del DOM una sola vez al iniciar
const listaSintomas = document.getElementById('lista-sintomas');
const seccionDiagnostico = document.getElementById('seccion-diagnostico');
const seccionResultado = document.getElementById('seccion-resultado');
const contenidoResultado = document.getElementById('contenido-resultado');
const contenidoHistorial = document.getElementById('contenido-historial');
const btnDiagnosticar = document.getElementById('btn-diagnosticar');
const btnLimpiar = document.getElementById('btn-limpiar');
const btnNuevoDiagnostico = document.getElementById('btn-nuevo-diagnostico');
const btnActualizarHistorial = document.getElementById('btn-actualizar-historial');


// --- Carga de sintomas ---

async function cargarSintomas() {
  try {
    const respuesta = await fetch(`${API_BASE}/sintomas`);
    if (!respuesta.ok) throw new Error(`Error HTTP ${respuesta.status}`);
    const datos = await respuesta.json();
    renderizarSintomas(datos.sintomas);
  } catch (error) {
    listaSintomas.innerHTML = `<p class="error">No se pudieron cargar los sintomas. Verifique que el servidor este corriendo.</p>`;
  }
}

function renderizarSintomas(sintomas) {
  listaSintomas.innerHTML = '';
  sintomas.forEach(sintoma => {
    const etiqueta = ETIQUETAS_SINTOMAS[sintoma] || sintoma.replace(/_/g, ' ');

    const item = document.createElement('div');
    item.classList.add('sintoma-item');
    item.dataset.sintoma = sintoma;

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = `sintoma-${sintoma}`;
    checkbox.value = sintoma;

    const label = document.createElement('label');
    label.htmlFor = `sintoma-${sintoma}`;
    label.textContent = etiqueta;

    item.appendChild(checkbox);
    item.appendChild(label);

    // Permitimos hacer clic en el area completa del item para marcar el checkbox
    item.addEventListener('click', (evento) => {
      if (evento.target !== checkbox) {
        checkbox.checked = !checkbox.checked;
      }
      item.classList.toggle('seleccionado', checkbox.checked);
    });

    listaSintomas.appendChild(item);
  });
}


// --- Obtencion de sintomas seleccionados ---

function obtenerSintomasSeleccionados() {
  const checkboxes = listaSintomas.querySelectorAll('input[type="checkbox"]:checked');
  return Array.from(checkboxes).map(cb => cb.value);
}


// --- Solicitud de diagnostico ---

async function solicitarDiagnostico() {
  const sintomas = obtenerSintomasSeleccionados();

  if (sintomas.length === 0) {
    mostrarError(contenidoResultado, 'Selecciona al menos un sintoma antes de diagnosticar.');
    mostrarSeccionResultado();
    return;
  }

  btnDiagnosticar.disabled = true;
  btnDiagnosticar.textContent = 'Procesando...';

  const cuerpo = { sintomas };

  try {
    const respuesta = await fetch(`${API_BASE}/diagnostico`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cuerpo)
    });

    if (!respuesta.ok) {
      const error = await respuesta.json();
      throw new Error(error.error || `Error HTTP ${respuesta.status}`);
    }

    const resultado = await respuesta.json();
    renderizarResultado(resultado);
    mostrarSeccionResultado();
    cargarHistorial();
  } catch (error) {
    mostrarError(contenidoResultado, `Error al procesar el diagnostico: ${error.message}`);
    mostrarSeccionResultado();
  } finally {
    btnDiagnosticar.disabled = false;
    btnDiagnosticar.textContent = 'Diagnosticar';
  }
}


// --- Renderizado del resultado ---

function renderizarResultado(resultado) {
  contenidoResultado.innerHTML = '';

  const meta = document.createElement('p');
  meta.classList.add('resultado-meta');
  const sintomasLegibles = resultado.sintomas
    .map(s => ETIQUETAS_SINTOMAS[s] || s.replace(/_/g, ' '))
    .join(', ');
  meta.textContent = `Sintomas analizados: ${sintomasLegibles}`;
  contenidoResultado.appendChild(meta);

  if (!resultado.diagnosticos || resultado.diagnosticos.length === 0) {
    const vacio = document.createElement('div');
    vacio.classList.add('resultado-vacio');
    vacio.textContent = 'No se encontro una falla especifica para los sintomas seleccionados. Considere consultar a un tecnico.';
    contenidoResultado.appendChild(vacio);
    return;
  }

  resultado.diagnosticos.forEach(d => {
    const card = document.createElement('div');
    card.classList.add('diagnostico-card');

    const etiquetaFalla = document.createElement('p');
    etiquetaFalla.classList.add('diagnostico-card__etiqueta');
    etiquetaFalla.textContent = 'Falla detectada';

    const falla = document.createElement('p');
    falla.classList.add('diagnostico-card__falla');
    falla.textContent = ETIQUETAS_FALLAS[d.falla] || d.falla.replace(/_/g, ' ');

    const etiquetaRec = document.createElement('p');
    etiquetaRec.classList.add('diagnostico-card__etiqueta');
    etiquetaRec.style.marginTop = '0.75rem';
    etiquetaRec.textContent = 'Recomendacion';

    const recomendacion = document.createElement('p');
    recomendacion.classList.add('diagnostico-card__recomendacion');
    recomendacion.textContent = d.recomendacion;

    card.appendChild(etiquetaFalla);
    card.appendChild(falla);
    card.appendChild(etiquetaRec);
    card.appendChild(recomendacion);
    contenidoResultado.appendChild(card);
  });
}


// --- Historial ---

async function cargarHistorial() {
  contenidoHistorial.innerHTML = '<p class="cargando">Cargando historial...</p>';
  try {
    const respuesta = await fetch(`${API_BASE}/historial`);
    if (!respuesta.ok) throw new Error(`Error HTTP ${respuesta.status}`);
    const datos = await respuesta.json();
    renderizarHistorial(datos.historial);
  } catch (error) {
    contenidoHistorial.innerHTML = `<p class="error">No se pudo cargar el historial.</p>`;
  }
}

function renderizarHistorial(historial) {
  contenidoHistorial.innerHTML = '';

  if (!historial || historial.length === 0) {
    contenidoHistorial.innerHTML = '<p class="historial-vacio">No hay diagnosticos en el historial todavia.</p>';
    return;
  }

  historial.forEach(registro => {
    const item = document.createElement('div');
    item.classList.add('historial-item');

    const encabezado = document.createElement('div');
    encabezado.classList.add('historial-item__encabezado');

    const idSpan = document.createElement('span');
    idSpan.classList.add('historial-item__id');
    idSpan.textContent = `#${registro.id}`;

    const fechaSpan = document.createElement('span');
    fechaSpan.classList.add('historial-item__fecha');
    fechaSpan.textContent = registro.fecha;

    encabezado.appendChild(idSpan);
    encabezado.appendChild(fechaSpan);

    const resumen = document.createElement('p');
    resumen.classList.add('historial-item__resumen');
    const sintomasLegibles = registro.sintomas
      .map(s => ETIQUETAS_SINTOMAS[s] || s.replace(/_/g, ' '))
      .join(', ');
    resumen.textContent = `Sintomas: ${sintomasLegibles}`;

    const fallas = document.createElement('div');
    fallas.classList.add('historial-item__fallas');

    if (!registro.diagnosticos || registro.diagnosticos.length === 0) {
      const etiqueta = document.createElement('span');
      etiqueta.classList.add('etiqueta-sin-resultado');
      etiqueta.textContent = 'Sin diagnostico';
      fallas.appendChild(etiqueta);
    } else {
      registro.diagnosticos.forEach(d => {
        const etiqueta = document.createElement('span');
        etiqueta.classList.add('etiqueta-falla');
        etiqueta.textContent = ETIQUETAS_FALLAS[d.falla] || d.falla.replace(/_/g, ' ');
        fallas.appendChild(etiqueta);
      });
    }

    item.appendChild(encabezado);
    item.appendChild(resumen);
    item.appendChild(fallas);
    contenidoHistorial.appendChild(item);
  });
}


// --- Utilidades de interfaz ---

function mostrarSeccionResultado() {
  seccionResultado.classList.remove('card--oculto');
  seccionResultado.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function ocultarSeccionResultado() {
  seccionResultado.classList.add('card--oculto');
  contenidoResultado.innerHTML = '';
}

function mostrarError(contenedor, mensaje) {
  contenedor.innerHTML = `<div class="error">${mensaje}</div>`;
}

function limpiarSeleccion() {
  const checkboxes = listaSintomas.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(cb => {
    cb.checked = false;
    cb.closest('.sintoma-item').classList.remove('seleccionado');
  });
}


// --- Manejadores de eventos ---

btnDiagnosticar.addEventListener('click', solicitarDiagnostico);

btnLimpiar.addEventListener('click', () => {
  limpiarSeleccion();
  ocultarSeccionResultado();
});

btnNuevoDiagnostico.addEventListener('click', () => {
  limpiarSeleccion();
  ocultarSeccionResultado();
  seccionDiagnostico.scrollIntoView({ behavior: 'smooth', block: 'start' });
});

btnActualizarHistorial.addEventListener('click', cargarHistorial);


// --- Inicializacion al cargar la pagina ---

cargarSintomas();
cargarHistorial();
