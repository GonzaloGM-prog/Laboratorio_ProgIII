from django import forms
from .models import Artesano


class SolicitudForm(forms.ModelForm):
    # Campos que no son del modelo Artesano: se usan en la vista
    apellido = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'id': 'apellido'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'id': 'email'}),
    )
    aceptar = forms.BooleanField(
        label='Declaro que los datos ingresados son correctos.',
        widget=forms.CheckboxInput(attrs={'id': 'aceptar'}),
    )

    class Meta:
        model = Artesano
        fields = ['nombre', 'dni', 'telefono', 'localidad', 'rubros', 'descripcion', 'foto']
        labels = {
            'descripcion': 'Descripción del emprendimiento',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'id': 'nombre'}),
            'dni': forms.TextInput(attrs={'id': 'dni'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono'}),
            'descripcion': forms.Textarea(attrs={'id': 'descripcion', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # En el modelo son blank=True, pero en la solicitud los pedimos
        self.fields['telefono'].required = True
        self.fields['descripcion'].required = True