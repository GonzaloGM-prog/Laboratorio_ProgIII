from django import forms
from django.contrib.auth.password_validation import validate_password

from usuarios.models import Usuario
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
    # Contraseña para ingresar luego a cargar productos (usuario = DNI)
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'password', 'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Repetir contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'password2', 'autocomplete': 'new-password'}),
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

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        # El DNI es también el usuario para ingresar: no puede repetirse
        if Usuario.objects.filter(username=dni).exists():
            raise forms.ValidationError('Ya existe una cuenta con este DNI. Ingresá con tu contraseña.')
        return dni

    def clean(self):
        datos = super().clean()
        password = datos.get('password')
        password2 = datos.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        elif password:
            try:
                validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password', error)
        return datos