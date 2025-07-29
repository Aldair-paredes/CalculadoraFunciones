import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# Definir símbolo
x = sp.Symbol('x')

# Entrada del usuario
try:
    expresion = input("Ingresa una función en x (ej. x**2 + 3*x + 1): ")
    funcion = sp.sympify(expresion)
except Exception as e:
    print(f"Error al interpretar la función: {e}")
    exit()

# Derivada
derivada = sp.diff(funcion, x)

# Evaluación
try:
    punto = float(input("Ingresa el valor de x para evaluar: "))
    evaluada = funcion.subs(x, punto)
except Exception as e:
    print(f"Error al evaluar la función: {e}")
    exit()

# Límite cuando x -> punto
try:
    limite = sp.limit(funcion, x, punto)
except Exception:
    limite = "No se pudo calcular"

# Simplificación
simplificada = sp.simplify(funcion)

# Resolver f(x) = 0
try:
    soluciones = sp.solve(funcion, x)
except Exception:
    soluciones = "No se pudo resolver"

# Verificar inyectividad: criterio de derivada
inyectiva = False
try:
    derivada_simple = sp.simplify(derivada)
    signo_derivada = sp.solve(derivada_simple > 0)
    if signo_derivada:
        inyectiva = True  # Si hay intervalo donde siempre crece
except Exception:
    inyectiva = False

# Mostrar resultados
print("\n--- RESULTADOS ---")
print(f"Función original: {funcion}")
print(f"Derivada: {derivada}")
print(f"Evaluada en x = {punto}: {evaluada}")
print(f"Límite cuando x → {punto}: {limite}")
print(f"Forma simplificada: {simplificada}")
print(f"Soluciones de f(x) = 0: {soluciones}")
print(f"¿Es inyectiva?: {'Sí (creciente/decreciente)' if inyectiva else 'No segura (puede cambiar de sentido)'}")

# Graficar función
try:
    f_lambd = sp.lambdify(x, funcion, modules=['numpy'])
    x_vals = np.linspace(punto - 10, punto + 10, 400)
    y_vals = f_lambd(x_vals)

    # Validar que los valores de y no contengan NaN o Inf
    if np.any(np.isnan(y_vals)) or np.any(np.isinf(y_vals)):
        raise ValueError("La función contiene valores no definidos en el dominio.")

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label=f'f(x) = {funcion}', color='blue')
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.scatter(punto, float(evaluada), color='red', zorder=5, label=f'f({punto}) = {evaluada}')
    plt.title('Gráfica de la función')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"❌ Error al graficar la función: {e}")
