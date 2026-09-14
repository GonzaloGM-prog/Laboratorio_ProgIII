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
        // Validar nombre 
        if (nombre.length < 2) { alert("El nombre debe tener al menos 2 caracteres."); return; } 
        // Validar apellido 
        if (apellido.length < 2) { alert("El apellido debe tener al menos 2 caracteres."); return; }
        //Validar DNI 
        if (!/^[0-9]{7,8}$/.test(dni)) { alert("El DNI debe tener entre 7 y 8 números."); return; }
         // Validar email 
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { alert("Ingresá un email válido."); return; }
         // Validar teléfono 
        if (!/^[0-9]{8,15}$/.test(telefono)) { alert("El teléfono debe contener entre 8 y 15 números."); return; } 
        // Validar descripción 
        if (descripcion.length < 10) { alert("La descripción debe tener al menos 10 caracteres."); return; } 
        // Validar checkbox 
        if (!aceptar) { 
            alert("Debés aceptar la declaración de datos."); return; 
        } 
            alert("Solicitud enviada correctamente."); formularioSolicitud.reset(); 
        }); }


const formularioContacto = document.querySelector("#formContacto");
if (formularioContacto) {
    formularioContacto.addEventListener("submit", function (evento) {
        evento.preventDefault();
        const nombre = document.querySelector("#nombre").value.trim();
        const asunto = document.querySelector("#asunto").value.trim();
        const mensaje = document.querySelector("#mensaje").value.trim();
        const email = document.querySelector("#email").value.trim();

        // Validar nombre
        if (nombre.length < 2) {
            alert("El nombre debe tener al menos 2 caracteres.");
            return;
        }

        // Validar asunto
        if (asunto.length < 2) {
            alert("El asunto debe tener al menos 2 caracteres.");
            return;
        }

        // Validar mensaje
        if (mensaje.length < 10) {
            alert("El mensaje debe tener al menos 10 caracteres.");
            return;
        }

        // Validar email
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            alert("Ingresá un email válido.");
            return;
        }

        alert("Mensaje enviado correctamente.");
        formularioContacto.reset();
    });
}
        

const formularioProductos = document.querySelector("#formProductos");
if (formularioProductos) {
    formularioProductos.addEventListener("submit", function (evento) {
        evento.preventDefault();
        const nombre = document.querySelector("#nombre").value.trim();
        const rubro = document.querySelector("#rubro").value.trim();
        const precio = document.querySelector("#precio").value.trim();
        const descripcion = document.querySelector("#descripcion").value.trim();

        // Validar nombre
        if (nombre.length < 2) {
            alert("El nombre debe tener al menos 2 caracteres.");
            return;
        }

        // Validar rubro
        if (rubro === "") {
            alert("El rubro no puede estar vacío.");
            return;
        }
        
        // Validar precio
        if (precio <=0 || precio === "") {
            alert("El precio no puede estar vacío y debe ser mayor que 0.");
            return;
        }
        
        // Validar descripción
        if (descripcion.length < 10) {
            alert("La descripción debe tener al menos 10 caracteres.");
            return;
        }
        
        alert("Producto añadido correctamente.");
        formularioProductos.reset();
    });
}