from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagprincipal, name='pagprincipal'),
    path('calculadora_explicita/', views.calculadora_explicita, name='calculadora_explicita'),
    path('funcion_implicita/', views.funcion_implicita_view, name='funcion_implicita'),
    path('temas/', views.temas, name='temas'),
    path('tema_funciones/', views.tema_funciones, name='tema_funciones'),
]
