from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROL_CHOICES = (
        ('alumno', 'Alumno'),
        ('maestro', 'Maestro'),
    )
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

# Create your models here.
