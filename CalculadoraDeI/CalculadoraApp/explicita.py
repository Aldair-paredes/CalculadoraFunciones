from sympy import symbols, sympify, diff, integrate, limit, series, solve, exp, sin, cos, tan, log, Abs, oo
import re 


x, y, z, t = symbols('x y z t') 

def _limpiar_y_preparar_funcion_str(funcion_str):

    # Normalizar guiones largos a cortos y eliminar espacios
    funcion_limpia = funcion_str.strip().replace('−', '-').replace(' ', '')

    # 1. Eliminar prefijos de función como "f(x)=", "g(t)=", etc.
    funcion_limpia = re.sub(r'^[a-zA-Z](?:\([a-zA-Z]+\))?\s*=\s*', '', funcion_limpia)
    
    # 2. Reemplazar operadores de potencia comunes si no son reconocidos por SymPy
    funcion_limpia = funcion_limpia.replace('^', '**')
    funcion_limpia = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', funcion_limpia)

    # 3. Añadir el signo de multiplicación '*' donde sea implícito
    funcion_con_multiplicacion = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', funcion_limpia)
    funcion_con_multiplicacion = re.sub(r'(\))([a-zA-Z(])', r'\1*\2', funcion_con_multiplicacion)
    
    # Inserta '*' entre una letra y un paréntesis que abre (ej. x(y+1) -> x*(y+1))
    funcion_con_multiplicacion = re.sub(r'([a-zA-Z])(\()', r'\1*\2', funcion_con_multiplicacion)
    
    return funcion_con_multiplicacion


def calcular_funcion_explicita(funcion_str, operacion, **kwargs):

    resultado = None
    error_message = None
    
    try:
        funcion_para_sympy = _limpiar_y_preparar_funcion_str(funcion_str)
        
        funcion_expr = sympify(funcion_para_sympy)

        if operacion == 'derivar':
            variable_derivacion = kwargs.get('variable_derivacion')
            if not variable_derivacion:
                raise ValueError("Para 'derivar', se requiere la variable de derivación.")
            var_der = symbols(variable_derivacion)
            resultado = diff(funcion_expr, var_der)
            
        elif operacion == 'integrar':
            variable_integracion = kwargs.get('variable_integracion')
            if not variable_integracion:
                raise ValueError("Para 'integrar', se requiere la variable de integración.")
            var_int = symbols(variable_integracion)
            resultado = integrate(funcion_expr, var_int)

        elif operacion == 'evaluar':
            valores_evaluacion_str = kwargs.get('valores_evaluacion_str') 
            if not valores_evaluacion_str:
                raise ValueError("Para 'evaluar', se requiere un diccionario de valores de evaluación.")
            
            sustituciones = {}
            partes = valores_evaluacion_str.split(',')
            for parte in partes:
                if '=' in parte:
                    key, value = parte.split('=')
                    sustituciones[symbols(key.strip())] = float(value.strip())
                else:
                    raise ValueError("Formato de valores inválido. Usa 'variable=valor'.")
            
            resultado_sustituido = funcion_expr.subs(sustituciones) 

            if resultado_sustituido.is_number:
                resultado = float(resultado_sustituido)
            else:
                evaluado = resultado_sustituido.evalf()
                if evaluado.is_number:
                    resultado = float(evaluado)
                else:
                    resultado = evaluado 

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

            resultado = limit(funcion_expr, var_lim, punto_limite_sympy)

        elif operacion == 'simplificar':
            resultado = funcion_expr.simplify()
            
        elif operacion == 'resolver':
            variable_resolver = kwargs.get('variable_resolver')
            if not variable_resolver:
                raise ValueError("Para 'resolver', se requiere la variable a resolver.")
            
            var_res = symbols(variable_resolver)
            resultado = solve(funcion_expr, var_res)
            
        else:
            error_message = "Operación no soportada. Las operaciones válidas son: 'derivar', 'integrar', 'evaluar', 'limite', 'simplificar', 'resolver'."

    except (SyntaxError, TypeError, ValueError, NameError) as e:
        error_message = f"Error en la entrada o en la operación: {e}. Asegúrate de que la función y los argumentos sean válidos."
    except Exception as e:
        error_message = f"Ha ocurrido un error inesperado: {e}."
        
    return resultado, error_message