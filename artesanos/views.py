from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from usuarios.models import Usuario
from usuarios.roles import asignar_rol
from .forms import SolicitudForm
from .models import Solicitud


def solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST, request.FILES)
        if form.is_valid():
            datos = form.cleaned_data
            with transaction.atomic():
                usuario = Usuario.objects.create_user(
                    username=datos['dni'],
                    password=datos['password'],
                    email=datos['email'],
                    first_name=datos['nombre'],
                    last_name=datos['apellido'],
                )
                # Hasta que un administrador apruebe la solicitud es visitante
                asignar_rol(usuario, 'visitante')
                artesano = form.save(commit=False)
                artesano.usuario = usuario
                artesano.nombre = f"{datos['nombre']} {datos['apellido']}"
                artesano.save()
                form.save_m2m()
                Solicitud.objects.create(artesano=artesano)
            # Queda con la sesión iniciada para ver el estado de su solicitud
            login(request, usuario)
            messages.success(request, 'Solicitud enviada correctamente. Queda pendiente de aprobación: '
                                      'cuando la aprueben vas a poder cargar tus productos. '
                                      'Para volver a ingresar usá tu DNI y contraseña.')
            return redirect('productos:lista')
    else:
        form = SolicitudForm()
    return render(request, 'artesanos/solicitud_form.html', {'form': form})


@login_required
@permission_required('artesanos.change_solicitud', raise_exception=True)
def solicitudes(request):
    """Pantalla del administrador para revisar solicitudes (sin usar el admin de Django)."""
    base = Solicitud.objects.select_related('artesano__localidad').prefetch_related('artesano__rubros')
    return render(request, 'artesanos/solicitudes.html', {
        'pendientes': base.filter(estado='pendiente').order_by('fecha'),
        'resueltas': base.exclude(estado='pendiente').order_by('-fecha')[:10],
    })


@login_required
@permission_required('artesanos.change_solicitud', raise_exception=True)
@require_POST
def resolver_solicitud(request, pk, accion):
    if accion not in ('aprobar', 'rechazar'):
        raise Http404
    # Solo se resuelven solicitudes pendientes
    solicitud = get_object_or_404(Solicitud.objects.select_related('artesano__usuario'),
                                  pk=pk, estado='pendiente')
    solicitud.observaciones = request.POST.get('observaciones', '').strip()
    usuario = solicitud.artesano.usuario
    with transaction.atomic():
        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
            asignar_rol(usuario, 'artesano')  # pasa al grupo Artesano: ya puede cargar productos
            messages.success(request, f'Solicitud de {solicitud.artesano.nombre} aprobada.')
        else:
            solicitud.estado = 'rechazada'
            messages.warning(request, f'Solicitud de {solicitud.artesano.nombre} rechazada.')
        solicitud.save()
    return redirect('artesanos:solicitudes')
