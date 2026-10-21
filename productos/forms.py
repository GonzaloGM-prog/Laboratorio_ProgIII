from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['artesano', 'nombre', 'precio', 'imagen', 'descripcion']
        widgets = {
            'artesano': forms.Select(attrs={'class': 'form-select'}),
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