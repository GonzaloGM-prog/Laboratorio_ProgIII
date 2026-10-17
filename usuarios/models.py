from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('artesano', 'Artesano'),
        ('visitante', 'Visitante'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='visitante')

    def __str__(self):
        return self.username
