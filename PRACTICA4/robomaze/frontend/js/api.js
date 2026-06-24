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
