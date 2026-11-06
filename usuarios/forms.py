from django import forms
from django.contrib.auth.forms import AuthenticationForm


class IngresoForm(AuthenticationForm):
    """Login de artesanos: el usuario es el DNI con el que se postularon."""

    username = forms.CharField(
        label='Usuario o DNI',
        widget=forms.TextInput(attrs={
            'id': 'usuario', 'autofocus': True, 'autocomplete': 'username',
            'placeholder': 'Ej: 30123456',
        }),
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'password', 'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': 'Usuario o contraseña incorrectos. Revisá los datos e intentá de nuevo.',
        'inactive': 'Esta cuenta está inactiva.',
    }
