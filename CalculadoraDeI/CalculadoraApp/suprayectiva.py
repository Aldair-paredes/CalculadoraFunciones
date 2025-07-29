import numpy as np
import matplotlib.pyplot as plt

def plot_user_function():
    """
    Permite al usuario ingresar los parámetros de una función (lineal o cuadrática)
    y la grafica usando Matplotlib.
    Esta función está diseñada para ser llamada desde otra parte de una aplicación.
    """
    print("--- Graficador de Funciones ---")
    print("Elige un tipo de función para graficar:")
    print("1. Función Lineal (f(x) = ax + b)")
    print("2. Función Cuadrática (f(x) = ax^2 + bx + c)")

    func_type = input("Ingresa el número del tipo de función (1 o 2): ")

    if func_type == '1':
        print("\n--- Configurando Función Lineal (f(x) = ax + b) ---")
        try:
            a = float(input("Ingresa el valor de 'a' (pendiente): "))
            b = float(input("Ingresa el valor de 'b' (ordenada al origen): "))
            func_str = f"f(x) = {a}x + {b}"
            func = lambda x: a * x + b
        except ValueError:
            print("Entrada inválida. Por favor, ingresa números para los coeficientes.")
            return
    elif func_type == '2':
        print("\n--- Configurando Función Cuadrática (f(x) = ax^2 + bx + c) ---")
        try:
            a = float(input("Ingresa el valor de 'a': "))
            b = float(input("Ingresa el valor de 'b': "))
            c = float(input("Ingresa el valor de 'c': "))
            func_str = f"f(x) = {a}x^2 + {b}x + {c}"
            func = lambda x: a * x**2 + b * x + c
        except ValueError:
            print("Entrada inválida. Por favor, ingresa números para los coeficientes.")
            return
    else:
        print("Opción de función no válida. Por favor, elige 1 o 2.")
        return

    print("\n--- Define el rango del Dominio (Eje X) para la gráfica ---")
    try:
        x_min = float(input("Ingresa el valor mínimo para X: "))
        x_max = float(input("Ingresa el valor máximo para X: "))
        if x_min >= x_max:
            print("El valor mínimo de X debe ser menor que el valor máximo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, ingresa números para los límites de X.")
        return

    # Generamos los valores de X
    x_valores = np.linspace(x_min, x_max, 400)
    # Calculamos los valores de Y usando la función definida por el usuario
    y_valores = func(x_valores)

    # --- Configuración de la gráfica con Matplotlib ---
    plt.figure(figsize=(10, 6))
    plt.plot(x_valores, y_valores, label=func_str, color='blue')

    # Añadir ejes en el origen si están dentro del rango
    if x_min <= 0 <= x_max:
        plt.axvline(0, color='grey', linestyle='--', linewidth=0.7)
    if min(y_valores) <= 0 <= max(y_valores):
        plt.axhline(0, color='grey', linestyle='--', linewidth=0.7)

    plt.title(f'Gráfica de la Función: {func_str}', fontsize=16)
    plt.xlabel('Dominio (x)', fontsize=12)
    plt.ylabel('Rango / Imagen (y)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()

plot_user_function()

 