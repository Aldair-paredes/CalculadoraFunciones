from django.shortcuts import render
from django.http import HttpRequest
from collections.abc import Iterable
from .explicita import calcular_funcion_explicita 
from .funcion.implicita import FuncionImplicita
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




    return render(request, 'funcion_implicita.html', context)



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
from django.shortcuts import render
from django.conf import settings
import os
import uuid

def decreciente(request):
    if request.method == 'POST':
        try:
            funcion_str = request.POST.get('funcion')
            intervalo_min = float(request.POST.get('intervalo_min'))
            intervalo_max = float(request.POST.get('intervalo_max'))
            punto_limite = float(request.POST.get('punto_limite'))
            graficar = request.POST.get('graficar') == 's'

            x = sp.symbols('x')
            f = sp.sympify(funcion_str)
            derivada = sp.diff(f, x)

            limite = sp.limit(f, x, punto_limite)

            puntos = np.linspace(intervalo_min, intervalo_max, 100)
            derivadas_numericas = [float(derivada.subs(x, punto)) for punto in puntos]
            es_decreciente = all(valor <= 0 for valor in derivadas_numericas)

            resultado = (
                f"Límite de f(x) cuando x → {punto_limite}: {limite}\n"
                f"Derivada: f'(x) = {derivada}\n"
                f"Conclusión: {'La función es decreciente en todo el intervalo.' if es_decreciente else 'La función no es completamente decreciente en el intervalo.'}"
            )

            grafico_url = None
            if graficar:
                f_lambd = sp.lambdify(x, f, modules=['numpy'])
                deriv_lambd = sp.lambdify(x, derivada, modules=['numpy'])

                y_f = f_lambd(puntos)
                y_df = deriv_lambd(puntos)

                if np.isscalar(y_f):
                    y_f = np.full_like(puntos, y_f, dtype=float)
                else:
                    y_f = np.array(y_f, dtype=float)

                if np.isscalar(y_df):
                    y_df = np.full_like(puntos, y_df, dtype=float)
                else:
                    y_df = np.array(y_df, dtype=float)

                plt.figure(figsize=(10, 6))
                plt.plot(puntos, y_f, label='f(x)', color='blue')
                plt.plot(puntos, y_df, label="f'(x)", color='red', linestyle='--')
                plt.axhline(0, color='black', linewidth=0.5)
                plt.title('Función y su derivada')
                plt.xlabel('x')
                plt.ylabel('Valor')
                plt.legend()
                plt.grid(True)

                filename = f"grafico_{uuid.uuid4().hex}.png"
                filepath = os.path.join(settings.MEDIA_ROOT, filename)
                plt.savefig(filepath)
                plt.close()

                grafico_url = settings.MEDIA_URL + filename

            return render(request, 'Decreciente.html', {
                'resultado': resultado,
                'grafico_url': grafico_url,
            })

        except Exception as e:
            return render(request, 'Decreciente.html', {
                'error': f"Error: {str(e)}",
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

def teorias(request):
    return render(request, 'teorias.html')

def continuidad(request):
    error = None
    resultado_continuidad = None
    grafica_base64 = None
    function_input = ''
    punto_continuidad_input = ''
    rango_x_min_input = ''
    rango_x_max_input = ''

    if request.method == "POST":
        function_input = request.POST.get('function_input', '').strip()
        punto_continuidad_input = request.POST.get('punto_continuidad_input', '').strip()
        rango_x_min_input = request.POST.get('rango_x_min_continuidad', '').strip()
        rango_x_max_input = request.POST.get('rango_x_max_continuidad', '').strip()

        if not function_input or not punto_continuidad_input:
            error = "La expresión de la función y el punto de continuidad son requeridos."
        else:
            es_continua, mensaje = verificar_continuidad_en_punto(function_input, punto_continuidad_input)
            resultado_continuidad = {
                "Estado de Continuidad": "Sí" if es_continua else "No",
                "Detalles": mensaje
            }

            grafica_base64, grafica_error = graficar_funcion_continuidad(
                function_input,
                punto_continuidad_input,
                rango_x_min_input,
                rango_x_max_input
            )
            if grafica_error:
                error = f"{error}\nError al generar la gráfica: {grafica_error}" if error else f"Error al generar la gráfica: {grafica_error}"

    context = {
        'function_input': function_input,
        'punto_continuidad_input': punto_continuidad_input,
        'rango_x_min_input': rango_x_min_input,
        'rango_x_max_input': rango_x_max_input,
        'resultado_continuidad': resultado_continuidad,
        'grafica_base64': grafica_base64,
        'error': error,
    }
    return render(request, 'continuidad.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistroForm, LoginForm
from .models import Perfil

# Página principal
def pagprincipal(request):
    contexto = {}
    if request.user.is_authenticated:
        perfil = Perfil.objects.get(user=request.user)
        contexto['usuario'] = request.user.username
        contexto['rol'] = perfil.rol
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
            usuario = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
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
