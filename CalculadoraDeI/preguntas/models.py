from django.db import models

class Pregunta(models.Model):
    TIPO_PREGUNTA_CHOICES = [
        ('VF', 'Verdadero/Falso'),
        ('OM', 'Opción Múltiple'),
    ]
    texto_pregunta = models.CharField(max_length=255)
    tipo_pregunta = models.CharField(max_length=2, choices=TIPO_PREGUNTA_CHOICES)
    respuesta_correcta_vf = models.BooleanField(null=True, blank=True) # Para preguntas de Verdadero/Falso

    def __str__(self):
        return self.texto_pregunta

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto_opcion = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto_opcion
    

# Create your models here.
