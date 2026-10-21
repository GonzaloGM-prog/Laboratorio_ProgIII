
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect

from usuarios.models import Usuario
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
                    email=datos['email'],
                    first_name=datos['nombre'],
                    last_name=datos['apellido'],
                    rol='artesano',
                )
                artesano = form.save(commit=False)
                artesano.usuario = usuario
                artesano.nombre = f"{datos['nombre']} {datos['apellido']}"
                artesano.save()
                form.save_m2m()
                Solicitud.objects.create(artesano=artesano)
            messages.success(request, 'Solicitud enviada correctamente. Te vamos a contactar cuando sea revisada.')
            return redirect('artesanos:solicitud')
    else:
        form = SolicitudForm()
    return render(request, 'artesanos/solicitud_form.html', {'form': form})