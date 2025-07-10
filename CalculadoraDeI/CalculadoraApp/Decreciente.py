import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# Aqui para ingresar la funcion y analizar si es decreciente

def analizar_funcion():
    print("Análisis de funciones decrecientes")
    x = sp.symbols('x')
<<<<<<< HEAD
    expresion = input("Ingresa la función en x (por ejemplo: -2*x + 3): ")

=======
    expresion= input("ingresa la funcion x (por ejempli: -2*x + 3): ")
# aqui lo que hace el codigo es tomar la funcion y si es posible calcular la derivada
>>>>>>> 54a7487 (agregar comentario de lo que hace cada parte de mi codigo)
    try:
        # Interpretar la función
        f = sp.sympify(expresion)
<<<<<<< HEAD
        print(f"\nFunción original: f(x) = {f}")

        # Derivar la función
        derivada = sp.diff(f, x)
        print(f"Derivada: f'(x) = {derivada}")

        # Simplificar la función
        simplificada = sp.simplify(f)
        print(f"Función simplificada: {simplificada}")

        # Resolver la ecuación f(x) = 0
        soluciones = sp.solve(f, x)
        print(f"Soluciones a f(x)=0: {soluciones if soluciones else 'No hay soluciones reales encontradas.'}")
=======
    derivada = sp.diff(f,x)
    print(f"f(x) = {f}")
    print(f"f'(x) = {derivada}")
# aqui vamos a ingresar los intervalos que queremos analizar
    intervalos_minimo = float(input("limite inferior del intervalo:"))
    intervalos_maximo = float(input("limite superior del intervalo:"))

    puntos = sp.linspace(intervalos_minimo, intervalos_maximo, 5)
    decreciente = True
    for punto in puntos:
        valor = derivda.subs (x, punto)
        print(f"f'({puntos}) = {valor}")
        if valor > 0:
            decreciente = False
# aqui es donde dara el resultado si la funcion es decreciente o no 
            if decreciente:
                print (" la funcion es decreciente en el intervalo")
               
            else: 
                print ("la duncion no es completamen en el intervalo")
                except:
        print(" Error al interpretar la función. Asegúrate de escribirla correctamente.") }
>>>>>>> 54a7487 (agregar comentario de lo que hace cada parte de mi codigo)

        # Calcular límite en un punto (pide el punto al usuario)
        punto_limite = float(input("\nIngresa el punto donde calcular el límite: "))
        limite = sp.limit(f, x, punto_limite)
        print(f"Límite de f(x) cuando x → {punto_limite}: {limite}")

        # Evaluar si la función es decreciente en un intervalo
        intervalo_minimo = float(input("\nLímite inferior del intervalo: "))
        intervalo_maximo = float(input("Límite superior del intervalo: "))

        puntos = np.linspace(intervalo_minimo, intervalo_maximo, 100)
        derivadas_numericas = [float(derivada.subs(x, punto)) for punto in puntos]

        decreciente = all(valor <= 0 for valor in derivadas_numericas)

        if decreciente:
            print("\nConclusión: La función es decreciente en todo el intervalo.")
        else:
            print("\nConclusión: La función no es completamente decreciente en el intervalo.")

        # Opcional: graficar función y derivada
        graficar = input("\n¿Deseas graficar la función y su derivada? (s/n): ").strip().lower()
        if graficar == 's':
            f_lambd = sp.lambdify(x, f, modules=['numpy'])
            deriv_lambd = sp.lambdify(x, derivada, modules=['numpy'])
            y_f = f_lambd(puntos)
            y_df = deriv_lambd(puntos)

            # Asegurarse de que y_f y y_df sean arrays compatibles con puntos
            if np.isscalar(y_f):
                y_f = np.full_like(puntos, y_f)
            if np.isscalar(y_df):
                y_df = np.full_like(puntos, y_df)

            plt.figure(figsize=(10,6))
            plt.plot(puntos, y_f, label='f(x)', color='blue')
            plt.plot(puntos, y_df, label="f'(x)", color='red', linestyle='--')
            plt.axhline(0, color='black', linewidth=0.5)
            plt.legend()
            plt.title('Función y su derivada')
            plt.xlabel('x')
            plt.ylabel('Valor')
            plt.grid(True)
            plt.show()

    except Exception as e:
        print("\nError al interpretar la función. Asegúrate de escribirla correctamente.") 
        print(f"Detalle del error: {e}")

analizar_funcion()