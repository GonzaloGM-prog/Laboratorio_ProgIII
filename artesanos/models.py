from django.db import models
from django.conf import settings

class Rubro(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100, default='Catamarca')

    def __str__(self):
        return self.nombre

class Artesano(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='artesano')
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT,
                                  related_name='artesanos')
    rubros = models.ManyToManyField(Rubro, related_name='artesanos')
    nombre = models.CharField(max_length=200)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    descripcion = models.TextField(blank=True)
    foto = models.ImageField(upload_to='artesanos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('cambios', 'Requiere cambios'),
    ]
    artesano = models.ForeignKey(Artesano, on_delete=models.CASCADE,
                                 related_name='solicitudes')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f'Solicitud {self.id} - {self.artesano} ({self.get_estado_display()})'
