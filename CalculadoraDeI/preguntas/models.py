from django.db import models

class Pregunta(models.Model):
    texto_pregunta= models.TextField(verbose_name= "Enunciado de la pregunta")
    TIPOS_PREGUNTA = [
        ('multiple_choice', 'Opción Múltiple'),
        ('true_false', 'Verdadero o Falso'),
    ]
    tipo_pregunta = models.CharField(
        max_length=20,
        choices=TIPOS_PREGUNTA,
        default='multiple_choice', 
        verbose_name="Tipo de pregunta"
    )
    respuesta_correcta_tf = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Respuesta Correcta (Verdadero/Falso)",
        help_text="Solo para preguntas de Verdadero o Falso. Marcar si la afirmación es Verdadera."
    )

    def __str__(self):
        
        return self.texto_pregunta

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

class Opcion(models.Model):
    
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='opciones', 
        limit_choices_to={'tipo_pregunta': 'multiple_choice'} 
    )

    texto_opcion = models.CharField(max_length=255, verbose_name="Texto de la opción")

    es_correcta = models.BooleanField(default=False, verbose_name="¿Es la respuesta correcta?")

    def __str__(self):
        
        return f"{self.texto_opcion} (Correcta: {self.es_correcta})"

    class Meta:
        verbose_name = "Opción de Respuesta"
        verbose_name_plural = "Opciones de Respuesta"
        
        unique_together = ('pregunta', 'texto_opcion')
    

# Create your models here.
