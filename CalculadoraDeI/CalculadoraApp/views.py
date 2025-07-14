from django.shortcuts import render
from django.http import HttpRequest
from collections.abc import Iterable
from .explicita import calcular_funcion_explicita 
from .funcion.implicita import FuncionImplicita
from .transcendente import calcular_funcion_transcendente 
from .funcion.creciente import FuncionCreciente
import matplotlib.pyplot as plt
import base64
import io
import sympy as sp

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