from django.shortcuts import render
from .explicita import calcular_funcion_explicita 


def pagprincipal(request):
    return render(request, 'pagprincipal.html')

def temas (request):
    return render(request, 'temas.html')

def tema_funciones (request):
    return render(request, 'tema_funciones.html')



def calculadora_explicita(request):
    result = None
    error = None
    function_input = ""
    operation_select = ""

   
    if request.method == 'POST':
        function_input = request.POST.get('function_input', '').strip()
        operation_select = request.POST.get('operation_select', '').strip()
        variable_input = request.POST.get('variable_input', '').strip()
        limit_point_input = request.POST.get('limit_point_input', '').strip()
        evaluate_values_input = request.POST.get('evaluate_values_input', '').strip()

    
        kwargs_para_funcion = {}
        if operation_select in ['derivar', 'limite', 'resolver']:
            kwargs_para_funcion['variable_derivacion'] = variable_input 
            kwargs_para_funcion['variable_integracion'] = variable_input
            kwargs_para_funcion['variable_limite'] = variable_input
            kwargs_para_funcion['variable_resolver'] = variable_input
        
        if operation_select == 'limite':
            kwargs_para_funcion['punto_limite'] = limit_point_input
        
        if operation_select == 'evaluar':
            kwargs_para_funcion['valores_evaluacion_str'] = evaluate_values_input

        
        result, error = calcular_funcion_explicita(function_input, operation_select, **kwargs_para_funcion)

    
    context = {
        'function_input': function_input,
        'operation_select': operation_select,
        'result': result,
        'error': error,
    }
    return render(request, 'funcion_explicita.html', context)