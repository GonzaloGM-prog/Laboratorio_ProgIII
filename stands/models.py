from django.db import models

class Stand(models.Model):
    artesano = models.ForeignKey('artesanos.Artesano', on_delete=models.CASCADE,
                                 related_name='stands')
    numero = models.CharField(max_length=20, unique=True)
    ubicacion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Stand {self.numero} - {self.artesano}'