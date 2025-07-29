from sympy import symbols, sympify, diff, integrate, limit, solve, Abs, oo, pi, E
import re
from sympy.parsing.sympy_parser import parse_expr 

x, y, z, t = symbols('x y z t') 

def _limpiar_y_preparar_funcion_str(funcion_str):
    funcion_limpia = funcion_str.strip().replace('−', '-').replace(' ', '')
    funcion_limpia = re.sub(r'^[a-zA-Z](?:\([a-zA-Z]+\))?\s*=\s*', '', funcion_limpia)
    funcion_limpia = funcion_limpia.replace('^', '**')
    funcion_limpia = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', funcion_limpia)
    funcion_limpia = re.sub(r'(\))([a-zA-Z(])', r'\1*\2', funcion_limpia)

    if '=' in funcion_limpia:
        partes = funcion_limpia.split('=')
        izquierda = partes[0]
        derecha = partes[1] if len(partes) > 1 else '0'
        funcion_limpia = f"({izquierda}) - ({derecha})"

    return funcion_limpia


def calcular_funcion_explicita(funcion_expr, operacion, **kwargs):
    resultado = None
    error_message = None
    
    try:
        if operacion == 'derivar':
            variable_derivacion = kwargs.get('variable_derivacion')
            if not variable_derivacion:
                raise ValueError("Para 'derivar', se requiere la variable de derivación.")
            var_der = symbols(variable_derivacion)
            derivada = diff(funcion_expr, var_der)
            resultado = str(derivada).replace('**', '^') 

        elif operacion == 'integrar':
            variable_integracion = kwargs.get('variable_integracion')
            if not variable_integracion:
                raise ValueError("Para 'integrar', se requiere la variable de integración.")
            var_int = symbols(variable_integracion)
            integrado = integrate(funcion_expr, var_int)
            resultado = str(integrado).replace('**', '^')
            
        elif operacion == 'evaluar':
            valores_evaluacion_str = kwargs.get('valores_evaluacion_str') 
            if not valores_evaluacion_str:
                raise ValueError("Para 'evaluar', se requieren valores.")
            
            sustituciones = {}
            partes = valores_evaluacion_str.split(',')
            for parte in partes:
                if '=' in parte:
                    key, value = parte.split('=')
                    sustituciones[symbols(key.strip())] = sympify(value.strip())
                else:
                    raise ValueError("Formato de valores inválido. Usa 'variable=valor'.")
            
            missing_vars = [str(s) for s in funcion_expr.free_symbols if s not in sustituciones and s not in (pi, E)]
            if missing_vars:
                raise ValueError(f"Faltan valores para las variables: {', '.join(missing_vars)}.")

            resultado_sustituido = funcion_expr.subs(sustituciones) 

            if resultado_sustituido.is_number:
                try:
                    resultado = float(resultado_sustituido)
                except TypeError:
                    resultado = str(resultado_sustituido).replace('**', '^')
            else:
                try:
                    evaluado = resultado_sustituido.evalf()
                    if evaluado.is_number:
                        resultado = float(evaluado)
                    else:
                        resultado = str(evaluado).replace('**', '^')
                except Exception:
                    resultado = str(resultado_sustituido).replace('**', '^')

        elif operacion == 'limite':
            variable_limite = kwargs.get('variable_limite')
            punto_limite_str = kwargs.get('punto_limite')

            if not variable_limite:
                raise ValueError("Para 'límite', se requiere la variable del límite.")
            if not punto_limite_str: 
                raise ValueError("Para 'límite', se requiere el punto del límite.")
            
            var_lim = symbols(variable_limite)
            
            if str(punto_limite_str).lower() in ['infinito', 'oo']:
                punto_limite_sympy = oo
            elif str(punto_limite_str).lower() in ['-infinito', '-oo']:
                punto_limite_sympy = -oo
            else:
                try:
                    punto_limite_sympy = sympify(punto_limite_str)
                except Exception:
                    raise ValueError("El punto del límite debe ser un número, 'infinito' o 'oo'.")

            resultado_limite = limit(funcion_expr, var_lim, punto_limite_sympy)
            resultado = str(resultado_limite).replace('**', '^')

        elif operacion == 'simplificar':
            simplificado = funcion_expr.simplify()
            resultado = str(simplificado).replace('**', '^')
            
        elif operacion == 'resolver':
            variable_resolver = kwargs.get('variable_resolver')
            if not variable_resolver:
                raise ValueError("Para 'resolver', se requiere la variable a resolver.")
            
            var_res = symbols(variable_resolver)
            soluciones = solve(funcion_expr, var_res)
            resultado = ", ".join([str(s).replace('**', '^') for s in soluciones])
            
        else:
            error_message = "Operación no soportada. Las operaciones válidas son: 'derivar', 'integrar', 'evaluar', 'limite', 'simplificar', 'resolver'."

    except (SyntaxError, TypeError, ValueError, NameError) as e:
        error_message = f"Error interno en la operación matemática: {e}. Por favor, contacta al soporte si este error persiste."
    except Exception as e:
        error_message = f"Ha ocurrido un error inesperado al calcular: {e}."
            
    return resultado, error_message
