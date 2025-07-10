import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# Definir símbolo
x = sp.Symbol('x')

# Ingresar función
funcion = sp.sympify(input("Ingresa una función en x (ej. x**2 + 3*x + 1): "))

# Derivada
derivada = sp.diff(funcion, x)

# Evaluación
punto = float(input("Ingresa el valor de x para evaluar: "))
evaluada = funcion.subs(x, punto)

# Límite cuando x -> punto
limite = sp.limit(funcion, x, punto)

# Simplificación
simplificada = sp.simplify(funcion)

# Resolver f(x) = 0
soluciones = sp.solve(funcion, x)

# Verificar inyectividad: si derivada > 0 o derivada < 0 en todo su dominio
# Este método no es perfecto, pero da una buena idea usando sympy
inyectiva = False
try:
    # Intentar determinar si siempre es positiva o negativa
    prueba_1 = sp.solve(sp.diff(funcion, x) > 0)
    prueba_2 = sp.solve(sp.diff(funcion, x) < 0)
    if prueba_1 == [sp.S.Reals] or prueba_2 == [sp.S.Reals]:
        inyectiva = True
except:
    inyectiva = False

# Mostrar resultados
print("\n--- RESULTADOS ---")
print(f"Función original: {funcion}")
print(f"Derivada: {derivada}")
print(f"Evaluada en x = {punto}: {evaluada}")
print(f"Límite cuando x → {punto}: {limite}")
print(f"Forma simplificada: {simplificada}")
print(f"Soluciones de f(x) = 0: {soluciones}")
print(f"¿Es inyectiva?: {'Sí' if inyectiva else 'No'}")

# GRAFICAR FUNCIÓN
f_lambd = sp.lambdify(x, funcion, modules=['numpy'])

x_vals = np.linspace(punto - 10, punto + 10, 400)
y_vals = f_lambd(x_vals)

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
