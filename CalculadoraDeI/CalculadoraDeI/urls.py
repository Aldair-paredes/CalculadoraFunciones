from django.contrib import admin
from django.urls import path
from CalculadoraApp import views

urlpatterns = [
    path('admin/', admin.site.urls),



path('', views.calculadora_explicita, name='explicita'),




]
