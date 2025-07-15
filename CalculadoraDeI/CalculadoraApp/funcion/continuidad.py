import sympy as sp
from sympy import symbols, limit, N, SympifyError
from sympy.abc import x
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def verificar_continuidad_en_punto(expresion_str, punto_a_str):
    try:
        f_x = sp.sympify(expresion_str)
    except SympifyError:
        return False, f"Error: La expresión '{expresion_str}' no es una función simbólica válida."

    try:
        punto_a = float(punto_a_str)
    except ValueError:
        return False, f"Error: El punto '{punto_a_str}' debe ser un valor numérico."

    try:
        valor_fa = f_x.subs(x, punto_a)
        if valor_fa.is_infinite:
            return False, f"f({punto_a}) es indefinida (infinito)."
        valor_fa_num = N(valor_fa)
    except Exception as e:
        return False, f"f({punto_a}) es indefinida en el punto: {e}"

    try:
        limite_izquierdo = limit(f_x, x, punto_a, dir='-')
        if limite_izquierdo.is_infinite:
            return False, f"El límite por la izquierda en {punto_a} es infinito."
        limite_izquierdo_num = N(limite_izquierdo)
    except Exception as e:
        return False, f"No se pudo calcular el límite por la izquierda en {punto_a}: {e}"

    try:
        limite_derecho = limit(f_x, x, punto_a, dir='+')
        if limite_derecho.is_infinite:
            return False, f"El límite por la derecha en {punto_a} es infinito."
        limite_derecho_num = N(limite_derecho)
    except Exception as e:
        return False, f"No se pudo calcular el límite por la derecha en {punto_a}: {e}"

    tolerancia = 1e-9
    if abs(limite_izquierdo_num - limite_derecho_num) < tolerancia:
        limite_bilateral = limite_izquierdo_num
        if abs(limite_bilateral - valor_fa_num) < tolerancia:
            return True, f"La función es **continua** en $x = {punto_a}$.\n$f({punto_a}) = {valor_fa_num:.4f}$, Límite = ${limite_bilateral:.4f}$"
        else:
            return False, f"La función es **discontinua** en $x = {punto_a}$ (Límite $\\neq$ $f(a)$).\n$f({punto_a}) = {valor_fa_num:.4f}$, Límite = ${limite_bilateral:.4f}$"
    else:
        return False, f"La función es **discontinua** en $x = {punto_a}$ (Los límites laterales no son iguales).\nLímite Izquierdo = ${limite_izquierdo_num:.4f}$, Límite Derecho = ${limite_derecho_num:.4f}$"

def graficar_funcion_continuidad(expresion_str, punto_a_str=None, rango_x_min_str=None, rango_x_max_str=None):
    try:
        f_x = sp.sympify(expresion_str)
        f_callable = lambda val: N(f_x.subs(x, val))
    except SympifyError:
        return None, "Error de SymPy: La expresión no es una función simbólica válida."

    punto_a = None
    if punto_a_str:
        try:
            punto_a = float(punto_a_str)
        except ValueError:
            return None, "Error: El punto 'a' para graficar debe ser un número."

    rango_x = (-5.0, 5.0)
    try:
        if rango_x_min_str and rango_x_max_str:
            rango_x_min = float(rango_x_min_str)
            rango_x_max = float(rango_x_max_str)
            if rango_x_min >= rango_x_max:
                raise ValueError("El rango mínimo debe ser menor que el máximo.")
            rango_x = (rango_x_min, rango_x_max)
        elif punto_a is not None:
            rango_x = (punto_a - 5, punto_a + 5)
    except ValueError as e:
        return None, f"Error en el rango de X para la gráfica: {e}. Se usará el rango por defecto (-5, 5)."
    except Exception as e:
        return None, f"Error inesperado al configurar el rango de X para la gráfica: {e}. Se usará el rango por defecto (-5, 5)."

    x_vals = np.linspace(rango_x[0], rango_x[1], 400)
    y_vals = []
    for val in x_vals:
        try:
            y_vals.append(f_callable(val))
        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            y_vals.append(np.nan) 

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=f'$f(x) = {expresion_str}$', color='blue')

    if punto_a is not None:
        try:
            valor_fa_grafica = N(f_x.subs(x, punto_a))
            if not np.isinf(valor_fa_grafica) and not np.isnan(valor_fa_grafica):
                plt.plot(punto_a, valor_fa_grafica, 'ro', markersize=8, label=f'$f({punto_a}) = {valor_fa_grafica:.4f}$ (Punto de análisis)')
            else:
                pass
        except Exception:
            pass 

    plt.title(f'Gráfica de $f(x) = {expresion_str}$')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.7)
    plt.grid(True)
    plt.legend()
    plt.ylim(auto=True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64, None