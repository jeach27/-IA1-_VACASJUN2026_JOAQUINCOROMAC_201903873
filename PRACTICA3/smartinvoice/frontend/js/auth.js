function verificarAutenticacion() {
    const token = obtenerToken();
    if (!token) {
        window.location.href = "/index.html";
    }
}

function cerrarSesion() {
    borrarToken();
    window.location.href = "/index.html";
}

async function iniciarSesion(evento) {
    evento.preventDefault();
    const usuario = document.getElementById("usuario").value.trim();
    const contrasena = document.getElementById("contrasena").value;
    const btnLogin = document.getElementById("btn-login");
    const alerta = document.getElementById("alerta-login");

    btnLogin.disabled = true;
    btnLogin.textContent = "Verificando...";

    try {
        const respuesta = await post("/auth/login", { username: usuario, password: contrasena });
        guardarToken(respuesta.access_token);

        const me = await get("/auth/me");
        localStorage.setItem("usuario", JSON.stringify(me));

        window.location.href = "/dashboard.html";
    } catch (err) {
        mostrarAlerta("alerta-login", err.message || "Error al iniciar sesion", "error");
    } finally {
        btnLogin.disabled = false;
        btnLogin.textContent = "Ingresar al sistema";
    }
}

function mostrarInfoUsuario() {
    const usuarioStr = localStorage.getItem("usuario");
    if (!usuarioStr) return;
    const usuario = JSON.parse(usuarioStr);
    const el = document.getElementById("info-usuario");
    if (el) {
        el.textContent = `${usuario.username} (${usuario.rol})`;
    }
}
