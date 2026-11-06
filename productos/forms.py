from django import forms

from artesanos.models import Artesano
from .models import Producto


class ProductoForm(forms.ModelForm):
    """Formulario del artesano: el artesano no se elige, es el usuario logueado."""

    class Meta:
        model = Producto
        fields = ['rubro', 'nombre', 'precio', 'imagen', 'descripcion']
        widgets = {
            'rubro': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={
                'id': 'nombre', 'class': 'form-control',
                'placeholder': 'Ej: Poncho artesanal',
            }),
            'precio': forms.NumberInput(attrs={
                'id': 'precio', 'class': 'form-control',
                'placeholder': 'Ej: 50000', 'min': '0',
            }),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={
                'id': 'descripcion', 'class': 'form-control', 'rows': 5,
                'placeholder': 'Describí brevemente tu producto...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # En el modelo es blank=True, pero acá la pedimos
        self.fields['descripcion'].required = True
        # En el modelo es null=True (para productos ya cargados), pero acá la pedimos
        self.fields['rubro'].required = True
        self.fields['rubro'].empty_label = 'Elegí un rubro'


class ProductoAdminForm(ProductoForm):
    """Formulario del administrador: puede elegir a qué artesano pertenece el producto."""

    class Meta(ProductoForm.Meta):
        fields = ['artesano'] + ProductoForm.Meta.fields
        widgets = dict(ProductoForm.Meta.widgets, artesano=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo artesanos con la solicitud aprobada
        self.fields['artesano'].queryset = Artesano.objects.filter(
            solicitudes__estado='aprobada').distinct().order_by('nombre')
        self.fields['artesano'].empty_label = 'Elegí un artesano'
