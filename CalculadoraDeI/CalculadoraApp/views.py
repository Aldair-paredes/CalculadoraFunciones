from django.shortcuts import render
from .explicita import calcular_funcion_explicita 
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

def calculadora_algebraica(request):
    result = None
    error = None
    function_type = request.POST.get('function_type', '')
    input_data = {}
    
    if request.method == 'POST':
        try:
            function_type = request.POST.get('function_type')
            input_data = {
                'a': request.POST.get('a', ''),
                'b': request.POST.get('b', ''),
                'c': request.POST.get('c', ''),
                'm': request.POST.get('m', ''),
                'poly': request.POST.get('poly', ''),
                'num': request.POST.get('num', ''),
                'den': request.POST.get('den', ''),
                'g_x': request.POST.get('g_x', ''),
                'val_x': request.POST.get('val_x', ''),
                'solve_val': request.POST.get('solve_val', '')
            }
            
            if function_type == 'linear':
                result = handle_linear_function(input_data)
            elif function_type == 'quadratic':
                result = handle_quadratic_function(input_data)
            elif function_type == 'polynomial':
                result = handle_polynomial_function(input_data)
            elif function_type == 'rational':
                result = handle_rational_function(input_data)
            elif function_type == 'radical':
                result = handle_radical_function(input_data)
                
        except Exception as e:
            error = str(e)
    
    context = {
        'result': result,
        'error': error,
        'function_type': function_type,
        'input_data': input_data
    }
    return render(request, 'algebraica.html', context)

# Las demás funciones auxiliares (handle_linear_function, etc.) permanecen igual
def handle_linear_function(data):
    m = sympify(data['m']) if data['m'] else 0
    b = sympify(data['b']) if data['b'] else 0
    func_expr = m * x + b
    
    result = {
        'function': f"f(x) = {func_expr}",
        'evaluation': None,
        'solution': None
    }
    
    if data['val_x']:
        val_x = sympify(data['val_x'])
        result['evaluation'] = f"f({val_x}) = {func_expr.subs(x, val_x)}"
    
    if data['solve_val']:
        solve_val = sympify(data['solve_val'])
        solution = solve(Eq(func_expr, solve_val), x)
        result['solution'] = f"Para f(x) = {solve_val}, x = {solution}"
    
    return result

def handle_quadratic_function(data):
    a = sympify(data['a']) if data['a'] else 0
    b = sympify(data['b']) if data['b'] else 0
    c = sympify(data['c']) if data['c'] else 0
    func_expr = a * x**2 + b * x + c
    
    result = {
        'function': f"f(x) = {func_expr}",
        'evaluation': None,
        'roots': solve(Eq(func_expr, 0), x),
        'vertex': f"({-b/(2*a)}, {c - b**2/(4*a)})"
    }
    
    if data['val_x']:
        val_x = sympify(data['val_x'])
        result['evaluation'] = f"f({val_x}) = {func_expr.subs(x, val_x)}"
    
    return result

def handle_polynomial_function(data):
    poly_expr = sympify(data['poly']) if data['poly'] else 0
    
    result = {
        'function': f"f(x) = {poly_expr}",
        'evaluation': None,
        'roots': solve(Eq(poly_expr, 0), x),
        'factored': poly_expr.factor()
    }
    
    if data['val_x']:
        val_x = sympify(data['val_x'])
        result['evaluation'] = f"f({val_x}) = {poly_expr.subs(x, val_x)}"
    
    return result

def handle_rational_function(data):
    num = sympify(data['num']) if data['num'] else 0
    den = sympify(data['den']) if data['den'] else 1
    func_expr = num / den
    
    result = {
        'function': f"f(x) = {func_expr}",
        'evaluation': None,
        'simplified': simplify(func_expr),
        'roots': solve(Eq(num, 0), x) if num != 0 else [],
        'asymptotes': solve(Eq(den, 0), x) if den != 1 else []
    }
    
    if data['val_x']:
        val_x = sympify(data['val_x'])
        if den.subs(x, val_x) != 0:
            result['evaluation'] = f"f({val_x}) = {func_expr.subs(x, val_x)}"
        else:
            result['evaluation'] = f"Indefinido en x = {val_x} (denominador cero)"
    
    return result

def handle_radical_function(data):
    g_x = sympify(data['g_x']) if data['g_x'] else 0
    func_expr = sqrt(g_x)
    
    result = {
        'function': f"f(x) = sqrt({g_x})",
        'evaluation': None,
        'domain': f"x ≥ {solve(Eq(g_x, 0), x)[0]}" if g_x.is_polynomial() else "Complejo"
    }
    
    if data['val_x']:
        val_x = sympify(data['val_x'])
        arg = g_x.subs(x, val_x)
        if arg.is_real and arg >= 0:
            result['evaluation'] = f"f({val_x}) = {func_expr.subs(x, val_x)}"
        else:
            result['evaluation'] = f"f({val_x}) = {func_expr.subs(x, val_x)} (complejo)"
    
    return result

def calculadora_biyectiva(request):

    function_input = ""
    operation_select = ""
    variable_input = ""
    limit_point_input = ""
    evaluate_values_input = ""
    result = None
    error = None

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
        

        result, error = calcular_funcion_biyectiva(function_input, operation_select, **kwargs_para_funcion)
    
    context = {
        'function_input': function_input,
        'operation_select': operation_select,
        'variable_input': variable_input, 
        'limit_point_input': limit_point_input, 
        'evaluate_values_input': evaluate_values_input, 
        'result': result, 
        'error': error,
    }
    return render(request, 'biyectiva.html', context)
