from django.shortcuts import render
from .explicita import calcular_funcion_explicita 
from .funcion.implicita import FuncionImplicita
import sympy as sp
from collections.abc import Iterable
from .transcendente import calcular_funcion_transcendente 
from .algebraica import (
    calculate_linear_function,
    calculate_quadratic_function,
    calculate_polynomial_function,
    calculate_rational_function,
    calculate_radical_function
)
from sympy import symbols, Eq, sympify, sqrt, simplify, solve

# Variables globales para SymPy
x, y, z = symbols('x y z')
from .biyectiva import calcular_funcion_biyectiva


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



def funcion_implicita_view(request):
    resultado = {}
    
    if request.method == 'POST':
        expresion = request.POST.get('expresion', '')
        x_val = request.POST.get('x_val')
        y_val = request.POST.get('y_val')
        derivar_var = request.POST.get('derivar_var')
        derivar_orden = request.POST.get('derivar_orden')
        limite_var = request.POST.get('limite_var')
        limite_punto = request.POST.get('limite_punto')
        limite_dir = request.POST.get('limite_dir', '+')
        resolver_var = request.POST.get('resolver_var')
        resolver_val = request.POST.get('resolver_val')

        try:
            f = FuncionImplicita(expresion)

            if x_val and y_val:
                resultado['evaluacion'] = f.evaluar(float(x_val), float(y_val))

            if derivar_var:
                orden = int(derivar_orden) if derivar_orden else 1
                derivada = f.derivada(derivar_var, orden)
                resultado['derivada'] = str(derivada.expresion)

            if limite_var and limite_punto:
                resultado['limite'] = f.limite(limite_var, float(limite_punto), limite_dir)

            resultado['simplificada'] = str(f.simplificar().expresion)

            if resolver_var:
                sustituto = float(resolver_val) if resolver_val else None
                resultado['resolver'] = f.resolver(resolver_var, sustituto)

        except Exception as e:
            resultado['error'] = f"Error procesando la expresión: {str(e)}"
    
    resultado_procesado = {}
    for clave, valor in resultado.items():
        if isinstance(valor, Iterable) and not isinstance(valor, (str, bytes)):
            resultado_procesado[clave] = list(valor)
        else:
            resultado_procesado[clave] = valor

    return render(request, 'funcion_implicita.html', {'resultado': resultado_procesado})



def calculadora_transcendente(request):
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

        result, error = calcular_funcion_transcendente(function_input, operation_select, **kwargs_para_funcion)
    
    context = {
        'function_input': function_input,
        'operation_select': operation_select,
        'result': result,
        'error': error,
    }
    return render(request, 'transcendente.html', context)
