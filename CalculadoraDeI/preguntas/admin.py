from django.contrib import admin
from .models import Pregunta, Opcion

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 3 

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto_pregunta', 'tipo_pregunta', 'respuesta_correcta_vf')
    inlines = [OpcionInline]
    list_filter = ('tipo_pregunta',)
    search_fields = ('texto_pregunta',)

    def get_fieldsets(self, request, obj=None):
        if obj and obj.tipo_pregunta == 'VF':
            return (
                (None, {
                    'fields': ('texto_pregunta', 'tipo_pregunta', 'respuesta_correcta_vf'),
                }),
            )
        else:
            return (
                (None, {
                    'fields': ('texto_pregunta', 'tipo_pregunta'),
                }),
            )
# Register your models here.
