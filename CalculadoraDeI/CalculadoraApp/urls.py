from django.urls import path
from CalculadoraApp import views
from .views import registro_view, login_view, logout_view
from django.contrib import admin

urlpatterns = [
    path('', views.pagprincipal, name='pagprincipal'),
    path('calculadora_explicita/', views.calculadora_explicita, name='calculadora_explicita'),
    path('funcion_implicita/', views.funcion_implicita_view, name='funcion_implicita'),
    path('temas/', views.temas, name='temas'),
    path('tema_funciones/', views.tema_funciones, name='tema_funciones'),
    path('calculadora-transcendente/', views.calculadora_transcendente, name='calculadora_transcendente'),
    path('calculadora-biyectiva/', views.calculadora_biyectiva, name='calculadora_biyectiva'),
    path('calculadora-algebraica/', views.calculadora_algebraica, name='calculadora_algebraica'),
    path('graficador_funciones/', views.graficador_funciones, name='graficador_funciones'),


  path('inyectiva/', views.inyectiva_view, name='inyectiva'),


    path('decreciente/', views.analizar_funcion_view, name='decreciente'),
    path('funcion_creciente/', views.creciente_view, name='funcion_creciente'),
    path('continuidad/', views.calculadora_continuidad, name='continuidad'),
    path('teorias/', views.teorias, name='teorias'),

    path('accounts/login/', views.login_view, name='accounts_login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
]

