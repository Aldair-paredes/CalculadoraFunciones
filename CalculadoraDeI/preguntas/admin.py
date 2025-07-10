from django.contrib import admin

from .models import Pregunta, Opcion

#Para una mejor visualización de las opciones anidadas en la pregunta
class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 1 
    fields = ['texto_opcion', 'es_correcta'] # Campos a mostrar
   

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto_pregunta', 'tipo_pregunta', 'respuesta_correcta_tf_display')
    list_filter = ('tipo_pregunta',)
    search_fields = ('texto_pregunta',)

    # Función para mostrar la respuesta V/F de forma más amigable en la lista
    def respuesta_correcta_tf_display(self, obj):
        if obj.tipo_pregunta == 'true_false':
            return 'Verdadero' if obj.respuesta_correcta_tf else 'Falso'
        return "N/A"
    respuesta_correcta_tf_display.short_description = "Respuesta V/F"

    fieldsets = (
        (None, {
            'fields': ('texto_pregunta', 'tipo_pregunta'),
        }),
        ('Detalles de la Respuesta (solo para V/F)', {
            'fields': ('respuesta_correcta_tf',),
            'classes': ('collapse',), 
        }),
    )

    #Aqui es donde conectamos las opciones al formulario de la pregunta
    inlines = [OpcionInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if obj.tipo_pregunta == 'true_false' and obj.opciones.exists():
            obj.opciones.all().delete() 
        elif obj.tipo_pregunta == 'multiple_choice' and obj.respuesta_correcta_tf is not None:
            obj.respuesta_correcta_tf = None
            obj.save(update_fields=['respuesta_correcta_tf'])
# Register your models here.
