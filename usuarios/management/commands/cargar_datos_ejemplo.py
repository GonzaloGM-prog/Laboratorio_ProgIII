"""Carga los datos de ejemplo para la demo del laboratorio.

Uso:  python manage.py cargar_datos_ejemplo

Se puede correr varias veces: no duplica datos (usa get_or_create) y
vuelve a dejar las contraseñas de las cuentas de demo como se indica abajo.
"""
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from artesanos.models import Artesano, Localidad, Rubro, Solicitud
from productos.models import Producto
from stands.models import Stand
from usuarios.models import Usuario
from usuarios.roles import asignar_rol, configurar_grupos

LOCALIDADES = ['San Fernando del Valle de Catamarca', 'Belén', 'Andalgalá', 'Tinogasta',
               'Santa María', 'Fiambalá', 'Valle Viejo', 'Pomán']
RUBROS = ['Textiles', 'Cerámica', 'Platería', 'Tallado en madera', 'Cestería', 'Cuero',
          'Gastronomía regional']

# (usuario, contraseña, nombre, apellido, rol, es_superusuario)
CUENTAS = [
    ('admin', 'Admin2026!', 'Administración', 'Poncho', 'admin', True),
    ('visitante1', 'Visita2026', 'Valeria', 'Ríos', 'visitante', False),
]

# Artesanos: DNI = usuario para ingresar
ARTESANOS = [
    {
        'dni': '30123456', 'clave': 'Poncho2026', 'nombre': 'Rosa', 'apellido': 'Quiroga',
        'localidad': 'Belén', 'rubros': ['Textiles'], 'telefono': '3835123456', 'estado': 'aprobada',
        'descripcion': 'Tejedora de ponchos y mantas en telar criollo, con lana de llama y vicuña '
                       'teñida con tintes naturales.',
        'productos': [
            ('Poncho de vicuña', 'Textiles', 450000, 'Poncho tejido a mano en telar criollo con fibra de vicuña.'),
            ('Manta de llama', 'Textiles', 180000, 'Manta de lana de llama con guarda de rombos teñida con nogal.'),
            ('Camino de mesa', 'Textiles', 65000, 'Camino de mesa en telar con flecos anudados a mano.'),
        ],
        'stands': [('A-01', 'Pabellón Textil, pasillo 1')],
    },
    {
        'dni': '28456789', 'clave': 'Ceramica2026', 'nombre': 'Martín', 'apellido': 'Carrizo',
        'localidad': 'Andalgalá', 'rubros': ['Cerámica'], 'telefono': '3835987654', 'estado': 'aprobada',
        'descripcion': 'Alfarero: vasijas y piezas utilitarias de barro cocido con diseños diaguitas.',
        'productos': [
            ('Vasija diaguita', 'Cerámica', 38000, 'Vasija de barro cocido pintada con motivos diaguitas.'),
            ('Jarra pintada', 'Cerámica', 27000, 'Jarra utilitaria de cerámica esmaltada.'),
            ('Juego de cuencos', 'Cerámica', 22000, 'Tres cuencos de barro para cocina regional.'),
        ],
        'stands': [('B-07', 'Pabellón de Cerámica y Alfarería')],
    },
    # Solicitudes pendientes, para aprobar en vivo
    {
        'dni': '35678901', 'clave': 'Plata2026', 'nombre': 'Lucía', 'apellido': 'Herrera',
        'localidad': 'Santa María', 'rubros': ['Platería'], 'telefono': '3838456123', 'estado': 'pendiente',
        'descripcion': 'Platera: aros, prendedores y mates labrados en alpaca y plata.',
        'productos': [], 'stands': [],
    },
    {
        'dni': '32109876', 'clave': 'Madera2026', 'nombre': 'Jorge', 'apellido': 'Villagra',
        'localidad': 'Tinogasta', 'rubros': ['Tallado en madera', 'Cestería'], 'telefono': '3837321654',
        'estado': 'pendiente',
        'descripcion': 'Tallador en madera de algarrobo y cestero en fibra de simbol.',
        'productos': [], 'stands': [],
    },
]


class Command(BaseCommand):
    help = 'Carga grupos, usuarios por rol, artesanos, productos, solicitudes y stands de ejemplo.'

    @transaction.atomic
    def handle(self, *args, **options):
        configurar_grupos()
        self.stdout.write('Grupos Visitante, Artesano y Administrador configurados.')

        for nombre in LOCALIDADES:
            Localidad.objects.get_or_create(nombre=nombre)
        for nombre in RUBROS:
            Rubro.objects.get_or_create(nombre=nombre)

        for usuario, clave, nombre, apellido, rol, superusuario in CUENTAS:
            u, _ = Usuario.objects.get_or_create(username=usuario)
            u.first_name, u.last_name = nombre, apellido
            u.is_staff = u.is_superuser = superusuario
            u.set_password(clave)
            u.save()
            asignar_rol(u, rol)

        for datos in ARTESANOS:
            self._cargar_artesano(datos)

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo cargados.'))
        self.stdout.write('Cuentas: admin / Admin2026!  ·  visitante1 / Visita2026')
        for d in ARTESANOS:
            self.stdout.write(f"  {d['nombre']} {d['apellido']} ({d['estado']}): {d['dni']} / {d['clave']}")

    def _cargar_artesano(self, d):
        u, _ = Usuario.objects.get_or_create(username=d['dni'])
        u.first_name, u.last_name = d['nombre'], d['apellido']
        u.email = f"{d['nombre'].lower()}.{d['apellido'].lower()}@ejemplo.com"
        u.set_password(d['clave'])
        u.save()

        artesano, _ = Artesano.objects.get_or_create(
            dni=d['dni'],
            defaults={
                'usuario': u,
                'localidad': Localidad.objects.get(nombre=d['localidad']),
                'nombre': f"{d['nombre']} {d['apellido']}",
                'telefono': d['telefono'],
                'descripcion': d['descripcion'],
            },
        )
        artesano.rubros.set(Rubro.objects.filter(nombre__in=d['rubros']))

        if not artesano.solicitudes.exists():
            Solicitud.objects.create(artesano=artesano, estado=d['estado'])
        # Rol y grupo según el estado de su solicitud
        aprobada = artesano.solicitudes.filter(estado='aprobada').exists()
        asignar_rol(u, 'artesano' if aprobada else 'visitante')

        for nombre, rubro, precio, descripcion in d['productos']:
            Producto.objects.get_or_create(
                artesano=artesano, nombre=nombre,
                defaults={'rubro': Rubro.objects.get(nombre=rubro), 'precio': Decimal(precio),
                          'descripcion': descripcion},
            )
        for numero, ubicacion in d['stands']:
            Stand.objects.get_or_create(numero=numero, defaults={'artesano': artesano, 'ubicacion': ubicacion})
