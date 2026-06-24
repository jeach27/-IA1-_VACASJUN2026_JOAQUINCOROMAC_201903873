// Modulo de comunicacion con la API REST de RoboMaze.
// Todas las funciones son async y manejan errores con try/catch.

const API_BASE_URL = "http://localhost:8000";

// Obtiene la lista de laberintos predefinidos desde la API.
async function getPredefinedMazes() {
    try {
        const response = await fetch(`${API_BASE_URL}/maze/predefined`);
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Error al obtener laberintos predefinidos:", error);
        throw error;
    }
}

// Envia la configuracion del laberinto y ejecuta el algoritmo BFS.
// mazeData debe tener: rows, cols, grid, start, end.
async function searchBFS(mazeData) {
    try {
        const response = await fetch(`${API_BASE_URL}/search/bfs`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(mazeData),
        });
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Error en busqueda BFS:", error);
        throw error;
    }
}

// Envia la configuracion del laberinto y ejecuta el algoritmo DFS.
// mazeData debe tener: rows, cols, grid, start, end.
async function searchDFS(mazeData) {
    try {
        const response = await fetch(`${API_BASE_URL}/search/dfs`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(mazeData),
        });
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Error en busqueda DFS:", error);
        throw error;
    }
}

// Envia la configuracion del laberinto y ejecuta BFS y DFS de forma conjunta.
// Retorna un objeto con claves 'bfs' y 'dfs'.
async function searchBoth(mazeData) {
    try {
        const response = await fetch(`${API_BASE_URL}/search/both`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(mazeData),
        });
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Error en busqueda combinada:", error);
        throw error;
    }
}

// Envia la configuracion del laberinto y ejecuta el algoritmo A*.
// mazeData debe tener: rows, cols, grid, start, end.
async function searchAStar(mazeData) {
    try {
        const response = await fetch(`${API_BASE_URL}/search/astar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(mazeData),
        });
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Error en busqueda A*:", error);
        throw error;
    }
}

// Ejecuta BFS, DFS y A* en un solo llamado para comparacion estadistica.
// Retorna un objeto con claves 'bfs', 'dfs' y 'astar'.
async function searchAll(mazeData) {
    try {
        const response = await fetch(`${API_BASE_URL}/search/all`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(mazeData),
        });
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Error en comparacion de algoritmos:", error);
        throw error;
    }
}

// Solicita a la API un laberinto generado aleatoriamente con las dimensiones dadas.
// Retorna un objeto con rows, cols, grid, start y end.
async function generateMaze(rows, cols) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/maze/generate?rows=${rows}&cols=${cols}`
        );
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Error al generar laberinto:", error);
        throw error;
    }
}
