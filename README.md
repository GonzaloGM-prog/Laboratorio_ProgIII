 PONCHO DIGITAL
 
Descripción del proyecto

Poncho Digital es una plataforma web desarrollada como trabajo de laboratorio para la cátedra Programación III de la carrera de Ingeniería en Informática – U.N.Ca.

El sistema tiene como objetivo brindar información sobre los artesanos y productores que participan de la Fiesta Nacional e Internacional del Poncho, facilitando a los visitantes la búsqueda de artesanos, productos y ubicación de los stands.

La aplicación busca mejorar la experiencia de los visitantes y favorecer la difusión de los emprendimientos participantes.

## Integrantes del equipo

Cátedra Programación III · Ingeniería en Informática · Facultad de Tecnología y Ciencias Aplicadas (U.N.Ca.)

| Integrante | Matrícula | Usuario de GitHub |
|---|---|---|
| Barros Barrionuevo, Amira Virginia | M.U. 01866 | [amiibarros](https://github.com/amiibarros) |
| Gil Miranda, Gonzalo | M.U. 01921 | [GonzaloGM-prog](https://github.com/GonzaloGM-prog) |
| Gallo, Jorge Joaquín | M.U. 01959 | [gallojoaquin48-lang](https://github.com/gallojoaquin48-lang) |
| Lopez Macias, Leon | M.U. 01949 | [lopez-macias-leon](https://github.com/lopez-macias-leon) |

Repositorio: https://github.com/GonzaloGM-prog/Laboratorio_ProgIII

## Tecnologías y versiones

| Componente | Versión |
|---|---|
| Python | 3.12 |
| Django | 6.1.2 |
| PostgreSQL | Motor de base de datos del proyecto |
| psycopg2-binary | 2.9.13 |
| Pillow | 12.3.0 |
| python-decouple | 3.8 |
| asgiref | 3.12.1 |
| sqlparse | 0.6.0 |
| tzdata | 2026.5 |
| setuptools | 84.0.0 |

Las versiones exactas están fijadas en `requirements.txt`.

## Cómo ejecutarlo

1. Crear el entorno virtual e instalar dependencias:
   ```
   py -3.12 -m venv env_poncho
   .\env_poncho\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Crear la base `poncho_digital` en PostgreSQL y el archivo `.env` (copiar `.env.example` y completarlo).
3. Crear las tablas y cargar los datos de ejemplo:
   ```
   python manage.py migrate
   python manage.py cargar_datos_ejemplo
   ```
4. Levantar el servidor: `python manage.py runserver` y abrir http://127.0.0.1:8000/

`cargar_datos_ejemplo` se puede correr varias veces: no duplica datos y deja las contraseñas de demo como se indica abajo.

## Usuarios de demo

| Rol | Usuario | Contraseña | Qué puede hacer |
|---|---|---|---|
| Administrador | `admin` | `Admin2026!` | Aprobar/rechazar solicitudes, asignar stands, modificar o eliminar cualquier producto, admin de Django |
| Artesano (aprobado) | `30123456` (Rosa Quiroga) | `Poncho2026` | Agregar, modificar y eliminar **sus** productos; ver stands |
| Artesano (aprobado) | `28456789` (Martín Carrizo) | `Ceramica2026` | Igual que el anterior |
| Postulante (pendiente) | `35678901` (Lucía Herrera) | `Plata2026` | Ve el estado de su solicitud |
| Postulante (pendiente) | `32109876` (Jorge Villagra) | `Madera2026` | Ve el estado de su solicitud |
| Visitante | `visitante1` | `Visita2026` | Solo mira el catálogo |

Sin iniciar sesión también se puede ver el catálogo de productos.

## Roles y permisos

- El campo `rol` del usuario es una etiqueta; los **permisos reales los dan los grupos** de Django (`Visitante`, `Artesano`, `Administrador`), definidos en `usuarios/roles.py`.
- Al cambiar el rol de un usuario (en el admin o al aprobar una solicitud) se lo pasa automáticamente al grupo de ese rol.
- Las vistas se protegen con `@login_required` y `@permission_required(..., raise_exception=True)` (403 si no tiene permiso), y además se controla que el producto sea del artesano (*ownership*). Los templates solo esconden los botones con `{% if perms... %}`.
- El admin de Django se usa **solo** para usuarios, roles y grupos (`usuarios/admin.py`). Todo lo demás está hecho con vistas y templates.

## Flujo de una postulación

1. El visitante completa **Postularme** (con DNI y contraseña): se crea su usuario con rol *visitante* y una solicitud *pendiente*.
2. El administrador entra a **Solicitudes** y la aprueba o la rechaza (por POST, con motivo opcional).
3. Si se aprueba, el usuario pasa a rol *artesano* (grupo Artesano) y ya puede cargar productos.
