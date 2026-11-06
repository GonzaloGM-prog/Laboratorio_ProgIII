from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

from .forms import StandForm
from .models import Stand


@login_required
@permission_required('stands.view_stand', raise_exception=True)
def lista(request):
    # select_related / prefetch_related evitan una consulta por cada fila
    stands = (Stand.objects.select_related('artesano__localidad')
              .prefetch_related('artesano__rubros').order_by('numero'))
    return render(request, 'stands/lista.html', {'stands': stands})


@login_required
@permission_required('stands.add_stand', raise_exception=True)
def agregar(request):
    if request.method == 'POST':
        form = StandForm(request.POST)
        if form.is_valid():
            stand = form.save()
            messages.success(request, f'Stand {stand.numero} asignado a {stand.artesano}.')
            return redirect('stands:lista')
    else:
        form = StandForm()
    return render(request, 'stands/stand_form.html', {'form': form})
