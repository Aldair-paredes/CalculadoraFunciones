from django.shortcuts import render
from .explicita import calcular_funcion_explicita 
<<<<<<< HEAD
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
=======
import io, base64
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

>>>>>>> Agustin


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
<<<<<<< HEAD



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
=======
#Decreciente Agustin

def analizarfuncionview(request):
    if request.method == 'POST':
        try:
            # Recoger los datos del formulario
            funcion = request.POST.get('funcion')
            intervalo_min = float(request.POST.get('intervalo_min'))
            intervalo_max = float(request.POST.get('intervalo_max'))
            punto_limite = float(request.POST.get('punto_limite'))
            graficar = request.POST.get('graficar') == 's'

            x = sp.symbols('x')
            f = sp.sympify(funcion)

            resultado = f"\nFunción original: f(x) = {f}\n"

            # Derivar
            derivada = sp.diff(f, x)
            resultado += f"Derivada: f'(x) = {derivada}\n"

            # Simplificar
            simplificada = sp.simplify(f)
            resultado += f"Función simplificada: {simplificada}\n"

            # Resolver f(x)=0
            soluciones = sp.solve(f, x)
            resultado += f"Soluciones a f(x)=0: {soluciones if soluciones else 'No hay soluciones reales encontradas.'}\n"

            # Calcular límite
            limite = sp.limit(f, x, punto_limite)
            resultado += f"Límite de f(x) cuando x → {punto_limite}: {limite}\n"

            # Analizar si es decreciente
            puntos = np.linspace(intervalo_min, intervalo_max, 100)
            derivadas_numericas = [float(derivada.subs(x, punto)) for punto in puntos]
            decreciente = all(valor <= 0 for valor in derivadas_numericas)

            if decreciente:
                resultado += "\nConclusión: La función es decreciente en todo el intervalo."
            else:
                resultado += "\nConclusión: La función no es completamente decreciente en el intervalo."

            grafico_url = None

            # Graficar si el usuario lo pidió
            if graficar:
                f_lambd = sp.lambdify(x, f, modules=['numpy'])
                deriv_lambd = sp.lambdify(x, derivada, modules=['numpy'])
                y_f = f_lambd(puntos)
                y_df = deriv_lambd(puntos)

                if np.isscalar(y_f):
                    y_f = np.full_like(puntos, y_f)
                if np.isscalar(y_df):
                    y_df = np.full_like(puntos, y_df)

                plt.figure(figsize=(10,6))
                plt.plot(puntos, y_f, label='f(x)', color='blue')
                plt.plot(puntos, y_df, label="f'(x)", color='red', linestyle='--')
                plt.axhline(0, color='black', linewidth=0.5)
                plt.legend()
                plt.title('Función y su derivada')
                plt.xlabel('x')
                plt.ylabel('Valor')
                plt.grid(True)

                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                grafico_base64 = base64.b64encode(image_png).decode('utf-8')
                grafico_url = f"data:image/png;base64,{grafico_base64}"
                plt.close()

            return render(request, 'Decreciente.html', {
                'resultado': resultado,
                'grafico_url': grafico_url
            })

        except Exception as e:
            return render(request, 'Decreciente.html', {
                'error': f"Error al analizar la función: {str(e)}"
            })

    return render(request, 'Decreciente.html')

#Inyectiva Agustin

from django.shortcuts import render
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings

def funcion_inyectiva(request):
    resultado = {}
    
    if request.method == 'POST':
        expresion = request.POST.get('funcion')
        operacion = request.POST.get('operacion')
        valor_x = request.POST.get('valor_x')

        x = sp.Symbol('x')
        try:
            funcion = sp.sympify(expresion)
        except:
            resultado = {'expresion': expresion, 'operacion': operacion, 'valor': 'Error: función inválida'}
            return render(request, 'inyectiva.html', {'resultado': resultado})

        valor = None

        try:
            if operacion == 'derivar':
                valor = sp.diff(funcion, x)
            elif operacion == 'evaluar':
                valor = funcion.subs(x, float(valor_x))
            elif operacion == 'limite':
                valor = sp.limit(funcion, x, float(valor_x))
            elif operacion == 'simplificar':
                valor = sp.simplify(funcion)
            elif operacion == 'resolver':
                valor = sp.solve(funcion, x)
        except Exception as e:
            valor = f'Error al calcular: {str(e)}'

        resultado = {
            'expresion': expresion,
            'operacion': operacion,
            'valor': valor
        }

    return render(request, 'inyectiva.html', {'resultado': resultado})
>>>>>>> Agustin
