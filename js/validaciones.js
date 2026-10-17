/* ============================
   SISTEMA DE NOTIFICACIONES TOAST
   Reemplaza los alert() del navegador por
   notificaciones visuales más prolijas
   ============================ */
function mostrarToast(mensaje, tipo = 'exito') {
    let contenedor = document.querySelector('.toast-container');
    if (!contenedor) {
        contenedor = document.createElement('div');
        contenedor.className = 'toast-container';
        document.body.appendChild(contenedor);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    toast.textContent = mensaje;
    contenedor.appendChild(toast);

    // Animar entrada
    requestAnimationFrame(() => toast.classList.add('toast-show'));

    // Remover después de 4 segundos
    setTimeout(() => {
        toast.classList.remove('toast-show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/* ============================
   FORMULARIO DE SOLICITUD (solicitud.html)
   ============================ */
const formularioSolicitud = document.querySelector("#formSolicitud");
if (formularioSolicitud) {
    formularioSolicitud.addEventListener("submit", function (evento) {
        evento.preventDefault();
        const nombre = document.querySelector("#nombre").value.trim();
        const apellido = document.querySelector("#apellido").value.trim();
        const dni = document.querySelector("#dni").value.trim();
        const email = document.querySelector("#email").value.trim();
        const telefono = document.querySelector("#telefono").value.trim();
        const descripcion = document.querySelector("#descripcion").value.trim();
        const aceptar = document.querySelector("#aceptar").checked;

        if (nombre.length < 2) {
            mostrarToast("El nombre debe tener al menos 2 caracteres.", "error");
            return;
        }
        if (apellido.length < 2) {
            mostrarToast("El apellido debe tener al menos 2 caracteres.", "error");
            return;
        }
        if (!/^[0-9]{7,8}$/.test(dni)) {
            mostrarToast("El DNI debe tener entre 7 y 8 números.", "error");
            return;
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            mostrarToast("Ingresá un email válido.", "error");
            return;
        }
        if (!/^[0-9]{8,15}$/.test(telefono)) {
            mostrarToast("El teléfono debe contener entre 8 y 15 números.", "error");
            return;
        }
        if (descripcion.length < 10) {
            mostrarToast("La descripción debe tener al menos 10 caracteres.", "error");
            return;
        }
        if (!aceptar) {
            mostrarToast("Debés aceptar la declaración de datos.", "error");
            return;
        }

        mostrarToast("Solicitud enviada correctamente.", "exito");
        formularioSolicitud.reset();
    });
}

/* ============================
   FORMULARIO DE CONTACTO (contactos.html)
   ============================ */
const formularioContacto = document.querySelector("#formContacto");
if (formularioContacto) {
    formularioContacto.addEventListener("submit", function (evento) {
        evento.preventDefault();
        const nombre = document.querySelector("#nombre").value.trim();
        const asunto = document.querySelector("#asunto").value.trim();
        const mensaje = document.querySelector("#mensaje").value.trim();
        const email = document.querySelector("#email").value.trim();

        if (nombre.length < 2) {
            mostrarToast("El nombre debe tener al menos 2 caracteres.", "error");
            return;
        }
        if (asunto.length < 2) {
            mostrarToast("El asunto debe tener al menos 2 caracteres.", "error");
            return;
        }
        if (mensaje.length < 10) {
            mostrarToast("El mensaje debe tener al menos 10 caracteres.", "error");
            return;
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            mostrarToast("Ingresá un email válido.", "error");
            return;
        }

        mostrarToast("Mensaje enviado correctamente.", "exito");
        formularioContacto.reset();
    });
}

/* ============================
   FORMULARIO DE PRODUCTOS (productos.html)
   ============================ */
const formularioProductos = document.querySelector("#formProducto");
if (formularioProductos) {
    formularioProductos.addEventListener("submit", function (evento) {
        evento.preventDefault();
        const nombre = document.querySelector("#nombre").value.trim();
        const rubro = document.querySelector("#rubro").value.trim();
        const precio = document.querySelector("#precio").value.trim();
        const descripcion = document.querySelector("#descripcion").value.trim();

        if (nombre.length < 2) {
            mostrarToast("El nombre debe tener al menos 2 caracteres.", "error");
            return;
        }
        if (rubro === "") {
            mostrarToast("El rubro no puede estar vacío.", "error");
            return;
        }
        if (precio <= 0 || precio === "") {
            mostrarToast("El precio no puede estar vacío y debe ser mayor que 0.", "error");
            return;
        }
        if (descripcion.length < 10) {
            mostrarToast("La descripción debe tener al menos 10 caracteres.", "error");
            return;
        }

        mostrarToast("Producto añadido correctamente.", "exito");
        formularioProductos.reset();
    });
}
