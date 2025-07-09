from sympy import symbols, sympify, diff, limit, oo, Reals, solve, Eq, S, expand_log, LambertW
import re

x, y, z, t = symbols('x y z t')

def _limpiar_y_preparar_funcion_str(funcion_str):
    funcion_limpia = funcion_str.strip().replace('−', '-').replace(' ', '')
    funcion_limpia = funcion_limpia.replace('⋅', '*')
    funcion_limpia = funcion_limpia.replace('ln(', 'log(')
    funcion_limpia = funcion_limpia.replace('sen(', 'sin(')
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

def calcular_funcion_biyectiva(funcion_str, operacion, **kwargs):
    result = None
    error_message = None
    
    try:
        funcion_para_sympy = _limpiar_y_preparar_funcion_str(funcion_str)
        global_symbols = {str(s): s for s in [x, y, z, t, oo]}
        funcion_expr = sympify(funcion_para_sympy, locals=global_symbols)
        
        if operacion == 'derivar':
            variable_derivacion = kwargs.get('variable_derivacion')
            if not variable_derivacion:
                raise ValueError("Para 'derivar', se requiere la variable de derivación.")
            var_der = symbols(variable_derivacion)
            derivada = diff(funcion_expr, var_der)
            formatted_derivada = str(derivada).replace('**', '^').replace('log(', 'ln(')
            result = re.sub(r'\*([a-zA-Z(])', r' \1', formatted_derivada)

        elif operacion == 'evaluar':
            valores_evaluacion_str = kwargs.get('valores_evaluacion_str') 
            if not valores_evaluacion_str:
                raise ValueError("Para 'evaluar', se requiere un diccionario de valores de evaluación.")
            
            valores_raw = {}
            partes = valores_evaluacion_str.split(',')
            for parte in partes:
                if '=' in parte:
                    key, value = parte.split('=')
                    valores_raw[key.strip()] = float(value.strip())
                else:
                    raise ValueError("Formato de valores inválido. Usa 'variable=valor'.")
            
            sustituciones = {}
            for sym in funcion_expr.free_symbols:
                if str(sym) in valores_raw:
                    sustituciones[sym] = valores_raw[str(sym)]
            
            resultado_sustituido = funcion_expr.subs(sustituciones) 

            if resultado_sustituido.is_number:
                result = float(resultado_sustituido)
            else:
                evaluado = resultado_sustituido.evalf()
                if evaluado.is_number:
                    result = float(evaluado)
                else:
                    formatted_evaluado = str(evaluado).replace('**', '^').replace('log(', 'ln(')
                    result = re.sub(r'\*([a-zA-Z(])', r' \1', formatted_evaluado)

        elif operacion == 'limite':
            variable_limite = kwargs.get('variable_limite')
            if not variable_limite:
                raise ValueError("Para 'limite', se requiere la variable del límite.")
            punto_limite = kwargs.get('punto_limite')
            if punto_limite is None: 
                raise ValueError("Para 'limite', se requiere el punto del límite.")
            
            var_lim = symbols(variable_limite)
            
            if str(punto_limite).lower() in ['infinito', 'oo']:
                punto_limite_sympy = oo
            else:
                try:
                    punto_limite_sympy = float(punto_limite)
                except ValueError:
                    raise ValueError("El punto del límite debe ser un número, 'infinito' o 'oo'.")

            result = limit(funcion_expr, var_lim, punto_limite_sympy)
            formatted_result = str(result).replace('**', '^').replace('log(', 'ln(')
            result = re.sub(r'\*([a-zA-Z(])', r' \1', formatted_result)

        elif operacion == 'simplificar':
            simplificado = expand_log(funcion_expr, force=True)
            formatted_simplificado = str(simplificado).replace('**', '^').replace('log(', 'ln(')
            result = re.sub(r'\*([a-zA-Z(])', r' \1', formatted_simplificado)
            
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
            result = re.sub(r'\*([a-zA-Z(])', r' \1', result)

        else:
            error_message = "Operación no soportada. Las operaciones válidas son: 'derivar', 'evaluar', 'limite', 'simplificar', 'resolver'."

    except (SyntaxError, TypeError, ValueError, NameError) as e:
        error_message = f"Error en la entrada o en la operación: {e}. Asegúrate de que la función y los argumentos sean válidos."
    except Exception as e:
        error_message = f"Ha ocurrido un error inesperado: {e}."
    
    return result, error_message
