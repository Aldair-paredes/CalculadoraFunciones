# En preguntas/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Pregunta, Opcion
import random

def quiz_view(request):
    
    todas_las_preguntas = list(Pregunta.objects.all().prefetch_related('opciones')) # Optimiza la carga de opciones

    if not todas_las_preguntas:
        return render(request, 'preguntas/quiz.html', {'pregunta': None, 'total_preguntas': 0, 'pregunta_actual_idx': 0})

    
    if 'quiz_preguntas_ids' not in request.session or request.GET.get('reiniciar'):
        random.shuffle(todas_las_preguntas)
        # Seleccionamos las primeras 5 preguntas para el quiz
        preguntas_para_quiz = todas_las_preguntas[:5]
        request.session['quiz_preguntas_ids'] = [p.id for p in preguntas_para_quiz]
        request.session['respuestas_contestadas'] = {} 
        request.session['pregunta_actual_idx'] = 0
        request.session.modified = True 

    quiz_preguntas_ids = request.session.get('quiz_preguntas_ids')
    respuestas_contestadas = request.session.get('respuestas_contestadas', {})
    pregunta_actual_idx = request.session.get('pregunta_actual_idx', 0)
    total_preguntas = len(quiz_preguntas_ids)

    if request.method == 'POST':
        # Procesar la respuesta de la pregunta actual
        pregunta_id_actual = quiz_preguntas_ids[pregunta_actual_idx]
        respuesta_key = f'respuesta_pregunta_{pregunta_id_actual}'

        if respuesta_key in request.POST:
            respuesta_dada = request.POST[respuesta_key]
            respuestas_contestadas[str(pregunta_id_actual)] = respuesta_dada # Almacena la respuesta
            request.session['respuestas_contestadas'] = respuestas_contestadas
            request.session.modified = True # Guarda los cambios en la sesión

            # Mover a la siguiente pregunta
            request.session['pregunta_actual_idx'] += 1
            request.session.modified = True # Guarda los cambios

            # Verificar si es la última pregunta o si se terminó el quiz
            if request.session['pregunta_actual_idx'] >= total_preguntas:
                # Calcular puntuación final
                puntuacion = 0
                for p_id_str, resp_dada in respuestas_contestadas.items():
                    try:
                        pregunta = Pregunta.objects.get(id=int(p_id_str))
                        if pregunta.tipo_pregunta == 'VF':
                            respuesta_correcta = 'true' if pregunta.respuesta_correcta_vf else 'false'
                            if resp_dada == respuesta_correcta:
                                puntuacion += 1
                        elif pregunta.tipo_pregunta == 'OM':
                            opcion_correcta = pregunta.opciones.get(es_correcta=True)
                            if str(opcion_correcta.id) == resp_dada:
                                puntuacion += 1
                    except (Pregunta.DoesNotExist, Opcion.DoesNotExist):
                        continue # Ignorar preguntas o opciones que no existan

                # Limpiar sesión del quiz
                del request.session['quiz_preguntas_ids']
                del request.session['respuestas_contestadas']
                del request.session['pregunta_actual_idx']
                request.session.modified = True # Guarda los cambios

                return render(request, 'preguntas/resultado.html', {'puntuacion': puntuacion, 'total_preguntas': total_preguntas})
            else:
                # Redirigir a la misma vista para mostrar la siguiente pregunta
                return redirect(reverse('preguntas:quiz_view')) # Redirige para evitar reenvío de formulario
        else:
           
            pregunta = Pregunta.objects.get(id=quiz_preguntas_ids[pregunta_actual_idx])
            context = {
                'pregunta': pregunta,
                'pregunta_actual_idx': pregunta_actual_idx,
                'total_preguntas': total_preguntas,
                'respuestas_contestadas': respuestas_contestadas,
                'error_mensaje': 'Por favor, selecciona una opción antes de continuar.'
            }
            return render(request, 'preguntas/quiz.html', context)

    else: # GET request
        if pregunta_actual_idx < total_preguntas:
            pregunta_id_a_mostrar = quiz_preguntas_ids[pregunta_actual_idx]
            pregunta = Pregunta.objects.get(id=pregunta_id_a_mostrar)
            context = {
                'pregunta': pregunta,
                'pregunta_actual_idx': pregunta_actual_idx,
                'total_preguntas': total_preguntas,
                'respuestas_contestadas': respuestas_contestadas,
            }
            return render(request, 'preguntas/quiz.html', context)
        else:
           
            return redirect(reverse('preguntas:quiz_view') + '?reiniciar=true') # Reinicia el quiz si ya no hay más preguntas

# Create your views here.
