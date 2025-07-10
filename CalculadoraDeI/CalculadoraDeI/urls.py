from django.contrib import admin
from django.urls import path
from CalculadoraApp import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.pagprincipal, name='pagprincipal'),
    path('calculadora_explicita/', views.calculadora_explicita, name='calculadora_explicita'),
    path('temas/', views.temas, name='temas'),
    path('tema_funciones/', views.tema_funciones, name='tema_funciones'),
    path('calculadora-transcendente/', views.calculadora_transcendente, name='calculadora_transcendente'),
    path('calculadora-biyectiva/', views.calculadora_biyectiva, name='calculadora_biyectiva'),
     path('calculadora-transcendente/', views.calculadora_transcendente, name='calculadora_transcendente'),
     path('calculadora-algebraica/', views.calculadora_algebraica, name='calculadora_algebraica'),

]
