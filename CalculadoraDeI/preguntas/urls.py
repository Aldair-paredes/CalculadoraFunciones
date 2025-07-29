from django.urls import path
from . import views

app_name = 'preguntas' 

urlpatterns = [
    path('', views.quiz_view, name='quiz_view'),
]