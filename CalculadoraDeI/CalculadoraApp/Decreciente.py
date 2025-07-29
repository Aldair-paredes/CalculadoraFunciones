import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import re

def preparar_expresion(expr_str):
    expr_str = expr_str.replace('^', '**')
    expr_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr_str)
    expr_str = re.sub(r'(\))([a-zA-Z(])', r'\1*\2', expr_str)
    return expr_str

def leer_flotante(mensaje):
    valor = input(mensaje)
    if valor is None or valor.strip() == '':
        raise ValueError("⚠️ Entrada vacía. No se ingresó un número.")
    return float(valor.strip())

def analizar_funcion():
    print("=== Análisis de funciones ===")

    x = sp.symbols('x')
    expresion_usuario = input("Ingresa la función (ej: -2x+3, x^2, sin(x)): ").strip()

    if not expresion_usuario:
        print("❌ No ingresaste una función.")
        return

    expresion_corregida = preparar_expresion(expresion_usuario)

    try:
        f = sp.sympify(expresion_corregida)
    except Exception as e:
        print(f"❌ Error al interpretar la función: {e}")
        return

    print(f"\n✅ Función interpretada: f(x) = {f}")

    try:
        derivada = sp.diff(f, x)
        print(f"📉 Derivada: f'(x) = {derivada}")
    except Exception as e:
        print(f"❌ Error al derivar la función: {e}")
        return

    try:
        soluciones = sp.solve(f, x)
        print(f"🔍 Soluciones f(x)=0: {soluciones if soluciones else 'Ninguna'}")
    except Exception as e:
        print(f"⚠️ No se pudieron calcular soluciones: {e}")

    # Cálculo del límite
    try:
        punto = leer_flotante("Punto para límite: ")
        lim = sp.limit(f, x, punto)
        print(f"📌 Límite cuando x → {punto} = {lim}")
    except Exception as e:
        print(f"⚠️ No se pudo calcular el límite: {e}")

    # Análisis de decrecimiento
    print("\n--- Análisis de Decrecimiento ---")
    try:
        a = leer_flotante("Límite inferior: ")
        b = leer_flotante("Límite superior: ")

        if a >= b:
            print("❌ El límite inferior debe ser menor que el superior.")
            return
    except Exception as e:
        print(f"❌ Error al leer el intervalo: {e}")
        return

    try:
        puntos = np.linspace(a, b, 300)
        f_lamb = sp.lambdify(x, f, modules=['numpy'])
        df_lamb = sp.lambdify(x, derivada, modules=['numpy'])

        y_f = f_lamb(puntos)
        y_df = df_lamb(puntos)

        y_f = np.nan_to_num(y_f, nan=np.nan)
        y_df = np.nan_to_num(y_df, nan=0.0, posinf=1e10, neginf=-1e10)

        if np.all(y_df <= 1e-9):
            print("✅ La función es decreciente en el intervalo.")
        else:
            print("❌ La función NO es completamente decreciente en el intervalo.")
    except Exception as e:
        print(f"❌ Error en el análisis de decrecimiento: {e}")
        return

    # Graficar
    try:
        graficar = input("¿Graficar la función y derivada? (s/n): ").strip().lower()
        if graficar == 's':
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
            plt.show()
    except Exception as e:
        print(f"❌ Error al graficar: {e}")

# Ejecutar
analizar_funcion()
