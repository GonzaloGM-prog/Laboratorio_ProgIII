/* =====================================================================
   PONCHO DIGITAL — Interacciones de interfaz
   Solo mejoras visuales y de usabilidad (mejora progresiva).
   No modifica validaciones ni envíos: esos siguen en validaciones.js
   y en Django. Todo va dentro de una IIFE para no generar variables
   globales que choquen con las de validaciones.js.
   ===================================================================== */
(function () {
    'use strict';

    const reducirMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ---------- Sombra de la barra al hacer scroll ---------- */
    const barra = document.getElementById('barra');
    if (barra) {
        const actualizarBarra = () => barra.classList.toggle('con-sombra', window.scrollY > 8);
        actualizarBarra();
        window.addEventListener('scroll', actualizarBarra, { passive: true });
    }

    /* ---------- Aparición suave de secciones ---------- */
    const revelables = document.querySelectorAll('[data-revelar]');
    if (revelables.length && 'IntersectionObserver' in window && !reducirMovimiento) {
        document.documentElement.classList.add('js-anim');
        const observador = new IntersectionObserver((entradas) => {
            entradas.forEach((entrada) => {
                if (entrada.isIntersecting) {
                    entrada.target.classList.add('visible');
                    observador.unobserve(entrada.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
        revelables.forEach((el) => observador.observe(el));
    }

    /* ---------- Errores del servidor junto a su campo ---------- */
    document.querySelectorAll('.campo .error-campo').forEach((error, i) => {
        if (!error.textContent.trim()) return;
        const campo = error.closest('.campo');
        campo.classList.add('campo-invalido');
        error.id = error.id || `error-campo-${i}`;
        error.setAttribute('role', 'alert');
        campo.querySelectorAll('input:not([type="hidden"]), select, textarea').forEach((control) => {
            control.setAttribute('aria-invalid', 'true');
            control.setAttribute('aria-describedby', error.id);
            const limpiar = () => {
                campo.classList.remove('campo-invalido');
                control.removeAttribute('aria-invalid');
            };
            control.addEventListener('input', limpiar, { once: true });
            control.addEventListener('change', limpiar, { once: true });
        });
    });

    // Lleva la vista al primer campo con error tras un envío fallido
    const primerError = document.querySelector('.campo-invalido');
    if (primerError) {
        primerError.scrollIntoView({ behavior: reducirMovimiento ? 'auto' : 'smooth', block: 'center' });
    }

    /* ---------- Contador de caracteres en textareas ---------- */
    const MINIMO = 10; // mismo mínimo que usa validaciones.js
    const contadores = [];
    document.querySelectorAll('.campo textarea').forEach((area) => {
        const contador = document.createElement('span');
        contador.className = 'contador';
        contador.setAttribute('aria-live', 'polite');
        area.insertAdjacentElement('afterend', contador);
        const actualizar = () => {
            const largo = area.value.trim().length;
            contador.textContent = largo < MINIMO
                ? `${largo} caracteres · mínimo ${MINIMO}`
                : `${largo} caracteres`;
            contador.classList.toggle('ok', largo >= MINIMO);
        };
        area.addEventListener('input', actualizar);
        actualizar();
        contadores.push(actualizar);
    });

    /* ---------- Rubros: select múltiple → chips táctiles ---------- */
    // El <select> original sigue en el formulario (es el que se envía);
    // los chips solo cambian qué opciones quedan seleccionadas.
    const iconoCheck = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';
    const sincronizadores = [];

    document.querySelectorAll('.campo select[multiple]').forEach((select) => {
        if (!select.options.length) return;

        const campo = select.closest('.campo');
        const etiqueta = campo.querySelector('label');
        const grupo = document.createElement('div');
        grupo.className = 'chips';
        grupo.setAttribute('role', 'group');
        if (etiqueta) {
            etiqueta.id = etiqueta.id || `etiqueta-${select.id}`;
            grupo.setAttribute('aria-labelledby', etiqueta.id);
            // La etiqueta ahora apunta al primer chip, no al select oculto
            etiqueta.removeAttribute('for');
        }

        const chips = Array.from(select.options).map((opcion) => {
            const chip = document.createElement('button');
            chip.type = 'button';
            chip.className = 'chip';
            chip.innerHTML = `${iconoCheck}<span></span>`;
            chip.querySelector('span').textContent = opcion.textContent;
            chip.addEventListener('click', () => {
                opcion.selected = !opcion.selected;
                sincronizar();
                select.dispatchEvent(new Event('change', { bubbles: true }));
            });
            grupo.appendChild(chip);
            return { chip, opcion };
        });

        function sincronizar() {
            chips.forEach(({ chip, opcion }) => chip.setAttribute('aria-pressed', String(opcion.selected)));
        }
        sincronizar();
        sincronizadores.push(sincronizar);

        // Oculto visualmente pero sigue en el formulario y con validación nativa
        select.classList.add('visually-hidden');
        select.tabIndex = -1;
        select.setAttribute('aria-hidden', 'true');
        select.insertAdjacentElement('afterend', grupo);

        // Si el navegador marca el select como inválido (required), llevar el foco a los chips
        select.addEventListener('invalid', () => {
            campo.classList.add('campo-invalido');
            chips[0].chip.focus();
        });
        select.addEventListener('change', () => campo.classList.remove('campo-invalido'));

        const ayuda = campo.querySelector('[data-ayuda-rubros]');
        if (ayuda) ayuda.textContent = 'Tocá uno o más rubros para seleccionarlos.';
    });

    /* ---------- Vista previa de imágenes elegidas ---------- */
    const limpiadoresPrevia = [];
    document.querySelectorAll('.campo input[type="file"]').forEach((entrada) => {
        const previa = document.createElement('div');
        previa.className = 'vista-previa';
        previa.hidden = true;
        previa.setAttribute('aria-live', 'polite');
        entrada.insertAdjacentElement('afterend', previa);

        let urlActual = null;
        const limpiar = () => {
            if (urlActual) URL.revokeObjectURL(urlActual);
            urlActual = null;
            previa.hidden = true;
            previa.textContent = '';
        };

        entrada.addEventListener('change', () => {
            limpiar();
            const archivo = entrada.files && entrada.files[0];
            if (!archivo) return;
            if (archivo.type.startsWith('image/')) {
                urlActual = URL.createObjectURL(archivo);
                const img = document.createElement('img');
                img.src = urlActual;
                img.alt = '';
                previa.appendChild(img);
            }
            const nombre = document.createElement('span');
            nombre.textContent = `${archivo.name} · ${(archivo.size / 1024).toFixed(0)} KB`;
            previa.appendChild(nombre);
            previa.hidden = false;
        });
        limpiadoresPrevia.push(limpiar);
    });

    /* ---------- Al limpiar un formulario, refrescar los extras visuales ---------- */
    document.querySelectorAll('form').forEach((formulario) => {
        formulario.addEventListener('reset', () => {
            // El reset nativo se aplica después del evento: esperar un ciclo
            setTimeout(() => {
                contadores.forEach((fn) => fn());
                sincronizadores.forEach((fn) => fn());
                limpiadoresPrevia.forEach((fn) => fn());
            }, 0);
        });
    });
})();
