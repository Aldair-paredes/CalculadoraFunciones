from sympy import symbols, Eq, solve, simplify, expand, Poly, sqrt, sympify

# --- 1. Declarar Símbolos (global para el script) ---
x, y, z = symbols('x y z')

# --- 2. Funciones de SymPy (simplificadas para este archivo) ---

def _solve_equation_internal(equation_expr, variable):
    """Resuelve una sola ecuación."""
    return solve(equation_expr, variable)

def _simplify_expression_internal(expression):
    """Simplifica una expresión."""
    return simplify(expression)

def _expand_expression_internal(expression):
    """Expande una expresión."""
    return expand(expression)

def _factor_polynomial_internal(polynomial_expr, variable):
    """Factoriza un polinomio."""
    try:
        return Poly(polynomial_expr, variable).factor()
    except Exception:
        return polynomial_expr.factor()

# --- 3. Funciones de la Calculadora (interacción con el usuario) ---

def calculate_linear_function():
    """Calcula una función lineal f(x) = mx + b."""
    print("\n--- Calculadora de Función Lineal (f(x) = mx + b) ---")
    while True:
        try:
            m_str = input("Ingrese el valor de 'm' (pendiente): ")
            b_str = input("Ingrese el valor de 'b' (intersección con el eje y): ")
            m = sympify(m_str)
            b = sympify(b_str)
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese valores numéricos o expresiones válidas para m y b.")

    func_expr = m * x + b
    print(f"\nLa función lineal es: f(x) = {func_expr}")

    while True:
        try:
            val_x_str = input("Ingrese un valor para 'x' para evaluar la función (o 's' para saltar): ")
            if val_x_str.lower() == 's':
                break
            val_x = sympify(val_x_str)
            result = func_expr.subs(x, val_x)
            print(f"f({val_x}) = {result}")
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese un valor numérico o expresión válida para x.")

    while True:
        try:
            solve_val_str = input("¿Desea resolver para 'x' cuando f(x) = C? Ingrese C (o 's' para saltar): ")
            if solve_val_str.lower() == 's':
                break
            solve_val = sympify(solve_val_str)
            equation_to_solve = Eq(func_expr, solve_val)
            solution = _solve_equation_internal(equation_to_solve, x)
            print(f"Para f(x) = {solve_val}, x = {solution}")
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese un valor numérico o expresión válida para C.")

def calculate_quadratic_function():
    """Calcula una función cuadrática f(x) = ax^2 + bx + c."""
    print("\n--- Calculadora de Función Cuadrática (f(x) = ax^2 + bx + c) ---")
    while True:
        try:
            a_str = input("Ingrese el valor de 'a': ")
            b_str = input("Ingrese el valor de 'b': ")
            c_str = input("Ingrese el valor de 'c': ")
            a = sympify(a_str)
            b = sympify(b_str)
            c = sympify(c_str)
            if a == 0:
                print("El coeficiente 'a' no puede ser cero para una función cuadrática. Será una lineal.")
                continue
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese valores numéricos o expresiones válidas.")

    func_expr = a * x**2 + b * x + c
    print(f"\nLa función cuadrática es: f(x) = {func_expr}")

    while True:
        try:
            val_x_str = input("Ingrese un valor para 'x' para evaluar la función (o 's' para saltar): ")
            if val_x_str.lower() == 's':
                break
            val_x = sympify(val_x_str)
            result = func_expr.subs(x, val_x)
            print(f"f({val_x}) = {result}")
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese un valor numérico o expresión válida para x.")

    print("\nResolviendo las raíces (f(x) = 0):")
    roots = _solve_equation_internal(Eq(func_expr, 0), x)
    print(f"Las raíces de la función son: {roots}")

def calculate_polynomial_function():
    """Calcula una función polinómica."""
    print("\n--- Calculadora de Función Polinómica ---")
    print("Ingrese la función polinómica en términos de 'x'.")
    print("Ejemplo: x**3 - 2*x**2 + x - 5")
    while True:
        try:
            poly_str = input("Ingrese la expresión del polinomio: ")
            poly_expr = sympify(poly_str)
            if not poly_expr.free_symbols.issubset({x, y, z}) and poly_expr != 0: # 0 es un polinomio válido
                 print("La expresión debe contener la variable 'x', 'y' o 'z' y ser un polinomio válido.")
                 continue
            if not poly_expr.is_polynomial(x):
                print("La expresión ingresada no parece ser un polinomio válido de 'x'.")
                continue
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese una expresión polinómica válida.")

    print(f"\nLa función polinómica es: f(x) = {poly_expr}")

    while True:
        try:
            val_x_str = input("Ingrese un valor para 'x' para evaluar la función (o 's' para saltar): ")
            if val_x_str.lower() == 's':
                break
            val_x = sympify(val_x_str)
            result = poly_expr.subs(x, val_x)
            print(f"f({val_x}) = {result}")
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese un valor numérico o expresión válida para x.")

    print("\nResolviendo las raíces (f(x) = 0):")
    roots = _solve_equation_internal(Eq(poly_expr, 0), x)
    print(f"Las raíces de la función son: {roots}")

    print("\nIntentando factorizar el polinomio:")
    try:
        factored_poly = _factor_polynomial_internal(poly_expr, x)
        print(f"Forma factorizada: {factored_poly}")
    except Exception as e:
        print(f"No se pudo factorizar o no aplica: {e}")

def calculate_rational_function():
    """Calcula una función racional f(x) = p(x) / q(x)."""
    print("\n--- Calculadora de Función Racional (f(x) = p(x) / q(x)) ---")
    print("Ingrese el numerador p(x) y el denominador q(x) en términos de 'x'.")
    print("Ejemplo: Numerador: x**2 + 1, Denominador: x - 3")
    while True:
        try:
            num_str = input("Ingrese la expresión del numerador p(x): ")
            den_str = input("Ingrese la expresión del denominador q(x): ")
            numerator = sympify(num_str)
            denominator = sympify(den_str)
            if denominator == 0:
                print("El denominador no puede ser cero. Ingrese otra expresión.")
                continue
            if not numerator.free_symbols.issubset({x, y, z}) and numerator != 0 and denominator != 0 or \
               not denominator.free_symbols.issubset({x, y, z}) and numerator != 0 and denominator != 0:
                print("Las expresiones deben contener la variable 'x' (o 'y', 'z') y ser válidas.")
                # Permitir constantes como 5 / (x+1) o x / 3
                if not (numerator.is_constant() or denominator.is_constant()):
                    continue
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese expresiones válidas.")

    func_expr = numerator / denominator
    print(f"\nLa función racional es: f(x) = {func_expr}")

    while True:
        try:
            val_x_str = input("Ingrese un valor para 'x' para evaluar la función (o 's' para saltar): ")
            if val_x_str.lower() == 's':
                break
            val_x = sympify(val_x_str)
            if denominator.subs(x, val_x) == 0:
                print(f"Error: El denominador es cero para x = {val_x}. División por cero.")
                continue
            result = func_expr.subs(x, val_x)
            print(f"f({val_x}) = {result}")
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese un valor numérico o expresión válida para x.")

    print("\nIntentando simplificar la función racional:")
    simplified_func = _simplify_expression_internal(func_expr)
    print(f"Forma simplificada: {simplified_func}")

def calculate_radical_function():
    """Calcula una función radical f(x) = sqrt(g(x))."""
    print("\n--- Calculadora de Función Radical (f(x) = sqrt(g(x))) ---")
    print("Ingrese la expresión bajo la raíz (g(x)) en términos de 'x'.")
    print("Ejemplo: x + 2")
    while True:
        try:
            g_x_str = input("Ingrese la expresión g(x) bajo la raíz: ")
            g_x_expr = sympify(g_x_str)
            if not g_x_expr.free_symbols.issubset({x, y, z}) and g_x_expr != 0:
                 print("La expresión debe contener la variable 'x' (o 'y', 'z') y ser válida.")
                 continue
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese una expresión válida.")

    func_expr = sqrt(g_x_expr)
    print(f"\nLa función radical es: f(x) = {func_expr}")

    while True:
        try:
            val_x_str = input("Ingrese un valor para 'x' para evaluar la función (o 's' para saltar): ")
            if val_x_str.lower() == 's':
                break
            val_x = sympify(val_x_str)
            arg_under_sqrt = g_x_expr.subs(x, val_x)
            if arg_under_sqrt.is_real and arg_under_sqrt < 0:
                print(f"Error: La expresión bajo la raíz es negativa para x = {val_x}. No es un número real.")
                continue
            result = func_expr.subs(x, val_x)
            print(f"f({val_x}) = {result}")
            break
        except (SyntaxError, TypeError, ValueError):
            print("Entrada inválida. Por favor, ingrese un valor numérico o expresión válida para x.")
        except Exception as e:
            print(f"Ocurrió un error al evaluar: {e}")

# --- 4. Función Principal de Ejecución ---

def run_algebra_calculator():
    """Ejecuta la interfaz de la calculadora de funciones algebraicas."""
    print("\n===== CALCULADORA DE FUNCIONES ALGEBRAICAS =====")
    while True:
        print("\nSeleccione el tipo de función:")
        print("1. Función Lineal (f(x) = mx + b)")
        print("2. Función Cuadrática (f(x) = ax^2 + bx + c)")
        print("3. Función Polinómica (f(x) = ax^n + ...)")
        print("4. Función Racional (f(x) = p(x) / q(x))")
        print("5. Función Radical (f(x) = sqrt(g(x)))")
        print("0. Salir")

        choice = input("Ingrese su opción: ")

        if choice == '1':
            calculate_linear_function()
        elif choice == '2':
            calculate_quadratic_function()
        elif choice == '3':
            calculate_polynomial_function()
        elif choice == '4':
            calculate_rational_function()
        elif choice == '5':
            calculate_radical_function()
        elif choice == '0':
            print("Saliendo de la calculadora. ¡Adiós!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")
