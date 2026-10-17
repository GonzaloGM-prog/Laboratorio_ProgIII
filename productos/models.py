from django.db import models

class Producto(models.Model):
    artesano = models.ForeignKey('artesanos.Artesano', on_delete=models.CASCADE,
                                 related_name='productos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre