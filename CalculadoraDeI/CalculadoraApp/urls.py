from django.urls import path
from CalculadoraApp import views

urlpatterns = [
    path('', views.pagprincipal, name='pagprincipal'),
    path('calculadora_explicita/', views.calculadora_explicita, name='calculadora_explicita'),
    path('funcion_implicita/', views.funcion_implicita_view, name='funcion_implicita'),
    path('temas/', views.temas, name='temas'),
    path('tema_funciones/', views.tema_funciones, name='tema_funciones'),
    path('calculadora-transcendente/', views.calculadora_transcendente, name='calculadora_transcendente'),
    path('calculadora-biyectiva/', views.calculadora_biyectiva, name='calculadora_biyectiva'),
    path('calculadora-algebraica/', views.calculadora_algebraica, name='calculadora_algebraica'),
    path('decreciente/', views.analizarfuncionview, name='decreciente'),
    path('inyectiva/', views.funcion_inyectiva, name='inyectiva'),
    path('teorias/', views.teorias, name='teorias'),
    path('funcion_creciente',views.creciente_view, name='funcion_creciente'),
    path('continuidad/', views.calculadora_continuidad, name='continuidad'),
        path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
]
