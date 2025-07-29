from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Perfil
from django.http import HttpRequest
from collections.abc import Iterable
from .funcion.implicita import FuncionImplicita
from .transcendente import _limpiar_y_preparar_funcion_str as transcendente_limpiar_y_preparar_funcion_str, calcular_funcion_transcendente
from .algebraica import (
    calculate_linear_function,
    calculate_quadratic_function,
    calculate_polynomial_function,
    calculate_rational_function,
    calculate_radical_function
)
from sympy import symbols, Eq, sympify, sqrt, simplify, solve

import numpy as np
import matplotlib.pyplot as plt
import io
import urllib.parse
import base64

# Variables globales para SymPy
x, y, z = symbols('x y z')
from .biyectiva import _limpiar_y_preparar_funcion_str as biyectiva_limpiar_y_preparar_funcion_str, calcular_funcion_biyectiva
import io, base64
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


from .funcion.creciente import FuncionCreciente
import matplotlib.pyplot as plt
import base64
import io
import sympy as sp
from .funcion.continuidad import verificar_continuidad_en_punto, graficar_funcion_continuidad

def pagprincipal(request):
    return render(request, 'pagprincipal.html')

def temas (request):
    return render(request, 'temas.html')

def teoria_implicita (request):
    return render(request, 'teoria_implicita')

def tema_funciones (request):
    return render(request, 'tema_funciones.html')

from django.shortcuts import render

from .explicita import _limpiar_y_preparar_funcion_str, calcular_funcion_explicita

from sympy import symbols, sympify, pi, E, Abs, sqrt, exp, log, sin, cos, tan, cot, sec, csc, \
                    asin, acos, atan, acot, asec, acsc, \
                    sinh, cosh, tanh, coth, sech, csch, \
                    asinh, acosh, atanh, acoth, asech, acsch, \
                    Add, Mul, Pow, S, Integer, Float 
try:
    from sympy import log10
except ImportError:
    def log10(x):
        return log(x, 10)

from sympy.parsing.sympy_parser import parse_expr 

ALLOWED_SYMPY_FUNCTIONS = {
    'sin': sin, 'cos': cos, 'tan': tan, 'cot': cot, 'sec': sec, 'csc': csc,
    'asin': asin, 'acos': acos, 'atan': atan, 'acot': acot, 'asec': asec, 'acsc': acsc,
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh, 'coth': coth, 'sech': sech, 'csch': csch,
    'asinh': asinh, 'acosh': acosh, 'atanh': atanh, 'acoth': acoth, 'asech': asech, 'acsch': acsch,
    'log': log, 'log10': log10, 'exp': exp, 'sqrt': sqrt, 'abs': Abs,
}
ALLOWED_SYMPY_CONSTANTS = {
    'pi': pi, 'E': E
}

def _get_safe_local_dict():
    safe_local_dict = {**ALLOWED_SYMPY_FUNCTIONS, **ALLOWED_SYMPY_CONSTANTS}
    
    for sym_name in ['x', 'y', 'z', 't']:
        safe_local_dict[sym_name] = symbols(sym_name)

    safe_local_dict['Add'] = Add
    safe_local_dict['Mul'] = Mul
    safe_local_dict['Pow'] = Pow
    safe_local_dict['Sub'] = type(symbols('a') - symbols('b')) 
    safe_local_dict['Div'] = type(symbols('a') / symbols('b')) 
    safe_local_dict['Integer'] = Integer 
    safe_local_dict['Float'] = Float 
    safe_local_dict['S'] = S 
    return safe_local_dict

def _validate_and_parse_function(function_input, variable_input, safe_local_dict, cleaner_func):
    error = None
    funcion_expr = None

    funcion_para_parsear = cleaner_func(function_input)

    try:
        current_safe_local_dict = safe_local_dict.copy()
        if variable_input:
            vars_in_input = [v.strip() for v in variable_input.split(',') if v.strip()]
            for var_name in vars_in_input:
                current_safe_local_dict[var_name] = symbols(var_name)

        funcion_expr = parse_expr(funcion_para_parsear, local_dict=current_safe_local_dict, global_dict={}, evaluate=False)

        parsed_free_symbols = funcion_expr.free_symbols
        explicitly_allowed_symbols_objects = set(current_safe_local_dict.values())
        
        unexpected_symbols = [
            s for s in parsed_free_symbols 
            if s not in explicitly_allowed_symbols_objects and s not in (pi, E)
        ]

        if unexpected_symbols:
            error = f"La función contiene símbolos no reconocidos o no permitidos: {', '.join(str(s) for s in unexpected_symbols)}. " \
                    f"Revisa tu guía de uso para las variables y funciones soportadas."
            funcion_expr = None 

    except (SyntaxError, TypeError, ValueError, NameError) as e:
        error = f"La función no cumple con las consideraciones de la guía de uso. Detalles: {e}. " \
                f"Asegúrate de usar solo operadores (*, **, +, -, /), funciones y constantes permitidas."
        funcion_expr = None
    except Exception as e:
        error = f"Ocurrió un error inesperado al procesar la función: {e}. Por favor, verifica tu entrada."
        funcion_expr = None
    
    return funcion_expr, error

#explicita

def calculadora_explicita(request):
    result = None
    error = None
    function_input = ""
    operation_select = ""
    variable_input = ""
    limit_point_input = ""
    evaluate_values_input = ""
    
    if request.method == 'POST':
        function_input = request.POST.get('function_input', '').strip()
        operation_select = request.POST.get('operation_select', '').strip()
        variable_input = request.POST.get('variable_input', '').strip()
        limit_point_input = request.POST.get('limit_point_input', '').strip()
        evaluate_values_input = request.POST.get('evaluate_values_input', '').strip()

        if not function_input:
            error = "La función no puede estar vacía."
        elif not operation_select:
            error = "Por favor, selecciona una operación."
        else:
            try:
                funcion_para_parsear = _limpiar_y_preparar_funcion_str(function_input)

                safe_local_dict = {**ALLOWED_SYMPY_FUNCTIONS, **ALLOWED_SYMPY_CONSTANTS}
                
                for sym_name in ['x', 'y', 'z', 't']:
                    safe_local_dict[sym_name] = symbols(sym_name)

                safe_local_dict['Add'] = Add
                safe_local_dict['Mul'] = Mul
                safe_local_dict['Pow'] = Pow
                safe_local_dict['Sub'] = type(symbols('a') - symbols('b'))
                safe_local_dict['Div'] = type(symbols('a') / symbols('b'))
                safe_local_dict['Integer'] = Integer
                safe_local_dict['Float'] = Float
                safe_local_dict['S'] = S

                if variable_input:
                    vars_in_input = [v.strip() for v in variable_input.split(',') if v.strip()]
                    for var_name in vars_in_input:
                        safe_local_dict[var_name] = symbols(var_name)

                funcion_expr = parse_expr(funcion_para_parsear, local_dict=safe_local_dict, global_dict={}, evaluate=False)

                parsed_free_symbols = funcion_expr.free_symbols
                explicitly_allowed_symbols_objects = set(safe_local_dict.values())
                
                unexpected_symbols = [
                    s for s in parsed_free_symbols 
                    if s not in explicitly_allowed_symbols_objects and s not in (pi, E)
                ]

                if unexpected_symbols:
                    error = f"La función contiene símbolos no reconocidos o no permitidos: {', '.join(str(s) for s in unexpected_symbols)}. " \
                            f"Revisa tu guía de uso para las variables y funciones soportadas."
                
                requires_variable = ['derivar', 'integrar', 'limite', 'resolver']
                if operation_select in requires_variable and not variable_input:
                    error = "La variable es requerida para la operación seleccionada."
                elif operation_select in requires_variable and variable_input:
                    var_sym = symbols(variable_input)
                    if operation_select != 'resolver' and var_sym not in funcion_expr.free_symbols:
                        if not any(v in funcion_para_parsear.replace('**', '').replace(' ', '') for v in [str(var_sym)]):
                            error = f"La variable '{variable_input}' no se encuentra en la función. Revisa tu guía de uso."
                
                if operation_select == 'limite' and not limit_point_input:
                    error = "El punto del límite es requerido para la operación de límite."
                
                if operation_select == 'evaluar':
                    if not evaluate_values_input:
                        error = "Los valores para evaluar son requeridos para la operación de evaluación (ej: x=2, y=3)."
                    else:
                        parts = evaluate_values_input.split(',')
                        for part in parts:
                            if '=' not in part or len(part.split('=')) != 2:
                                error = "Formato de valores para evaluar incorrecto. Usa 'variable=valor' separado por comas."
                                break
                            var_name = part.split('=')[0].strip()
                            if not var_name.isalnum():
                                error = "Nombres de variables inválidos en los valores para evaluar. Usa solo letras y números."
                                break
                
                if not error:
                    kwargs_para_funcion = {
                        'variable_derivacion': variable_input,
                        'variable_integracion': variable_input,
                        'variable_limite': limit_point_input,
                        'variable_resolver': variable_input,
                        'punto_limite': limit_point_input,
                        'valores_evaluacion_str': evaluate_values_input
                    }
                    result, error = calcular_funcion_explicita(funcion_expr, operation_select, **kwargs_para_funcion)

            except (SyntaxError, TypeError, ValueError, NameError) as e:
                error = f"La función no cumple con las consideraciones de la guía de uso. Detalles: {e}. " \
                        f"Asegúrate de usar solo operadores (*, **, +, -, /), funciones y constantes permitidas."
            except Exception as e:
                error = f"Ocurrió un error inesperado: {e}. Por favor, verifica tu entrada."

    context = {
        'function_input': function_input,
        'operation_select': operation_select,
        'variable_input': variable_input,
        'limit_point_input': limit_point_input,
        'evaluate_values_input': evaluate_values_input,
        'result': result,
        'error': error,
    }
    return render(request, 'funcion_explicita.html', context)



def funcion_implicita_view(request: HttpRequest):
    expresion_input = request.POST.get('expresion', '').strip()
    operation_select = request.POST.get('operation_select', '').strip()
    
    x_val_input = request.POST.get('x_val', '').strip()
    y_val_input = request.POST.get('y_val', '').strip()
    derivar_var_input = request.POST.get('derivar_var', '').strip()
    derivar_orden_input = request.POST.get('derivar_orden', '').strip()
    limite_var_input = request.POST.get('limite_var', '').strip()
    limite_punto_input = request.POST.get('limite_punto', '').strip()
    limite_dir_input = request.POST.get('limite_dir', '').strip() 
    resolver_var_input = request.POST.get('resolver_var', '').strip()
    resolver_val_input = request.POST.get('resolver_val', '').strip()

    rango_x_min_input = request.POST.get('rango_x_min', '').strip()
    rango_x_max_input = request.POST.get('rango_x_max', '').strip()
    rango_y_min_input = request.POST.get('rango_y_min', '').strip()
    rango_y_max_input = request.POST.get('rango_y_max', '').strip()
    puntos_input = request.POST.get('puntos', '').strip()

    resultado = None 
    error = None 
    grafica_base64 = None

    if request.method == 'POST' and expresion_input and operation_select:
        try:
            f = FuncionImplicita(expresion_input)

            if operation_select == 'evaluar':
                if not x_val_input and not y_val_input:
                    raise ValueError("Para evaluar, se requiere al menos un valor para 'x' o 'y'.")
                res = f.evaluar(x_val_input, y_val_input)
                resultado = {
                    'Expresión Original': expresion_input,
                    'Operación': 'Evaluar',
                    'Valor de x': x_val_input if x_val_input else 'N/A',
                    'Valor de y': y_val_input if y_val_input else 'N/A',
                    'Resultado': res
                }

            elif operation_select == 'derivar':
                if not derivar_var_input:
                    raise ValueError("Se requiere la variable (x o y) para la derivación.")
                res = f.derivada(derivar_var_input, derivar_orden_input)
                resultado = {
                    'Expresión Original': expresion_input,
                    'Operación': 'Derivar',
                    'Respecto a': derivar_var_input,
                    'Orden': derivar_orden_input if derivar_orden_input else '1',
                    'Resultado': res
                }

            elif operation_select == 'limite':
                if not limite_var_input or not limite_punto_input:
                    raise ValueError("Se requieren la variable y el punto para el cálculo del límite.")
                res = f.limite(limite_var_input, limite_punto_input, limite_dir_input)
                resultado = {
                    'Expresión Original': expresion_input,
                    'Operación': 'Límite',
                    'Variable': limite_var_input,
                    'Punto': limite_punto_input,
                    'Dirección': limite_dir_input if limite_dir_input else 'Ambos lados',
                    'Resultado': res
                }

            elif operation_select == 'simplificar':
                res = f.simplificar()
                resultado = {
                    'Expresión Original': expresion_input,
                    'Operación': 'Simplificar',
                    'Resultado': res
                }

            elif operation_select == 'resolver':
                if not resolver_var_input:
                    raise ValueError("Se requiere la variable (x o y) para resolver.")
                res = f.resolver(resolver_var_input, resolver_val_input if resolver_val_input else None)
                
                if isinstance(res, list):
                    resultado = {
                        'Expresión Original': expresion_input,
                        'Operación': 'Resolver',
                        'Variable a Despejar': resolver_var_input,
                        'Soluciones': res 
                    }
                else:
                    resultado = {
                        'Expresión Original': expresion_input,
                        'Operación': 'Resolver',
                        'Variable a Despejar': resolver_var_input,
                        'Solución': res 
                    }
            
            elif operation_select == 'graficar':
                try:
                    rango_x_min = float(rango_x_min_input) if rango_x_min_input else -5
                    rango_x_max = float(rango_x_max_input) if rango_x_max_input else 5
                    rango_y_min = float(rango_y_min_input) if rango_y_min_input else -5
                    rango_y_max = float(rango_y_max_input) if rango_y_max_input else 5
                    puntos = int(puntos_input) if puntos_input else 200

                    if rango_x_min >= rango_x_max or rango_y_min >= rango_y_max:
                        raise ValueError("El valor mínimo del rango debe ser menor que el máximo.")
                    if puntos < 50 or puntos > 1000: # Limita los puntos para evitar sobrecarga
                        raise ValueError("El número de puntos debe estar entre 50 y 1000.")
                        
                    rango_x = (rango_x_min, rango_x_max)
                    rango_y = (rango_y_min, rango_y_max)

                except ValueError as ve:
                    raise ValueError(f"Error en los parámetros de graficación: {ve}")
                except Exception:
                    raise ValueError("Los valores de rango y puntos para graficar deben ser numéricos válidos.")

                img_data = f.graficar(rango_x=rango_x, rango_y=rango_y, puntos=puntos)
                
                if img_data:
                    grafica_base64 = img_data
                    resultado = {
                        'Expresión Original': expresion_input,
                        'Operación': 'Graficar',
                        'Mensaje': 'Gráfica generada exitosamente.'
                    }
                else:
                    error = "No se pudo generar la gráfica."

            else:
                error = "Operación no válida seleccionada."

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Ocurrió un error inesperado al procesar: {type(e).__name__} - {str(e)}"
            import traceback
            traceback.print_exc()

    context = {
        'expresion_input': expresion_input,
        'operation_select': operation_select,
        'x_val_input': x_val_input,
        'y_val_input': y_val_input,
        'derivar_var_input': derivar_var_input,
        'derivar_orden_input': derivar_orden_input,
        'limite_var_input': limite_var_input,
        'limite_punto_input': limite_punto_input,
        'limite_dir_input': limite_dir_input,
        'resolver_var_input': resolver_var_input,
        'resolver_val_input': resolver_val_input,
        'rango_x_min_input': rango_x_min_input,
        'rango_x_max_input': rango_x_max_input,
        'rango_y_min_input': rango_y_min_input,
        'rango_y_max_input': rango_y_max_input,
        'puntos_input': puntos_input,
        'resultado': resultado,
        'error': error,
        'grafica_base64': grafica_base64,
    }
    return render(request, 'funcion_implicita.html', context) 



def calculadora_transcendente(request):
    result = None
    error = None
    function_input = ""
    operation_select = ""
    variable_input = ""
    limit_point_input = ""
    evaluate_values_input = ""
    
    if request.method == 'POST':
        function_input = request.POST.get('function_input', '').strip()
        operation_select = request.POST.get('operation_select', '').strip()
        variable_input = request.POST.get('variable_input', '').strip()
        limit_point_input = request.POST.get('limit_point_input', '').strip()
        evaluate_values_input = request.POST.get('evaluate_values_input', '').strip()

        if not function_input:
            error = "La función no puede estar vacía."
        elif not operation_select:
            error = "Por favor, selecciona una operación."
        else:
            safe_local_dict = _get_safe_local_dict()
            funcion_expr, error = _validate_and_parse_function(function_input, variable_input, safe_local_dict, transcendente_limpiar_y_preparar_funcion_str)

            if not error and funcion_expr: 
                requires_variable = ['derivar', 'integrar', 'limite', 'resolver']
                if operation_select in requires_variable and not variable_input:
                    error = "La variable es requerida para la operación seleccionada."
                elif operation_select in requires_variable and variable_input:
                    var_sym = symbols(variable_input)
                    if operation_select != 'resolver' and var_sym not in funcion_expr.free_symbols:
                        if not any(v in function_input.replace('**', '').replace(' ', '') for v in [str(var_sym)]):
                            error = f"La variable '{variable_input}' no se encuentra en la función. Revisa tu guía de uso."
                
                if operation_select == 'limite' and not limit_point_input:
                    error = "El punto del límite es requerido para la operación de límite."
                
                if operation_select == 'evaluar':
                    if not evaluate_values_input:
                        error = "Los valores para evaluar son requeridos para la operación de evaluación (ej: x=2, y=3)."
                    else:
                        parts = evaluate_values_input.split(',')
                        for part in parts:
                            if '=' not in part or len(part.split('=')) != 2:
                                error = "Formato de valores para evaluar incorrecto. Usa 'variable=valor' separado por comas."
                                break
                            var_name = part.split('=')[0].strip()
                            if not var_name.isalnum():
                                error = "Nombres de variables inválidos en los valores para evaluar. Usa solo letras y números."
                                break
                
                if not error:
                    kwargs_para_funcion = {
                        'variable_derivacion': variable_input,
                        'variable_integracion': variable_input,
                        'variable_limite': limit_point_input,
                        'variable_resolver': variable_input,
                        'punto_limite': limit_point_input,
                        'valores_evaluacion_str': evaluate_values_input
                    }
                    result, error = calcular_funcion_transcendente(funcion_expr, operation_select, **kwargs_para_funcion)

    context = {
        'function_input': function_input,
        'operation_select': operation_select,
        'variable_input': variable_input,
        'limit_point_input': limit_point_input,
        'evaluate_values_input': evaluate_values_input,
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
    result = None
    error = None
    function_input = ""
    operation_select = ""
    variable_input = ""
    limit_point_input = ""
    evaluate_values_input = ""
    
    if request.method == 'POST':
        function_input = request.POST.get('function_input', '').strip()
        operation_select = request.POST.get('operation_select', '').strip()
        variable_input = request.POST.get('variable_input', '').strip()
        limit_point_input = request.POST.get('limit_point_input', '').strip()
        evaluate_values_input = request.POST.get('evaluate_values_input', '').strip()

        if not function_input:
            error = "La función no puede estar vacía."
        elif not operation_select:
            error = "Por favor, selecciona una operación."
        else:
            safe_local_dict = _get_safe_local_dict()
            funcion_expr, error = _validate_and_parse_function(function_input, variable_input, safe_local_dict, biyectiva_limpiar_y_preparar_funcion_str)

            if not error and funcion_expr: 
                requires_variable = ['derivar', 'integrar', 'limite', 'resolver']
                if operation_select in requires_variable and not variable_input:
                    error = "La variable es requerida para la operación seleccionada."
                elif operation_select in requires_variable and variable_input:
                    var_sym = symbols(variable_input)
                    if operation_select != 'resolver' and var_sym not in funcion_expr.free_symbols:
                        if not any(v in function_input.replace('**', '').replace(' ', '') for v in [str(var_sym)]):
                            error = f"La variable '{variable_input}' no se encuentra en la función. Revisa tu guía de uso."
                
                if operation_select == 'limite' and not limit_point_input:
                    error = "El punto del límite es requerido para la operación de límite."
                
                if operation_select == 'evaluar':
                    if not evaluate_values_input:
                        error = "Los valores para evaluar son requeridos para la operación de evaluación (ej: x=2, y=3)."
                    else:
                        parts = evaluate_values_input.split(',')
                        for part in parts:
                            if '=' not in part or len(part.split('=')) != 2:
                                error = "Formato de valores para evaluar incorrecto. Usa 'variable=valor' separado por comas."
                                break
                            var_name = part.split('=')[0].strip()
                            if not var_name.isalnum():
                                error = "Nombres de variables inválidos en los valores para evaluar. Usa solo letras y números."
                                break
                
                if not error:
                    kwargs_para_funcion = {
                        'variable_derivacion': variable_input,
                        'variable_integracion': variable_input,
                        'variable_limite': limit_point_input,
                        'variable_resolver': variable_input,
                        'punto_limite': limit_point_input,
                        'valores_evaluacion_str': evaluate_values_input
                    }
                    result, error = calcular_funcion_biyectiva(funcion_expr, operation_select, **kwargs_para_funcion)

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


def creciente_view(request):
    expresion_input = None
    operation_select = None
    x_eval_input = None
    derivar_orden_input = None
    rango_x_min_input = None
    rango_x_max_input = None
    puntos_input = None

    resultado = None
    error = None
    grafica_base64 = None

    if request.method == 'POST':
        expresion_input = request.POST.get('expresion')
        operation_select = request.POST.get('operation_select')

        try:
            f = FuncionCreciente(expresion_input)

            if operation_select == 'evaluar':
                x_eval_str = request.POST.get('x_eval')
                if not x_eval_str:
                    raise ValueError("El valor de 'x' es requerido para evaluar.")
                x_eval_input = float(x_eval_str)
                eval_result = f.evaluar(x_eval_input)
                resultado = {
                    "Función": f.expresion_str,
                    "Variable de Evaluación": f.x,
                    "Valor de x": x_eval_input,
                    "Resultado de Evaluación": str(eval_result)
                }

            elif operation_select == 'derivar':
                derivar_orden_str = request.POST.get('derivar_orden', '1')
                derivar_orden_input = int(derivar_orden_str)
                derivada_obj = f.derivada(derivar_orden_input)
                if derivada_obj:
                    resultado = {
                        "Función Original": f.expresion_str,
                        f"Derivada (Orden {derivar_orden_input})": str(derivada_obj.expresion)
                    }
                else:
                    raise Exception("No se pudo calcular la derivada.")

            elif operation_select == 'encontrar_crecimiento':
                intervalos = f.encontrar_intervalos_crecientes()
                if intervalos is not None:
                    formatted_intervals = []
                    for a, b in intervalos:
                        start = "-\u221E" if a == -sp.oo else str(a)
                        end = "\u221E" if b == sp.oo else str(b)
                        formatted_intervals.append(f"({start}, {end})")

                    resultado = {
                        "Función": f.expresion_str,
                        "Intervalos Crecientes": ", ".join(formatted_intervals) if formatted_intervals else "No se encontraron intervalos crecientes."
                    }
                else:
                    raise Exception("No se pudieron encontrar los intervalos de crecimiento.")

            elif operation_select == 'graficar':
                rango_x_min_str = request.POST.get('rango_x_min', '-5')
                rango_x_max_str = request.POST.get('rango_x_max', '5')
                puntos_str = request.POST.get('puntos', '500')

                rango_x_min_input = float(rango_x_min_str)
                rango_x_max_input = float(rango_x_max_str)
                puntos_input = int(puntos_str)

                x_vals, y_vals, dy_vals, func_str, deriv_str = f.graficar(
                    (rango_x_min_input, rango_x_max_input), puntos_input
                )

                if x_vals is not None:
                    buffer = io.BytesIO()
                    
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
                    
                    ax1.plot(x_vals, y_vals, label=f'f(x) = {func_str}')
                    ax1.set_title('Función')
                    ax1.set_xlabel('x')
                    ax1.set_ylabel('f(x)')
                    ax1.grid(True)
                    ax1.legend()
                    
                    ax2.plot(x_vals, dy_vals, label=f"f'(x) = {deriv_str}", color='orange')
                    ax2.axhline(0, color='red', linestyle='--', linewidth=0.5)
                    ax2.set_title('Derivada')
                    ax2.set_xlabel('x')
                    ax2.set_ylabel("f'(x)")
                    ax2.grid(True)
                    ax2.legend()
                    
                    plt.tight_layout()
                    
                    plt.savefig(buffer, format='png')
                    plt.close(fig)
                    
                    buffer.seek(0)
                    grafica_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                else:
                    raise Exception("No se pudieron generar los datos para graficar.")

            else:
                error = "Operación no reconocida."

        except ValueError as e:
            error = f"Error de entrada: {e}"
        except Exception as e:
            error = f"Error en el cálculo: {e}"
            
    if operation_select:
       operation_display = operation_select.replace("_", " ").title()
    else:
        operation_display = None

    context = {
        'expresion_input': expresion_input,
        'operation_select': operation_select,
        'operation_display': operation_display,
        'x_eval_input': x_eval_input,
        'derivar_orden_input': derivar_orden_input,
        'rango_x_min_input': rango_x_min_input,
        'rango_x_max_input': rango_x_max_input,
        'puntos_input': puntos_input,
        'resultado': resultado,
        'error': error,
        'grafica_base64': grafica_base64,
    }
    return render(request, 'funcion_creciente.html', context)


def calculadora_continuidad(request):
    function_input = ""
    punto_continuidad_input = ""
    rango_x_min_input = ""
    rango_x_max_input = ""
    
    resultado_continuidad = None
    grafica_base64 = None
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
#Decreciente Agustin
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import re
from django.shortcuts import render

def preparar_expresion(expr_str):
    expr_str = expr_str.replace('^', '**')
    expr_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr_str)
    expr_str = re.sub(r'(\))([a-zA-Z(])', r'\1*\2', expr_str)
    return expr_str

def analizar_funcion_view(request):
    resultado = ''
    error = None
    grafico_url = None

    if request.method == 'POST':
        function_input = request.POST.get('function_input', '').strip()
        interval_min_input = request.POST.get('interval_min_input', '').strip()
        interval_max_input = request.POST.get('interval_max_input', '').strip()
        limit_point_input = request.POST.get('limit_point_input', '').strip()
        graficar_input = request.POST.get('graficar_input', 'n')

        # Validar entradas
        if not function_input or not interval_min_input or not interval_max_input or not limit_point_input:
            error = "Por favor, completa todos los campos."
        else:
            try:
                x = sp.symbols('x')
                funcion_corregida = preparar_expresion(function_input)
                f = sp.sympify(funcion_corregida)

                a = float(interval_min_input)
                b = float(interval_max_input)
                if a >= b:
                    error = "El límite inferior debe ser menor que el superior."
                else:
                    derivada = sp.diff(f, x)

                    resultado += f"Función: f(x) = {f}\n"
                    resultado += f"Derivada: f'(x) = {derivada}\n"

                    # Soluciones
                    soluciones = sp.solve(f, x)
                    if soluciones:
                        resultado += f"Soluciones f(x) = 0: {soluciones}\n"
                    else:
                        resultado += "No se encontraron soluciones reales para f(x) = 0.\n"

                    # Límite
                    try:
                        punto_lim = float(limit_point_input)
                        lim = sp.limit(f, x, punto_lim)
                        resultado += f"Límite cuando x→{punto_lim}: {lim}\n"
                    except Exception as e:
                        resultado += "No se pudo calcular el límite.\n"

                    # Análisis decreciente
                    puntos = np.linspace(a, b, 300)

                    f_lamb = sp.lambdify(x, f, 'numpy')
                    df_lamb = sp.lambdify(x, derivada, 'numpy')

                    y_f = f_lamb(puntos)
                    y_df = df_lamb(puntos)

                    # Aquí corregimos el error de dimensiones para y_f
                    if np.isscalar(y_f):
                        y_f = np.full_like(puntos, y_f, dtype=np.float64)
                    else:
                        y_f = np.array(y_f, dtype=np.float64)

                    # Igual para y_df
                    if np.isscalar(y_df):
                        y_df = np.full_like(puntos, y_df, dtype=np.float64)
                    else:
                        y_df = np.array(y_df, dtype=np.float64)

                    # Limpiar infinitos
                    y_f[np.isinf(y_f)] = np.nan
                    y_df[np.isinf(y_df)] = np.nan

                    # Comprobar si derivada <= 0 en todo intervalo (decreciente)
                    y_df_clean = np.nan_to_num(y_df, nan=0.0, posinf=1e10, neginf=-1e10)
                    if np.all(y_df_clean <= 1e-9):
                        resultado += "La función es decreciente en todo el intervalo.\n"
                    else:
                        resultado += "La función NO es completamente decreciente en el intervalo.\n"

                    # Generar gráfica si se pidió
                    if graficar_input == 's':
                        plt.figure(figsize=(10, 6))
                        plt.plot(puntos, y_f, label=f'f(x) = {sp.latex(f)}', color='blue')
                        plt.plot(puntos, y_df, label=f"f'(x) = {sp.latex(derivada)}", color='red', linestyle='--')
                        plt.axhline(0, color='black', linewidth=0.5)
                        plt.xlabel('x')
                        plt.ylabel('y')
                        plt.title('Función y su Derivada')
                        plt.legend()
                        plt.grid(True)
                        plt.tight_layout()

                        buf = io.BytesIO()
                        plt.savefig(buf, format='png')
                        plt.close()
                        buf.seek(0)
                        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
                        grafico_url = f"data:image/png;base64,{image_base64}"

            except Exception as e:
                error = f"Error al procesar la función: {e}"

    else:
        function_input = ''
        interval_min_input = ''
        interval_max_input = ''
        limit_point_input = ''
        graficar_input = 'n'

    context = {
        'resultado': resultado,
        'error': error,
        'grafico_url': grafico_url,
        'function_input': function_input,
        'interval_min_input': interval_min_input,
        'interval_max_input': interval_max_input,
        'limit_point_input': limit_point_input,
        'graficar_input': graficar_input,
    }

    return render(request, 'decreciente.html', context)


#Inyectiva Agustin
from django.shortcuts import render
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def inyectiva_view(request):
    if request.method == "POST":
        expresion = request.POST.get("expresion")
        punto_input = request.POST.get("punto")

        x = sp.Symbol('x')

        try:
            funcion = sp.sympify(expresion)
        except Exception:
            return render(request, "inyectiva.html", {"error": "Error al interpretar la función."})

        try:
            punto = float(punto_input)
        except Exception:
            return render(request, "inyectiva.html", {"error": "El valor de x debe ser un número válido."})

        derivada = sp.diff(funcion, x)
        evaluada = funcion.subs(x, punto)
        simplificada = sp.simplify(funcion)

        # Límite
        try:
            limite = sp.limit(funcion, x, punto)
        except Exception:
            limite = "No se pudo calcular"

        # Soluciones
        try:
            soluciones = sp.solve(funcion, x)
        except Exception:
            soluciones = "No se pudo calcular"

        # Inyectividad
        try:
            derivada_simp = sp.simplify(derivada)
            signo_deriv = sp.solve(derivada_simp > 0)
            inyectiva = bool(signo_deriv)
        except Exception:
            inyectiva = False

        # Gráfica
        try:
            f_lambd = sp.lambdify(x, funcion, modules=['numpy'])
            x_vals = np.linspace(punto - 10, punto + 10, 400)
            y_vals = f_lambd(x_vals)

            if np.any(np.isnan(y_vals)) or np.any(np.isinf(y_vals)):
                raise ValueError("Valores inválidos")

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label=f'f(x) = {funcion}', color='blue')
            ax.axhline(0, color='gray', linestyle='--')
            ax.axvline(0, color='gray', linestyle='--')
            ax.scatter(punto, float(evaluada), color='red', label=f'f({punto}) = {evaluada}')
            ax.set_title("Gráfica de la función")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True)
            ax.legend()

            buffer = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            grafica_base64 = base64.b64encode(image_png).decode('utf-8')
            plt.close()
        except Exception:
            grafica_base64 = None

        contexto = {
            "funcion": funcion,
            "derivada": derivada,
            "evaluada": evaluada,
            "punto": punto,
            "limite": limite,
            "simplificada": simplificada,
            "soluciones": soluciones,
            "inyectiva": inyectiva,
            "grafica": grafica_base64,
        }

        return render(request, "inyectiva.html", contexto)

    return render(request, "inyectiva.html")

#SEPARACION


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistroForm, LoginForm
from .models import Perfil

# Página principal
def pagprincipal(request):
    contexto = {}
    contexto['usuario'] = "Invitado"
    contexto['usuario'] = "No autenticado"
    if request.user.is_authenticated:
        Perfil_instancia, created = Perfil.objects.get_or_create(user=request.user)
        if created and not Perfil_instancia.rol:
            Perfil_instancia.rol = "Estudiante"
            Perfil_instancia.save()
        contexto['usuario'] = request.user.username
        contexto['rol'] = Perfil_instancia.rol

    return render(request, 'pagprincipal.html', contexto)

# Vista de registro
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            rol = form.cleaned_data['rol']
            Perfil.objects.create(user=usuario, rol=rol)
            login(request, usuario)
            return redirect('pagprincipal')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('pagprincipal')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Vista de cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('pagprincipal')

from django.shortcuts import render

def teorias(request):
    return render(request, 'teorias.html')  # Asegúrate que el archivo esté en la carpeta templates/

# En tu archivo views.py

def calculadora_view(request):
    if request.method == 'POST':
        operation = request.POST.get('operation_select')
        
        if operation == 'derivar':
            # Tu lógica para derivar...
            pass
        elif operation == 'limite':
            # Tu lógica para límites...
            pass
        # ... otras operaciones
        elif operation == 'decreciente':
            # AQUÍ va la lógica para analizar la función decreciente
            function_input = request.POST.get('function_input')
            interval_min = request.POST.get('interval_min_input')
            interval_max = request.POST.get('interval_max_input')
            point_to_check = request.POST.get('point_to_check_input') # Renombré el campo para mayor claridad
            graficar = request.POST.get('graficar_input')
            
            # ...Llama a tu función de análisis, genera el texto de resultado y la URL del gráfico...
            
            context = {
                'result': 'El texto con el análisis...',
                'grafico_url': '/static/graphs/mi_grafico.png', # La URL de la imagen generada
                # ...otros datos para rellenar el formulario
            }
            return render(request, 'tu_template.html', context)

    return render(request, 'tu_template.html')
def graficador_funciones(request):
    graph_url = None
    error = None
    function_expression = ""
    input_data = {
        'function_type': '',
        'a_linear': '', 'b_linear': '',
        'a_quadratic': '', 'b_quadratic': '', 'c_quadratic': '',
        'x_min': '-10', 'x_max': '10' # Valores por defecto
    }

    if request.method == 'POST':
        function_type = request.POST.get('function_type')
        x_min_str = request.POST.get('x_min', '-10')
        x_max_str = request.POST.get('x_max', '10')

        input_data['function_type'] = function_type
        input_data['x_min'] = x_min_str
        input_data['x_max'] = x_max_str

        try:
            x_min = float(x_min_str)
            x_max = float(x_max_str)
            if x_min >= x_max:
                raise ValueError("El valor mínimo de X debe ser menor que el valor máximo.")
        except ValueError as e:
            error = f"Error en los límites de X: {e}"
            return render(request, 'graficador.html', {'error': error, 'input_data': input_data})

        func = None
        
        if function_type == 'linear':
            a_str = request.POST.get('a_linear')
            b_str = request.POST.get('b_linear')
            input_data['a_linear'] = a_str
            input_data['b_linear'] = b_str

            try:
                a = float(a_str)
                b = float(b_str)
                func = lambda x: a * x + b
                function_expression = f"f(x) = {a}x + {b}"
            except (ValueError, TypeError):
                error = "Entrada inválida para función lineal. Asegúrate de ingresar números válidos para 'a' y 'b'."

        elif function_type == 'quadratic':
            a_str = request.POST.get('a_quadratic')
            b_str = request.POST.get('b_quadratic')
            c_str = request.POST.get('c_quadratic')
            input_data['a_quadratic'] = a_str
            input_data['b_quadratic'] = b_str
            input_data['c_quadratic'] = c_str

            try:
                a = float(a_str)
                b = float(b_str)
                c = float(c_str)
                func = lambda x: a * x**2 + b * x + c
                function_expression = f"f(x) = {a}x² + {b}x + {c}"
            except (ValueError, TypeError):
                error = "Entrada inválida para función cuadrática. Asegúrate de ingresar números válidos para 'a', 'b' y 'c'."
        else:
            error = "Tipo de función no válido."

        if func and not error:
            try:
                x_valores = np.linspace(x_min, x_max, 400)
                y_valores = func(x_valores)

                # --- Generar la gráfica con Matplotlib ---
                plt.figure(figsize=(10, 6))
                plt.plot(x_valores, y_valores, label=function_expression, color='#007bff') # Usamos el color de Bootstrap primary

                # Añadir ejes en el origen si están dentro del rango
                if x_min <= 0 <= x_max:
                    plt.axvline(0, color='grey', linestyle='--', linewidth=0.7)
                if min(y_valores) <= 0 <= max(y_valores):
                    plt.axhline(0, color='grey', linestyle='--', linewidth=0.7)

                plt.title(f'Gráfica de la Función: {function_expression}', fontsize=16)
                plt.xlabel('Dominio (x)', fontsize=12)
                plt.ylabel('Rango / Imagen (y)', fontsize=12)
                plt.grid(True, linestyle=':', alpha=0.7)
                plt.legend(fontsize=12)
                plt.tight_layout()

                # Guardar la gráfica en un buffer de memoria
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                plt.close() # Cierra la figura para liberar memoria

                # Codificar la imagen en base64 para incrustarla en HTML
                image_png = buffer.getvalue()
                graph_url = urllib.parse.quote(base64.b64encode(image_png).decode())

            except Exception as e:
                error = f"Ocurrió un error al generar la gráfica: {e}"
    
    return render(request, 'graficador.html', {
        'graph_url': f"data:image/png;base64,{graph_url}" if graph_url else None,
        'error': error,
        'input_data': input_data,
        'function_type': input_data['function_type'], # Pasamos function_type para que el select se mantenga seleccionado
        'function_expression': function_expression, # Para mostrar la expresión de la función en el resultado
    })


