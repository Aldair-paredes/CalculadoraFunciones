from django.shortcuts import render, redirect
from .models import Pregunta, Opcion
import random

def quiz_view(request):
    if request.method == 'POST':
        puntuacion = 0
        preguntas_respondidas = 0
        for key, value in request.POST.items():
            if key.startswith('pregunta_'):
                try:
                    pregunta_id = key.split('_')[1]
                    pregunta = Pregunta.objects.get(id=pregunta_id)
                    preguntas_respondidas += 1

                    if pregunta.tipo_pregunta == 'VF':
                        respuesta_usuario = True if value == 'true' else False
                        if pregunta.respuesta_correcta_vf == respuesta_usuario:
                            puntuacion += 1
                    elif pregunta.tipo_pregunta == 'OM':
                        opcion_seleccionada_id = int(value)
                        opcion_correcta = pregunta.opciones.get(es_correcta=True)
                        if opcion_seleccionada_id == opcion_correcta.id:
                            puntuacion += 1
                except Pregunta.DoesNotExist:
                    continue 
                except Opcion.DoesNotExist:
                    continue 

        return render(request, 'quiz_app/resultado.html', {'puntuacion': puntuacion, 'total_preguntas': preguntas_respondidas})

    else:
       
        preguntas_disponibles = list(Pregunta.objects.all())
        random.shuffle(preguntas_disponibles)
        preguntas = preguntas_disponibles[:5] # Muestra 5 preguntas al azar

        return render(request, 'preguntas/quiz.html', {'preguntas': preguntas})

# Create your views here.
