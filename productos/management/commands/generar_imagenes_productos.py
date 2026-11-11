"""Genera una imagen ilustrada para cada producto que todavía no tiene foto.

Uso:
    python manage.py generar_imagenes_productos          # solo productos sin imagen
    python manage.py generar_imagenes_productos --todos  # también reemplaza las existentes

Las imágenes son ilustraciones generadas por código (colores y guardas inspirados
en los textiles del norte), no fotografías. Para usar fotos reales, se suben desde
el formulario de "Modificar producto".
"""
import hashlib
import io

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from productos.models import Producto

ANCHO, ALTO = 800, 600

# (fondo, franja principal, franja secundaria, detalle, texto)
PALETAS = [
    ((122, 24, 24), (214, 160, 58), (245, 233, 214), (60, 20, 20), (255, 248, 235)),
    ((46, 70, 92), (226, 167, 72), (240, 226, 200), (24, 36, 50), (255, 250, 240)),
    ((96, 58, 38), (200, 120, 60), (240, 222, 190), (50, 28, 18), (255, 246, 230)),
    ((44, 88, 72), (222, 176, 80), (238, 228, 200), (22, 44, 36), (255, 250, 238)),
    ((88, 42, 88), (230, 150, 70), (244, 226, 210), (44, 20, 44), (255, 246, 236)),
]


def _fuente(tamano):
    for nombre in ('DejaVuSans-Bold.ttf', 'arialbd.ttf', 'arial.ttf'):
        try:
            return ImageFont.truetype(nombre, tamano)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=tamano)
    except TypeError:
        return ImageFont.load_default()


def _renglones(dibujo, texto, fuente, ancho_max):
    renglones, actual = [], ''
    for palabra in texto.split():
        prueba = f'{actual} {palabra}'.strip()
        if dibujo.textlength(prueba, font=fuente) <= ancho_max or not actual:
            actual = prueba
        else:
            renglones.append(actual)
            actual = palabra
    if actual:
        renglones.append(actual)
    return renglones[:3]


def crear_imagen(nombre, rubro, artesano):
    """Devuelve los bytes JPEG de la ilustración de un producto."""
    semilla = int(hashlib.md5(f'{rubro}{nombre}'.encode('utf-8')).hexdigest(), 16)
    fondo, principal, secundario, detalle, texto = PALETAS[semilla % len(PALETAS)]

    imagen = Image.new('RGB', (ANCHO, ALTO), fondo)
    d = ImageDraw.Draw(imagen)

    # Franjas horizontales arriba y abajo
    for y, alto, color in ((0, 34, principal), (40, 12, secundario),
                           (ALTO - 34, 34, principal), (ALTO - 52, 12, secundario)):
        d.rectangle([0, y, ANCHO, y + alto], fill=color)

    # Guarda de rombos
    lado = 46
    for fila, (y, color) in enumerate(((78, principal), (ALTO - 124, principal))):
        for i in range(-1, ANCHO // lado + 2):
            x = i * lado + (lado // 2 if fila else 0)
            d.polygon([(x, y + lado // 2), (x + lado // 2, y), (x + lado, y + lado // 2),
                       (x + lado // 2, y + lado)], fill=color)
            d.polygon([(x + 12, y + lado // 2), (x + lado // 2, y + 12), (x + lado - 12, y + lado // 2),
                       (x + lado // 2, y + lado - 12)], fill=detalle)

    # Panel central con el nombre
    d.rounded_rectangle([70, 170, ANCHO - 70, ALTO - 170], radius=26, fill=detalle)
    d.rounded_rectangle([82, 182, ANCHO - 82, ALTO - 182], radius=20, outline=principal, width=4)

    fuente_nombre, fuente_pie = _fuente(50), _fuente(26)
    lineas = _renglones(d, nombre, fuente_nombre, ANCHO - 200)
    alto_linea = 60
    y = ALTO // 2 - (len(lineas) * alto_linea) // 2 - 14
    for linea in lineas:
        d.text((ANCHO // 2, y), linea, font=fuente_nombre, fill=texto, anchor='mt')
        y += alto_linea
    pie = ' · '.join(p for p in (rubro, artesano) if p)
    if pie:
        d.text((ANCHO // 2, ALTO - 214), pie[:48], font=fuente_pie, fill=principal, anchor='mb')

    buffer = io.BytesIO()
    imagen.save(buffer, 'JPEG', quality=88)
    return buffer.getvalue()


class Command(BaseCommand):
    help = 'Genera imágenes ilustradas para los productos sin imagen (o para todos con --todos).'

    def add_arguments(self, parser):
        parser.add_argument('--todos', action='store_true',
                            help='Reemplaza también las imágenes que ya tienen cargadas.')

    def handle(self, *args, **opciones):
        productos = Producto.objects.select_related('artesano', 'rubro')
        if not opciones['todos']:
            productos = productos.filter(imagen='') | productos.filter(imagen__isnull=True)

        cantidad = 0
        for p in productos:
            datos = crear_imagen(p.nombre, str(p.rubro or ''), p.artesano.nombre)
            p.imagen.save(f'producto_{p.pk}.jpg', ContentFile(datos), save=True)
            cantidad += 1
            self.stdout.write(f'  Imagen generada: {p.nombre}')
        self.stdout.write(self.style.SUCCESS(f'Listo: {cantidad} imagen(es) generada(s).'))
