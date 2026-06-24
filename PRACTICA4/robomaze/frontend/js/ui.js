// Modulo de interfaz de usuario. Inicializa la pagina, carga datos
// y gestiona los eventos de los controles.

// Inicializa la pagina: carga laberintos predefinidos y renderiza el laberinto por defecto.
async function initPage() {
    try {
        const mazes = await getPredefinedMazes();
        const selector = document.getElementById("maze-selector");
        selector.innerHTML = '<option value="">Seleccionar laberinto...</option>';
        mazes.forEach((maze) => {
            const option = document.createElement("option");
            option.value = maze.id;
            option.textContent = `${maze.name} - ${maze.description}`;
            option.dataset.maze = JSON.stringify(maze);
            selector.appendChild(option);
        });
    } catch (error) {
        displayError("No se pudo conectar con la API. Asegurese de que el backend esta en ejecucion.");
    }

    initMaze(10, 10);
    renderMaze("maze-grid");
    setActiveMode("obstacle");
    syncSizeInputs();
}

// Actualiza los inputs de tamano para que reflejen el estado actual del laberinto.
function syncSizeInputs() {
    const data = getMazeData();
    document.getElementById("input-rows").value = data.rows;
    document.getElementById("input-cols").value = data.cols;
}

// Crea un laberinto vacio con el tamano indicado en los inputs.
function handleCreateMaze() {
    const rows = parseInt(document.getElementById("input-rows").value, 10) || 10;
    const cols = parseInt(document.getElementById("input-cols").value, 10) || 10;
    const clampedRows = Math.max(5, Math.min(25, rows));
    const clampedCols = Math.max(5, Math.min(25, cols));
    initMaze(clampedRows, clampedCols);
    renderMaze("maze-grid");
    clearResults();
    document.getElementById("maze-selector").value = "";
}

// Solicita a la API un laberinto generado aleatoriamente y lo carga.
async function handleGenerateMaze() {
    const rows = parseInt(document.getElementById("input-rows").value, 10) || 10;
    const cols = parseInt(document.getElementById("input-cols").value, 10) || 10;
    const clampedRows = Math.max(5, Math.min(25, rows));
    const clampedCols = Math.max(5, Math.min(25, cols));
    try {
        const mazeData = await generateMaze(clampedRows, clampedCols);
        loadMaze(mazeData);
        renderMaze("maze-grid");
        clearResults();
        document.getElementById("maze-selector").value = "";
    } catch (error) {
        displayError("No se pudo generar el laberinto. Verifique la conexion con el backend.");
    }
}

// Carga el laberinto seleccionado en el selector de predefinidos.
function handleMazeSelect(event) {
    const option = event.target.selectedOptions[0];
    if (!option || !option.dataset.maze) return;
    const mazeData = JSON.parse(option.dataset.maze);
    loadMaze(mazeData);
    syncSizeInputs();
    renderMaze("maze-grid");
    clearResults();
}

// Limpia los paneles de resultado.
function clearResults() {
    document.getElementById("result-bfs").innerHTML = "";
    document.getElementById("result-dfs").innerHTML = "";
    document.getElementById("result-astar").innerHTML = "";
    document.getElementById("comparison-table").innerHTML = "";
}

// Retorna true si el laberinto tiene inicio y destino definidos.
function validateMaze() {
    const data = getMazeData();
    if (!data.start) { displayError("Debe definir la posicion inicial."); return false; }
    if (!data.end)   { displayError("Debe definir la posicion destino."); return false; }
    return true;
}

// Indica si la animacion esta activada.
function isAnimationEnabled() {
    return document.getElementById("toggle-animation").checked;
}

// Renderiza el resultado de un algoritmo en la cuadricula, con o sin animacion.
async function applyResultToGrid(result) {
    const path     = result.found ? result.path : [];
    const explored = result.explored_order || [];
    if (isAnimationEnabled() && explored.length > 0) {
        await renderMazeAnimated("maze-grid", explored, path, 20);
    } else {
        renderMaze("maze-grid", path, []);
    }
}

// Ejecuta BFS y muestra los resultados.
async function handleRunBFS() {
    if (!validateMaze()) return;
    clearResults();
    setLoading("result-bfs", "Ejecutando BFS...");
    try {
        const result = await searchBFS(getMazeData());
        await applyResultToGrid(result);
        displayResults(result, "result-bfs");
    } catch (error) {
        displayError("Error al ejecutar BFS. Verifique la conexion con el backend.");
    }
}

// Ejecuta DFS y muestra los resultados.
async function handleRunDFS() {
    if (!validateMaze()) return;
    clearResults();
    setLoading("result-dfs", "Ejecutando DFS...");
    try {
        const result = await searchDFS(getMazeData());
        await applyResultToGrid(result);
        displayResults(result, "result-dfs");
    } catch (error) {
        displayError("Error al ejecutar DFS. Verifique la conexion con el backend.");
    }
}

// Ejecuta A* y muestra los resultados.
async function handleRunAStar() {
    if (!validateMaze()) return;
    clearResults();
    setLoading("result-astar", "Ejecutando A*...");
    try {
        const result = await searchAStar(getMazeData());
        await applyResultToGrid(result);
        displayResults(result, "result-astar");
    } catch (error) {
        displayError("Error al ejecutar A*. Verifique la conexion con el backend.");
    }
}

// Ejecuta BFS y DFS juntos.
async function handleRunBoth() {
    if (!validateMaze()) return;
    clearResults();
    setLoading("result-bfs", "Ejecutando BFS...");
    setLoading("result-dfs", "Ejecutando DFS...");
    try {
        const results = await searchBoth(getMazeData());
        renderMaze("maze-grid", results.bfs.found ? results.bfs.path : [], []);
        displayResults(results.bfs, "result-bfs");
        displayResults(results.dfs, "result-dfs");
    } catch (error) {
        displayError("Error al ejecutar los algoritmos. Verifique la conexion con el backend.");
    }
}

// Ejecuta los tres algoritmos y muestra comparativa estadistica.
async function handleRunAll() {
    if (!validateMaze()) return;
    clearResults();
    setLoading("result-bfs",   "Ejecutando BFS...");
    setLoading("result-dfs",   "Ejecutando DFS...");
    setLoading("result-astar", "Ejecutando A*...");
    try {
        const results = await searchAll(getMazeData());
        // Mostrar la ruta de BFS en la cuadricula (optima).
        renderMaze("maze-grid", results.bfs.found ? results.bfs.path : [], []);
        displayResults(results.bfs,   "result-bfs");
        displayResults(results.dfs,   "result-dfs");
        displayResults(results.astar, "result-astar");
        displayComparison(results);
    } catch (error) {
        displayError("Error al comparar algoritmos. Verifique la conexion con el backend.");
    }
}

// Muestra el indicador de carga en el contenedor dado.
function setLoading(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) container.innerHTML = `<p class="loading">${message}</p>`;
}

// Muestra los resultados de un algoritmo en el contenedor indicado.
function displayResults(result, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!result.found) {
        container.innerHTML = `
            <div class="result-card result-not-found">
                <h3>${result.algorithm}</h3>
                <p class="no-route">Sin ruta disponible.</p>
                <p>Nodos explorados: <strong>${result.explored_nodes}</strong></p>
                <p>Tiempo: <strong>${result.execution_time_ms} ms</strong></p>
            </div>`;
        return;
    }

    container.innerHTML = `
        <div class="result-card result-found">
            <h3>${result.algorithm}</h3>
            <p>Ruta encontrada: <strong>Si</strong></p>
            <p>Longitud de ruta: <strong>${result.path_length} celdas</strong></p>
            <p>Nodos explorados: <strong>${result.explored_nodes}</strong></p>
            <p>Tiempo: <strong>${result.execution_time_ms} ms</strong></p>
        </div>`;
}

// Muestra la tabla comparativa de los tres algoritmos.
// results debe tener claves 'bfs', 'dfs' y 'astar'.
function displayComparison(results) {
    const container = document.getElementById("comparison-table");
    if (!container) return;

    const algos = [
        { key: "bfs",   label: "BFS" },
        { key: "dfs",   label: "DFS" },
        { key: "astar", label: "A*"  },
    ];

    // Calcular ganadores por metrica (solo entre los que encontraron ruta).
    const found = algos.filter((a) => results[a.key].found);

    function bestClass(key, metric, lowerIsBetter = true) {
        if (!results[key].found) return "";
        const vals = found.map((a) => results[a.key][metric]);
        const best = lowerIsBetter ? Math.min(...vals) : Math.max(...vals);
        return results[key][metric] === best ? "best-value" : "";
    }

    const rows = algos.map((a) => {
        const r = results[a.key];
        const lengthCell = r.found
            ? `<td class="${bestClass(a.key, "path_length")}">${r.path_length}</td>`
            : `<td>-</td>`;
        const nodesCell  = `<td class="${bestClass(a.key, "explored_nodes")}">${r.explored_nodes}</td>`;
        const timeCell   = `<td class="${bestClass(a.key, "execution_time_ms")}">${r.execution_time_ms} ms</td>`;
        const foundCell  = `<td>${r.found ? "Si" : "No"}</td>`;
        return `<tr><td><strong>${a.label}</strong></td>${foundCell}${lengthCell}${nodesCell}${timeCell}</tr>`;
    });

    container.innerHTML = `
        <h3>Comparacion de algoritmos</h3>
        <table class="comparison">
            <thead>
                <tr>
                    <th>Algoritmo</th>
                    <th>Ruta</th>
                    <th>Longitud</th>
                    <th>Nodos</th>
                    <th>Tiempo</th>
                </tr>
            </thead>
            <tbody>${rows.join("")}</tbody>
        </table>
        <p class="comparison-note">El valor resaltado en verde es el mejor para cada metrica.</p>`;
}

// Muestra un mensaje de error en el panel de errores (desaparece a los 5 segundos).
function displayError(message) {
    const errorPanel = document.getElementById("error-panel");
    if (!errorPanel) return;
    errorPanel.textContent = message;
    errorPanel.style.display = "block";
    setTimeout(() => { errorPanel.style.display = "none"; }, 5000);
}

// Registra todos los manejadores de eventos al cargar el DOM.
document.addEventListener("DOMContentLoaded", () => {
    initPage();

    document.getElementById("maze-selector").addEventListener("change", handleMazeSelect);
    document.getElementById("btn-create").addEventListener("click", handleCreateMaze);
    document.getElementById("btn-generate").addEventListener("click", handleGenerateMaze);
    document.getElementById("btn-bfs").addEventListener("click", handleRunBFS);
    document.getElementById("btn-dfs").addEventListener("click", handleRunDFS);
    document.getElementById("btn-astar").addEventListener("click", handleRunAStar);
    document.getElementById("btn-both").addEventListener("click", handleRunBoth);
    document.getElementById("btn-all").addEventListener("click", handleRunAll);

    document.querySelectorAll(".mode-btn").forEach((btn) => {
        btn.addEventListener("click", () => setActiveMode(btn.dataset.mode));
    });
});
