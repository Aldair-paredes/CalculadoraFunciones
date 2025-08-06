from sympy import symbols, sympify, diff, limit, oo, Reals, solve, Eq, S, expand_log, LambertW, pi, E, Abs, sqrt, log, exp, sin, cos, tan, cot, sec, csc, asin, acos, atan, acot, asec, acsc, sinh, cosh, tanh, coth, sech, csch, asinh, acosh, atanh, acoth, asech, acsch
import re
from sympy.parsing.sympy_parser import parse_expr, T, standard_transformations, implicit_multiplication 

import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import sys

x, y, z, t = symbols('x y z t')

def _get_safe_local_dict():
    return {
        'Abs': Abs, 'sqrt': sqrt, 'log': log, 'log10': lambda expr: log(expr, 10), 'exp': exp,
        'sin': sin, 'cos': cos, 'tan': tan, 'cot': cot, 'sec': sec, 'csc': csc,
        'asin': asin, 'acos': acos, 'atan': atan, 'acot': acot, 'asec': asec, 'acsc': acsc,
        'sinh': sinh, 'cosh': cosh, 'tanh': tanh, 'coth': coth, 'sech': sech, 'csch': csch,
        'asinh': asinh, 'acosh': acosh, 'atanh': atanh, 'acoth': acoth, 'asech': acsc,
        'pi': pi, 'E': E, 'oo': oo
    }

def _limpiar_y_preparar_funcion_str(funcion_str):
    funcion_limpia = funcion_str.strip().replace('−', '-').replace(' ', '')
    funcion_limpia = funcion_limpia.replace('⋅', '*')
    funcion_limpia = funcion_limpia.replace('ln(', 'log(')
    funcion_limpia = funcion_limpia.replace('sen(', 'sin(')
    funcion_limpia = re.sub(r'^[a-zA-Z](?:\([a-zA-Z]+\))?\s*=\s*', '', funcion_limpia)
    funcion_limpia = funcion_limpia.replace('^', '**')
    
    funcion_limpia = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', funcion_limpia)
    funcion_limpia = re.sub(r'(\))([a-zA-Z(])', r'\1*\2', funcion_limpia)
    funcion_limpia = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', funcion_limpia)

    return funcion_limpia

def _plot_function(function_expr, variable, limit_point=None):
    try:
        if variable is None:
            raise ValueError("Se necesita una variable para graficar.")
            
        fig, ax = plt.subplots(figsize=(8, 6))

        if limit_point is not None and limit_point != oo and limit_point != -oo:
            try:
                center = float(limit_point)
                x_vals = np.linspace(center - 5, center + 5, 400)
            except (TypeError, ValueError):
                x_vals = np.linspace(-10, 10, 400)
        else:
            x_vals = np.linspace(-10, 10, 400)

        y_vals = []
        for val in x_vals:
            try:
                y_val = sympify(function_expr, locals=_get_safe_local_dict()).subs(variable, val).evalf()
                y_vals.append(float(y_val))
            except (TypeError, ValueError, ZeroDivisionError):
                y_vals.append(np.nan)
        
        y_vals = np.array(y_vals, dtype=float)

        ax.plot(x_vals, y_vals, label=f'$f({variable}) = {function_expr}$', color='#1f77b4')

        if limit_point is not None and limit_point != oo and limit_point != -oo:
            try:
                limit_y = sympify(function_expr, locals=_get_safe_local_dict()).subs(variable, limit_point).evalf()
                ax.plot(float(limit_point), float(limit_y), 'ro', markersize=8, label=f'Límite en ${limit_point}$')
            except (TypeError, ValueError, ZeroDivisionError):
                pass

        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        ax.set_title(f'Gráfica de la función ${function_expr}$', color='black')
        ax.set_xlabel(f'${variable}$', color='black')
        ax.set_ylabel('$f(x)$', color='black')
        
        ax.grid(True, linestyle='--', alpha=0.6, color='#6c757d')
        ax.axhline(0, color='black', linewidth=0.8)
        ax.axvline(0, color='black', linewidth=0.8)
        
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        
        ax.spines['bottom'].set_color('black')
        ax.spines['top'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.spines['left'].set_color('black')

        ax.legend(labelcolor='black')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=False)
        plt.close(fig)
        
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{image_base64}"
    
    except Exception as e:
        sys.stderr.write(f"Error al graficar: {e}\n")
        return None


def calcular_funcion_biyectiva(funcion_str, operacion, **kwargs):
    result = None
    error_message = None
    graph_image_data = None
    safe_local_dict = _get_safe_local_dict()
    
    try:
        funcion_limpia = _limpiar_y_preparar_funcion_str(funcion_str)
        
        funcion_expr = parse_expr(
            funcion_limpia, 
            local_dict=safe_local_dict, 
            transformations=(standard_transformations + (implicit_multiplication,)), 
            evaluate=True
        )

        if operacion == 'derivar':
            variable_derivacion = kwargs.get('variable_derivacion')
            if not variable_derivacion:
                raise ValueError("Para 'derivar', se requiere la variable de derivación.")
            var_der = symbols(variable_derivacion)
            derivada = diff(funcion_expr, var_der)
            result = str(derivada).replace('**', '^').replace('log(', 'ln(')

        elif operacion == 'evaluar':
            valores_evaluacion_str = kwargs.get('valores_evaluacion_str') 
            if not valores_evaluacion_str:
                raise ValueError("Para 'evaluar', se requiere un diccionario de valores de evaluación.")
            
            sustituciones = {}
            partes = valores_evaluacion_str.split(',')
            for parte in partes:
                if '=' in parte:
                    key, value = parte.split('=')
                    sustituciones[symbols(key.strip())] = sympify(value.strip(), locals=safe_local_dict)
                else:
                    raise ValueError("Formato de valores inválido. Usa 'variable=valor'.")
            
            missing_vars = [str(s) for s in funcion_expr.free_symbols if s not in sustituciones and s not in (pi, E)]
            if missing_vars:
                raise ValueError(f"Faltan valores para las variables: {', '.join(missing_vars)}.")
            
            resultado_sustituido = funcion_expr.subs(sustituciones) 

            if resultado_sustituido.is_number:
                try:
                    result = float(resultado_sustituido)
                except TypeError:
                    result = str(resultado_sustituido).replace('**', '^').replace('log(', 'ln(')
            else:
                try:
                    evaluado = resultado_sustituido.evalf()
                    if evaluado.is_number:
                        result = float(evaluado)
                    else:
                        result = str(evaluado).replace('**', '^').replace('log(', 'ln(')
                except Exception:
                    result = str(resultado_sustituido).replace('**', '^').replace('log(', 'ln(')

        elif operacion == 'limite':
            variable_limite = kwargs.get('variable_limite')
            punto_limite_str = kwargs.get('punto_limite')

            if not variable_limite:
                raise ValueError("Para 'limite', se requiere la variable del límite.")
            if not punto_limite_str: 
                raise ValueError("Para 'limite', se requiere el punto del límite.")
            
            var_lim = symbols(variable_limite)
            
            if str(punto_limite_str).lower() in ['infinito', 'oo']:
                punto_limite_sympy = oo
            elif str(punto_limite_str).lower() in ['-infinito', '-oo']:
                punto_limite_sympy = -oo
            else:
                try:
                    punto_limite_sympy = sympify(punto_limite_str, locals=safe_local_dict)
                except Exception:
                    raise ValueError("El punto del límite debe ser un número, 'infinito' o 'oo'.")

            resultado_limite = limit(funcion_expr, var_lim, punto_limite_sympy)
            result = str(resultado_limite).replace('**', '^').replace('log(', 'ln(')
            
            graph_image_data = _plot_function(funcion_expr, var_lim, punto_limite_sympy)

        elif operacion == 'simplificar':
            simplificado = expand_log(funcion_expr, force=True)
            result = str(simplificado).replace('**', '^').replace('log(', 'ln(')
            
        elif operacion == 'resolver':
            variable_resolver = kwargs.get('variable_resolver')
            if not variable_resolver:
                raise ValueError("Para 'resolver', se requiere la variable a resolver.")
            
            var_res = symbols(variable_resolver)
            soluciones = solve(funcion_expr, var_res)
            
            resolved_soluciones = []
            for s in soluciones:
                if s.has(LambertW):
                    try:
                        evaluated_s = s.evalf()
                        if evaluated_s.is_number:
                            resolved_soluciones.append(str(float(evaluated_s)))
                        else:
                            resolved_soluciones.append(str(s).replace('**', '^').replace('log(', 'ln('))
                    except Exception:
                        resolved_soluciones.append(str(s).replace('**', '^').replace('log(', 'ln('))
                else:
                    resolved_soluciones.append(str(s).replace('**', '^').replace('log(', 'ln('))

            result = ", ".join(resolved_soluciones)

        else:
            error_message = "Operación no soportada. Las operaciones válidas son: 'derivar', 'integrar', 'evaluar', 'limite', 'simplificar', 'resolver'."

    except (SyntaxError, TypeError, ValueError, NameError) as e:
        error_message = f"Error interno en la operación matemática: {e}. Por favor, contacta al soporte si este error persiste."
        print(f"ERROR EN CALCULAR_FUNCION_BIYECTIVA: {e}", file=sys.stderr)
    except Exception as e:
        error_message = f"Ha ocurrido un error inesperado: {e}."
        print(f"ERROR INESPERADO EN CALCULAR_FUNCION_BIYECTIVA: {e}", file=sys.stderr)
        
    return result, error_message, graph_image_data