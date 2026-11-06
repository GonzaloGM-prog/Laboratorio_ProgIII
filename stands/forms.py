from django import forms

from artesanos.models import Artesano
from .models import Stand


class StandForm(forms.ModelForm):
    class Meta:
        model = Stand
        fields = ['numero', 'ubicacion', 'artesano', 'activo']
        labels = {
            'numero': 'Número de stand',
            'ubicacion': 'Ubicación',
            'activo': 'Stand activo',
        }
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A-01'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pabellón Textil, pasillo 2'}),
            'artesano': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo se asignan stands a artesanos con la solicitud aprobada
        self.fields['artesano'].queryset = Artesano.objects.filter(
            solicitudes__estado='aprobada').distinct().order_by('nombre')
        self.fields['artesano'].empty_label = 'Elegí un artesano'
