from django.contrib import admin
from django.urls import include, path
from CalculadoraApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('preguntas.urls', namespace='preguntas')),



path('', views.pagprincipal, name='pagprincipal'),
    path('calculadora_explicita/', views.calculadora_explicita, name='calculadora_explicita'),
    path('temas/', views.temas, name='temas'),
    path('tema_funciones/', views.tema_funciones, name='tema_funciones'),
     path('calculadora-transcendente/', views.calculadora_transcendente, name='calculadora_transcendente'),
     path('calculadora-algebraica/', views.calculadora_algebraica, name='calculadora_algebraica'),
     path('graficador/', views.graficador_funciones, name='graficador_funciones'),

]
