/* ============================
   SISTEMA DE NOTIFICACIONES
   Reemplaza los alert() del navegador por
   notificaciones visuales más prolijas.
   (Las clases se llaman "notificacion" y no "toast"
   para no chocar con las de Bootstrap.)
   ============================ */
function mostrarToast(mensaje, tipo = 'exito') {
    let contenedor = document.querySelector('.notificaciones');
    if (!contenedor) {
        contenedor = document.createElement('div');
        contenedor.className = 'notificaciones';
        document.body.appendChild(contenedor);
    }

    const aviso = document.createElement('div');
    aviso.className = `notificacion notificacion-${tipo}`;
    aviso.textContent = mensaje;
    contenedor.appendChild(aviso);

    // Animar entrada
    requestAnimationFrame(() => aviso.classList.add('notificacion-show'));

    // Remover después de 4 segundos
    setTimeout(() => {
        aviso.classList.remove('notificacion-show');
        setTimeout(() => aviso.remove(), 300);
    }, 4000);
}

/* ============================
   FORMULARIO DE SOLICITUD (solicitud_form.html)
   Si la validación pasa, se envía a Django.
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

        formularioSolicitud.submit();
    });
}

/* ============================
   FORMULARIO DE CONTACTO (contacto.html)
   No tiene modelo detrás: solo valida y avisa.
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
   FORMULARIO DE PRODUCTOS (lista.html)
   Si la validación pasa, se envía a Django.
   ============================ */
const formularioProductos = document.querySelector("#formProducto");
if (formularioProductos) {
    formularioProductos.addEventListener("submit", function (evento) {
        evento.preventDefault();
        const nombre = document.querySelector("#nombre").value.trim();
        const precio = document.querySelector("#precio").value.trim();
        const descripcion = document.querySelector("#descripcion").value.trim();

        if (nombre.length < 2) {
            mostrarToast("El nombre debe tener al menos 2 caracteres.", "error");
            return;
        }
        if (precio === "" || Number(precio) <= 0) {
            mostrarToast("El precio no puede estar vacío y debe ser mayor que 0.", "error");
            return;
        }
        if (descripcion.length < 10) {
            mostrarToast("La descripción debe tener al menos 10 caracteres.", "error");
            return;
        }

        formularioProductos.submit();
    });
}