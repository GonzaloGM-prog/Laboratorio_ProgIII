from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from artesanos.models import Rubro
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
