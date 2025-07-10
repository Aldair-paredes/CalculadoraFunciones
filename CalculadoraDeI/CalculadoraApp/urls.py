from django.urls import path
from . import views
 

urlpatterns = [
    



path('', views.pagprincipal, name='pagprincipal'),
    path('calculadora_explicita/', views.calculadora_explicita, name='calculadora_explicita'),
    path('decreciente/', views.analizarfuncionview, name='decreciente'),
    path('temas/', views.temas, name='temas'),
    path('tema_funciones/', views.tema_funciones, name='tema_funciones'),
    path('inyectiva/', views.funcion_inyectiva, name='inyectiva'),



 



]