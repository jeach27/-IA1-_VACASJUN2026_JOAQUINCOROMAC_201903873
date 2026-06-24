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
}

// Carga el laberinto seleccionado en el selector de predefinidos.
function handleMazeSelect(event) {
    const option = event.target.selectedOptions[0];
    if (!option || !option.dataset.maze) return;
    const mazeData = JSON.parse(option.dataset.maze);
    loadMaze(mazeData);
    renderMaze("maze-grid");
    clearResults();
}

// Limpia los paneles de resultado de BFS y DFS.
function clearResults() {
    document.getElementById("result-bfs").innerHTML = "";
    document.getElementById("result-dfs").innerHTML = "";
}

// Valida que el laberinto tenga inicio y destino definidos.
function validateMaze() {
    const data = getMazeData();
    if (!data.start) {
        displayError("Debe definir la posicion inicial.");
        return false;
    }
    if (!data.end) {
        displayError("Debe definir la posicion destino.");
        return false;
    }
    return true;
}

// Ejecuta BFS y muestra los resultados en el panel correspondiente.
async function handleRunBFS() {
    if (!validateMaze()) return;
    const data = getMazeData();
    try {
        setLoading("result-bfs", "Ejecutando BFS...");
        const result = await searchBFS(data);
        renderMaze("maze-grid", result.found ? result.path : [], null);
        displayResults(result, "result-bfs");
    } catch (error) {
        displayError("Error al ejecutar BFS. Verifique la conexion con el backend.");
    }
}

// Ejecuta DFS y muestra los resultados en el panel correspondiente.
async function handleRunDFS() {
    if (!validateMaze()) return;
    const data = getMazeData();
    try {
        setLoading("result-dfs", "Ejecutando DFS...");
        const result = await searchDFS(data);
        renderMaze("maze-grid", result.found ? result.path : [], null);
        displayResults(result, "result-dfs");
    } catch (error) {
        displayError("Error al ejecutar DFS. Verifique la conexion con el backend.");
    }
}

// Ejecuta BFS y DFS de forma conjunta y muestra ambos resultados.
async function handleRunBoth() {
    if (!validateMaze()) return;
    const data = getMazeData();
    try {
        setLoading("result-bfs", "Ejecutando BFS...");
        setLoading("result-dfs", "Ejecutando DFS...");
        const results = await searchBoth(data);
        renderMaze("maze-grid", results.bfs.found ? results.bfs.path : [], null);
        displayResults(results.bfs, "result-bfs");
        displayResults(results.dfs, "result-dfs");
    } catch (error) {
        displayError("Error al ejecutar los algoritmos. Verifique la conexion con el backend.");
    }
}

// Muestra el indicador de carga en el contenedor dado mientras espera la respuesta.
function setLoading(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) container.innerHTML = `<p class="loading">${message}</p>`;
}

// Muestra los resultados de un algoritmo en el contenedor indicado.
// result es el objeto retornado por la API.
function displayResults(result, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!result.found) {
        container.innerHTML = `
            <div class="result-card result-not-found">
                <h3>${result.algorithm}</h3>
                <p class="no-route">No existe ruta entre el inicio y el destino.</p>
                <p>Nodos explorados: <strong>${result.explored_nodes}</strong></p>
                <p>Tiempo: <strong>${result.execution_time_ms} ms</strong></p>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <div class="result-card result-found">
            <h3>${result.algorithm}</h3>
            <p>Ruta encontrada: <strong>Si</strong></p>
            <p>Longitud de la ruta: <strong>${result.path_length} celdas</strong></p>
            <p>Nodos explorados: <strong>${result.explored_nodes}</strong></p>
            <p>Tiempo de ejecucion: <strong>${result.execution_time_ms} ms</strong></p>
        </div>
    `;
}

// Muestra un mensaje de error visible al usuario en el panel de errores.
function displayError(message) {
    const errorPanel = document.getElementById("error-panel");
    if (!errorPanel) return;
    errorPanel.textContent = message;
    errorPanel.style.display = "block";
    setTimeout(() => {
        errorPanel.style.display = "none";
    }, 5000);
}

// Registra los manejadores de eventos al cargar el DOM.
document.addEventListener("DOMContentLoaded", () => {
    initPage();

    document.getElementById("maze-selector").addEventListener("change", handleMazeSelect);
    document.getElementById("btn-bfs").addEventListener("click", handleRunBFS);
    document.getElementById("btn-dfs").addEventListener("click", handleRunDFS);
    document.getElementById("btn-both").addEventListener("click", handleRunBoth);

    document.querySelectorAll(".mode-btn").forEach((btn) => {
        btn.addEventListener("click", () => setActiveMode(btn.dataset.mode));
    });
});
