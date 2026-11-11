import csv
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from artesanos.models import Artesano, Rubro
from usuarios.roles import es_administrador
from .forms import ProductoForm, ProductoAdminForm
from .models import Producto


def _artesano_de(user):
    """Artesano asociado al usuario (None si no inició sesión o no es artesano)."""
    if not user.is_authenticated:
        return None
    return getattr(user, 'artesano', None)


def _puede_tocar(user, producto):
    """Ownership: el dueño del producto o un administrador."""
    return es_administrador(user) or producto.artesano.usuario_id == user.pk


def lista(request):
    """Catálogo público: cualquiera puede mirar. Los botones dependen de los permisos."""
    productos = Producto.objects.select_related('artesano__localidad', 'rubro').order_by('nombre')

    # Filtros del catálogo
    busqueda = request.GET.get('q', '').strip()
    rubro_id = request.GET.get('rubro', '')
    if busqueda:
        productos = productos.filter(Q(nombre__icontains=busqueda) | Q(artesano__nombre__icontains=busqueda))
    if rubro_id.isdigit():
        productos = productos.filter(rubro_id=rubro_id)

    artesano = _artesano_de(request.user)
    solicitud = artesano.solicitudes.order_by('-fecha').first() if artesano else None
    mis_productos = (Producto.objects.filter(artesano=artesano).select_related('rubro').order_by('nombre')
                     if artesano else None)

    return render(request, 'productos/lista.html', {
        'productos': productos,
        'rubros': Rubro.objects.order_by('nombre'),
        'busqueda': busqueda,
        'rubro_id': rubro_id,
        'artesano': artesano,
        'solicitud': solicitud,
        'mis_productos': mis_productos,
        'es_admin': es_administrador(request.user),
    })


@login_required
@permission_required('productos.add_producto', raise_exception=True)
def agregar(request):
    artesano = _artesano_de(request.user)
    admin = es_administrador(request.user)
    if artesano is None and not admin:
        raise PermissionDenied
    Formulario = ProductoForm if artesano else ProductoAdminForm

    if request.method == 'POST':
        form = Formulario(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            if artesano:
                producto.artesano = artesano  # el producto es de quien lo carga
            producto.save()
            messages.success(request, 'Producto agregado correctamente.')
            return redirect('productos:lista')
    else:
        form = Formulario()
    return render(request, 'productos/producto_form.html', {
        'form': form, 'artesano': artesano, 'modo': 'agregar',
    })


@login_required
@permission_required('productos.change_producto', raise_exception=True)
def editar(request, pk):
    producto = get_object_or_404(Producto.objects.select_related('artesano'), pk=pk)
    if not _puede_tocar(request.user, producto):
        raise PermissionDenied  # 403: no es su producto
    Formulario = ProductoAdminForm if es_administrador(request.user) else ProductoForm

    if request.method == 'POST':
        form = Formulario(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto modificado correctamente.')
            return redirect('productos:lista')
    else:
        form = Formulario(instance=producto)
    return render(request, 'productos/producto_form.html', {
        'form': form, 'producto': producto, 'artesano': producto.artesano, 'modo': 'editar',
    })


@login_required
@permission_required('productos.delete_producto', raise_exception=True)
def eliminar(request, pk):
    producto = get_object_or_404(Producto.objects.select_related('artesano'), pk=pk)
    if not _puede_tocar(request.user, producto):
        raise PermissionDenied  # 403: no es su producto
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
    return redirect('productos:lista')


def _numero(valor):
    """Convierte un parámetro a Decimal; devuelve None si está vacío o es inválido."""
    try:
        return Decimal(valor.replace(',', '.')) if valor else None
    except InvalidOperation:
        return None


def _csv_productos(productos, nombre_archivo):
    """Arma la respuesta CSV (se abre en Excel) con los productos recibidos."""
    respuesta = HttpResponse(content_type='text/csv; charset=utf-8')
    respuesta['Content-Disposition'] = f'attachment; filename="{nombre_archivo}.csv"'
    respuesta.write('\ufeff')  # para que Excel respete las tildes
    escritor = csv.writer(respuesta, delimiter=';')
    escritor.writerow(['Producto', 'Rubro', 'Precio', 'Artesano', 'Localidad'])
    for p in productos:
        escritor.writerow([p.nombre, p.rubro or '', p.precio, p.artesano.nombre, p.artesano.localidad])
    return respuesta


@login_required
@permission_required('productos.view_producto', raise_exception=True)
def reporte_productos(request):
    """Reporte parametrizado de productos (solo administradores).

    Parámetros GET: q, rubro, artesano, precio_min, precio_max, orden.
    Sin 'descargar' muestra una vista previa; con 'descargar=1' entrega el CSV.
    """
    if not es_administrador(request.user):
        raise PermissionDenied

    filtros = {clave: request.GET.get(clave, '').strip()
               for clave in ('q', 'rubro', 'artesano', 'precio_min', 'precio_max', 'orden')}

    productos = Producto.objects.select_related('artesano__localidad', 'rubro')
    if filtros['q']:
        productos = productos.filter(nombre__icontains=filtros['q'])
    if filtros['rubro'].isdigit():
        productos = productos.filter(rubro_id=filtros['rubro'])
    if filtros['artesano'].isdigit():
        productos = productos.filter(artesano_id=filtros['artesano'])
    minimo, maximo = _numero(filtros['precio_min']), _numero(filtros['precio_max'])
    if minimo is not None:
        productos = productos.filter(precio__gte=minimo)
    if maximo is not None:
        productos = productos.filter(precio__lte=maximo)

    ordenes = {'nombre': 'nombre', 'precio': 'precio', '-precio': '-precio',
               'artesano': 'artesano__nombre'}
    productos = productos.order_by(ordenes.get(filtros['orden'], 'nombre'))

    if request.GET.get('descargar'):
        return _csv_productos(productos, 'reporte_productos')

    return render(request, 'productos/reporte.html', {
        'productos': productos,
        'filtros': filtros,
        'rubros': Rubro.objects.order_by('nombre'),
        'artesanos': (Artesano.objects.filter(solicitudes__estado='aprobada').distinct()
                      .annotate(total=Count('productos', distinct=True)).order_by('nombre')),
    })


@login_required
@permission_required('productos.view_producto', raise_exception=True)
def reporte_artesano(request, pk):
    """Reporte (CSV) de los productos de un solo artesano. Solo administradores."""
    if not es_administrador(request.user):
        raise PermissionDenied
    artesano = get_object_or_404(Artesano, pk=pk)
    productos = (Producto.objects.filter(artesano=artesano)
                 .select_related('artesano__localidad', 'rubro').order_by('nombre'))
    return _csv_productos(productos, f'reporte_{slugify(artesano.nombre)}')
