from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario
from .roles import sincronizar_grupo


class UsuarioCreationForm(UserCreationForm):
    """Formulario de alta apuntado al Usuario propio, con el campo rol."""

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('rol',)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """El admin de Django se usa SOLO para usuarios, roles y permisos."""

    add_form = UsuarioCreationForm
    fieldsets = UserAdmin.fieldsets + (
        ('Rol en Poncho Digital', {'fields': ('rol',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'rol', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'rol', 'grupos', 'is_staff')
    list_filter = UserAdmin.list_filter + ('rol',)
    search_fields = ('username', 'first_name', 'last_name', 'email')

    @admin.display(description='Grupos')
    def grupos(self, obj):
        return ', '.join(g.name for g in obj.groups.all()) or '—'

    def save_related(self, request, form, formsets, change):
        # Primero se guardan los grupos elegidos en el formulario;
        # después se asegura que el usuario esté en el grupo de su rol.
        super().save_related(request, form, formsets, change)
        sincronizar_grupo(form.instance)
