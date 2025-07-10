import sympy as sp

<<<<<<< HEAD
# Aqui para ingresar la funcion y analizar si es decreciente

=======
>>>>>>> 306f1ff97307917dfa96388bdeafb98d37f9a183
def analizar_funcion():
    print("Analisis de funciones decreciente")
    x = sp.symbols('x')
    expresion= input("ingresa la funcion x (por ejempli: -2*x + 3): ")
<<<<<<< HEAD
# aqui lo que hace el codigo es tomar la funcion y si es posible calcular la derivada
=======
>>>>>>> 306f1ff97307917dfa96388bdeafb98d37f9a183
    try:
        f = sp.sympify(expresion)
    derivada = sp.diff(f,x)
    print(f"f(x) = {f}")
    print(f"f'(x) = {derivada}")
<<<<<<< HEAD
# aqui vamos a ingresar los intervalos que queremos analizar
=======

>>>>>>> 306f1ff97307917dfa96388bdeafb98d37f9a183
    intervalos_minimo = float(input("limite inferior del intervalo:"))
    intervalos_maximo = float(input("limite superior del intervalo:"))

    puntos = sp.linspace(intervalos_minimo, intervalos_maximo, 5)
    decreciente = True
    for punto in puntos:
<<<<<<< HEAD
        valor = derivda.subs (x, punto)
        print(f"f'({puntos}) = {valor}")
        if valor > 0:
            decreciente = False
# aqui es donde dara el resultado si la funcion es decreciente o no 
=======
        valor = derivada.subs (x, punto)
        print(f"f'({puntos}) = {valor}")
        if valor > 0:
            decreciente = False

>>>>>>> 306f1ff97307917dfa96388bdeafb98d37f9a183
            if decreciente:
                print (" la funcion es decreciente en el intervalo")
               
            else: 
                print ("la duncion no es completamen en el intervalo")
                except:
<<<<<<< HEAD
        print(" Error al interpretar la función. Asegúrate de escribirla correctamente.") }
=======
        print(" Error al interpretar la función. Asegúrate de escribirla correctamente.") 
>>>>>>> 306f1ff97307917dfa96388bdeafb98d37f9a183

        analizar_funcion()
                