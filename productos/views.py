from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductoForm
from .models import Producto


def lista(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado correctamente.')
            return redirect('productos:lista')
    else:
        form = ProductoForm()

    productos = Producto.objects.select_related('artesano').prefetch_related('artesano__rubros')
    return render(request, 'productos/lista.html', {
        'productos': productos,
        'form': form,
    })


def editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto modificado correctamente.')
            return redirect('productos:lista')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/producto_form.html', {
        'form': form,
        'producto': producto,
    })


def eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
    return redirect('productos:lista')