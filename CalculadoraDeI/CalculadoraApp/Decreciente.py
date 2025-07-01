import sympy as sp

def analizar_funcion():
    print("Analisis de funciones decreciente")
    x = sp.symbols('x')
    expresion= input("ingresa la funcion x (por ejempli: -2*x + 3): ")
    try:
        f = sp.sympify(expresion)
    derivada = sp.diff(f,x)
    print(f"f(x) = {f}")
    print(f"f'(x) = {derivada}")

    intervalos_minimo = float(input("limite inferior del intervalo:"))
    intervalos_maximo = float(input("limite superior del intervalo:"))

    puntos = sp.linspace(intervalos_minimo, intervalos_maximo, 5)
    decreciente = True
    for punto in puntos:
        valor = derivada.subs (x, punto)
        print(f"f'({puntos}) = {valor}")
        if valor > 0:
            decreciente = False

            if decreciente:
                print (" la funcion es decreciente en el intervalo")
               
            else: 
                print ("la duncion no es completamen en el intervalo")
            except:
        print(" Error al interpretar la función. Asegúrate de escribirla correctamente.")

        analizar_funcion()
                