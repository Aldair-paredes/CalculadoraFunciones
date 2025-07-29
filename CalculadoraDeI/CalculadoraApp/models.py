from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES = (
        ('alumno', 'Alumno'),
        ('maestro', 'Maestro'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES, default='alumno')

    def __str__(self):
        return f"{self.user.username} ({self.rol})"
