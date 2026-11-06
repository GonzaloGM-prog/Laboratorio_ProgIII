"""Roles y grupos de permisos de Poncho Digital.

- El campo `rol` del Usuario es una etiqueta (admin / artesano / visitante).
- Los permisos reales los dan los GRUPOS de Django (uno por rol).
Este módulo crea los grupos con sus permisos y mantiene al usuario
en el grupo que corresponde a su rol.
"""
from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission

# rol del modelo Usuario -> nombre del grupo
GRUPO_DE_ROL = {
    'admin': 'Administrador',
    'artesano': 'Artesano',
    'visitante': 'Visitante',
}

# Permisos de cada grupo, como 'app.codename'
PERMISOS_POR_GRUPO = {
    'Visitante': [],  # solo mira el catálogo público
    'Artesano': [
        'productos.add_producto', 'productos.change_producto',
        'productos.delete_producto', 'productos.view_producto',
        'stands.view_stand',
    ],
    'Administrador': [
        'productos.add_producto', 'productos.change_producto',
        'productos.delete_producto', 'productos.view_producto',
        'artesanos.view_solicitud', 'artesanos.change_solicitud',
        'artesanos.view_artesano', 'artesanos.change_artesano',
        'stands.add_stand', 'stands.change_stand',
        'stands.delete_stand', 'stands.view_stand',
    ],
}


def configurar_grupos():
    """Crea (o actualiza) los grupos con sus permisos. Se puede correr muchas veces."""
    # Asegura que existan los permisos aunque la base sea nueva
    for etiqueta in ('artesanos', 'productos', 'stands'):
        create_permissions(apps.get_app_config(etiqueta), verbosity=0)

    for nombre, permisos in PERMISOS_POR_GRUPO.items():
        grupo, _ = Group.objects.get_or_create(name=nombre)
        objetos = []
        for permiso in permisos:
            app_label, codename = permiso.split('.')
            objetos.append(Permission.objects.get(content_type__app_label=app_label, codename=codename))
        grupo.permissions.set(objetos)


def asignar_rol(usuario, rol):
    """Pone el rol al usuario y lo deja solo en el grupo de ese rol."""
    if not Group.objects.filter(name=GRUPO_DE_ROL[rol]).exists():
        configurar_grupos()
    usuario.rol = rol
    usuario.save(update_fields=['rol'])
    sincronizar_grupo(usuario)


def sincronizar_grupo(usuario):
    """Saca al usuario de los grupos de otros roles y lo agrega al de su rol."""
    grupos_de_roles = Group.objects.filter(name__in=GRUPO_DE_ROL.values())
    usuario.groups.remove(*grupos_de_roles.exclude(name=GRUPO_DE_ROL[usuario.rol]))
    grupo = grupos_de_roles.filter(name=GRUPO_DE_ROL[usuario.rol]).first()
    if grupo is None:
        configurar_grupos()
        grupo = Group.objects.get(name=GRUPO_DE_ROL[usuario.rol])
    usuario.groups.add(grupo)


def es_administrador(usuario):
    """Administrador del sitio: rol admin o superusuario."""
    return usuario.is_authenticated and (usuario.is_superuser or usuario.rol == 'admin')
