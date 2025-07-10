from django.contrib import admin
from django.urls import path
from CalculadoraApp import views 


from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CalculadoraApp.urls')),


]
