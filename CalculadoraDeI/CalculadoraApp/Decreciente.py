import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

def analizar_funcion():
    print("Análisis de funciones decrecientes")
    x = sp.symbols('x')
    expresion = input("Ingresa la función en x (por ejemplo: -2*x + 3): ")

    try:
        # Interpretar y mostrar la función
        f = sp.sympify(expresion)
        print(f"\nFunción original: f(x) = {f}")

        # Derivada
        derivada = sp.diff(f, x)
        print(f"Derivada: f'(x) = {derivada}")

        # Simplificar
        simplificada = sp.simplify(f)
        print(f"Función simplificada: {simplificada}")

        # Soluciones
        soluciones = sp.solve(f, x)
        print(f"Soluciones a f(x) = 0: {soluciones if soluciones else 'No hay soluciones reales encontradas.'}")

        # Límite en un punto
        punto_limite = float(input("\nIngresa el punto donde calcular el límite: "))
        limite = sp.limit(f, x, punto_limite)
        print(f"Límite de f(x) cuando x → {punto_limite}: {limite}")

        # Intervalo de análisis
        intervalo_minimo = float(input("\nLímite inferior del intervalo: "))
        intervalo_maximo = float(input("Límite superior del intervalo: "))

        puntos = np.linspace(intervalo_minimo, intervalo_maximo, 100)
        derivadas_numericas = [float(derivada.subs(x, punto)) for punto in puntos]

        # Evaluar si es decreciente
        es_decreciente = all(valor <= 0 for valor in derivadas_numericas)
        if es_decreciente:
            print("\nConclusión: La función es decreciente en todo el intervalo.")
        else:
            print("\nConclusión: La función no es completamente decreciente en el intervalo.")

        # Graficar si el usuario quiere
        graficar = input("\n¿Deseas graficar la función y su derivada? (s/n): ").strip().lower()
        if graficar == 's':
            f_lambd = sp.lambdify(x, f, modules=['numpy'])
            deriv_lambd = sp.lambdify(x, derivada, modules=['numpy'])

            y_f = f_lambd(puntos)
            y_df = deriv_lambd(puntos)

            # Corregir caso escalar (constante)
            if np.isscalar(y_f):
                y_f = np.full_like(puntos, y_f, dtype=float)
            else:
                y_f = np.array(y_f, dtype=float)

            if np.isscalar(y_df):
                y_df = np.full_like(puntos, y_df, dtype=float)
            else:
                y_df = np.array(y_df, dtype=float)

            # Graficar
            plt.figure(figsize=(10, 6))
            plt.plot(puntos, y_f, label='f(x)', color='blue')
            plt.plot(puntos, y_df, label="f'(x)", color='red', linestyle='--')
            plt.axhline(0, color='black', linewidth=0.5)
            plt.title('Función y su derivada')
            plt.xlabel('x')
            plt.ylabel('Valor')
            plt.legend()
            plt.grid(True)
            plt.show()

    except Exception as e:
        print("\n❌ Error al interpretar la función. Asegúrate de escribirla correctamente.")
        print(f"🔍 Detalle del error: {e}")

# Ejecutar la función
analizar_funcion()
