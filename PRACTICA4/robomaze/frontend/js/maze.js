// Modulo de gestion y renderizado del laberinto en el DOM.
// Controla la cuadricula visual y los modos de interaccion del usuario.

// Estado interno del laberinto actual.
let mazeState = {
    rows: 10,
    cols: 10,
    grid: [],
    start: null,
    end: null,
};

// Modo de interaccion activo: "obstacle" | "start" | "end"
let activeMode = "obstacle";

// Inicializa el laberinto con una cuadricula vacia de ceros.
function initMaze(rows, cols) {
    mazeState.rows = rows;
    mazeState.cols = cols;
    mazeState.grid = Array.from({ length: rows }, () => Array(cols).fill(0));
    mazeState.start = null;
    mazeState.end = null;
}

// Carga la configuracion completa de un laberinto externo (predefinido).
function loadMaze(data) {
    mazeState.rows = data.rows;
    mazeState.cols = data.cols;
    mazeState.grid = data.grid.map((row) => [...row]);
    mazeState.start = data.start ? [...data.start] : null;
    mazeState.end = data.end ? [...data.end] : null;
}

// Retorna la configuracion actual del laberinto lista para enviar a la API.
function getMazeData() {
    return {
        rows: mazeState.rows,
        cols: mazeState.cols,
        grid: mazeState.grid.map((row) => [...row]),
        start: mazeState.start ? [...mazeState.start] : null,
        end: mazeState.end ? [...mazeState.end] : null,
    };
}

// Cambia el modo de interaccion activo para los clicks sobre la cuadricula.
function setActiveMode(mode) {
    activeMode = mode;
    document.querySelectorAll(".mode-btn").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.mode === mode);
    });
}

// Determina la clase CSS de una celda segun su tipo y los conjuntos de ruta/explorados.
function getCellClass(row, col, pathSet, exploredSet) {
    const key = `${row},${col}`;
    const isStart =
        mazeState.start &&
        mazeState.start[0] === row &&
        mazeState.start[1] === col;
    const isEnd =
        mazeState.end &&
        mazeState.end[0] === row &&
        mazeState.end[1] === col;

    if (isStart) return "cell cell-start";
    if (isEnd) return "cell cell-end";
    if (mazeState.grid[row][col] === 1) return "cell cell-obstacle";
    if (pathSet && pathSet.has(key)) return "cell cell-path";
    if (exploredSet && exploredSet.has(key)) return "cell cell-explored";
    return "cell cell-free";
}

// Renderiza la cuadricula completa del laberinto en el contenedor indicado.
// path y explored son listas de [fila, col]; pueden ser null o undefined.
function renderMaze(containerId, path, explored) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const pathSet = path
        ? new Set(path.map(([r, c]) => `${r},${c}`))
        : null;
    const exploredSet = explored
        ? new Set(explored.map(([r, c]) => `${r},${c}`))
        : null;

    container.style.gridTemplateColumns = `repeat(${mazeState.cols}, 1fr)`;
    container.innerHTML = "";

    for (let r = 0; r < mazeState.rows; r++) {
        for (let c = 0; c < mazeState.cols; c++) {
            const cell = document.createElement("div");
            cell.className = getCellClass(r, c, pathSet, exploredSet);
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener("click", () => handleCellClick(r, c));
            container.appendChild(cell);
        }
    }
}

// Maneja el click sobre una celda segun el modo de interaccion activo.
function handleCellClick(row, col) {
    if (activeMode === "start") {
        mazeState.start = [row, col];
        // Libera la celda de obstaculos si estaba bloqueada.
        mazeState.grid[row][col] = 0;
    } else if (activeMode === "end") {
        mazeState.end = [row, col];
        mazeState.grid[row][col] = 0;
    } else if (activeMode === "obstacle") {
        const isStart =
            mazeState.start &&
            mazeState.start[0] === row &&
            mazeState.start[1] === col;
        const isEnd =
            mazeState.end &&
            mazeState.end[0] === row &&
            mazeState.end[1] === col;
        if (!isStart && !isEnd) {
            // Alterna el obstaculo en la celda.
            mazeState.grid[row][col] = mazeState.grid[row][col] === 0 ? 1 : 0;
        }
    }
    renderMaze("maze-grid");
}
