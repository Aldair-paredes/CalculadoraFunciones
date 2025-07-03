import sympy as sp
import numpy as np
import matplotlib.pyplot as mpp
from sympy.utilities.lambdify import lambdify
from scipy.optimize import fsolve

class FuncionImplicita:
    def __init__(self, expresion_str, variable_x='x', variable_y='y'):
        self.x = sp.symbols(variable_x)
        self.y = sp.symbols(variable_y)

        try:
            self.expresion = sp.sympify(expresion_str)
            self.expresion_str = expresion_str
            self.historial = []
            self._crear_funcion()
        except sp.SympifyError as e:
            raise ValueError(f'Expresión inválida: {expresion_str}') from e

    def _crear_funcion(self):
        self.funcion_numerica = lambdify(
            (self.x, self.y),
            self.expresion,
            modules=['numpy']
        )

    def evaluar(self, x_val, y_val):
        try:
            resultado = self.funcion_numerica(x_val, y_val)
            self.historial.append(('evaluar', x_val, y_val, resultado))
            return resultado
        except Exception as e:
            print(f'Error al evaluar: {e}')
            return None

    def derivada(self, respecto_a='y', orden=1):
        try:
            if respecto_a == 'y':
                expr_derivada = sp.diff(self.expresion, self.y, orden)
            elif respecto_a == 'x':
                expr_derivada = sp.diff(self.expresion, self.x, orden)
            else:
                raise ValueError("respecto_a debe ser 'x' o 'y'")

            nueva_expresion = f'dF_{orden}/d{respecto_a} = {str(expr_derivada)}'
            nueva_funcion = FuncionImplicita(str(expr_derivada))
            self.historial.append(('derivada', respecto_a, orden, nueva_expresion))
            return nueva_funcion
        except Exception as e:
            print(f'Error al calcular derivada: {e}')
            return None

    def limite(self, variable, punto, direccion='+'):
        try:
            var = self.x if variable == 'x' else self.y
            lim = sp.limit(self.expresion, var, punto, dir=direccion)
            self.historial.append(('limite', variable, punto, direccion, lim))
            return lim
        except Exception as e:
            print(f'Error al calcular límite: {e}')
            return None

    def simplificar(self):
        try:
            expr_simplificada = sp.simplify(self.expresion)
            nueva_funcion = FuncionImplicita(str(expr_simplificada))
            self.historial.append(('simplificar', str(expr_simplificada)))
            return nueva_funcion
        except Exception as e:
            print(f'Error al simplificar: {e}')
            return None

    def resolver(self, respecto='y', valor_sustitucion=None):
        try:
            if respecto == 'y':
                soluciones = sp.solve(self.expresion, self.y)
                if valor_sustitucion is not None:
                    soluciones = [sol.subs(self.x, valor_sustitucion) for sol in soluciones]
            elif respecto == 'x':
                soluciones = sp.solve(self.expresion, self.x)
                if valor_sustitucion is not None:
                    soluciones = [sol.subs(self.y, valor_sustitucion) for sol in soluciones]
            else:
                raise ValueError("Error debe ser 'x' o 'y'")

            soluciones_simples = [sp.simplify(sol) for sol in soluciones]
            self.historial.append(('resolver', respecto, valor_sustitucion, soluciones_simples))
            return soluciones_simples
        except Exception as e:
            print(f'Error al resolver: {e}')
            return None

    def graficar(self, rango_x=(-5, 5), rango_y=(-5, 5), puntos=100):
        try:
            x = np.linspace(rango_x[0], rango_x[1], puntos)
            y = np.linspace(rango_y[0], rango_y[1], puntos)
            X, Y = np.meshgrid(x, y)

            Z = self.funcion_numerica(X, Y)

            fig, ax = mpp.subplots(figsize=(8, 6))
            ax.contour(X, Y, Z, [0], colors='r')
            ax.set_title(f'Gráfica de {self.expresion} = 0')
            ax.set_xlabel(str(self.x))
            ax.set_ylabel(str(self.y))
            ax.grid(True)
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            mpp.show()

            self.historial.append(('graficar', rango_x, rango_y))
        except Exception as e:
            print(f'ERROR AL GRAFICAR: {e}')

    def __str__(self):
        return f"F({self.x}, {self.y}) = {self.expresion} = 0"

    def interactuar(self):
        print("\n Ingresaste la función:")
        print(self)

        # Evaluar
        try:
            x_val = float(input(" Ingresa un valor para x para evaluar: "))
            y_val = float(input(" Ingresa un valor para y para evaluar: "))
            print("Resultado de evaluar:", self.evaluar(x_val, y_val))
        except:
            print(" No se pudo evaluar.")

        # Derivada
        try:
            respecto = input(" Derivar respecto a (x o y): ")
            orden = int(input(" Orden de la derivada (1 o más): "))
            derivada_func = self.derivada(respecto, orden)
            if derivada_func:
                print(" Derivada:", derivada_func)
        except:
            print(" No se pudo derivar.")

        # Límite
        try:
            variable = input(" Variable para límite (x o y): ")
            punto = float(input(" Punto al que tiende: "))
            direccion = input(" Dirección del límite (+, -, o ambos): ")
            print(" Límite:", self.limite(variable, punto, direccion))
        except:
            print(" No se pudo calcular el límite.")

        # Simplificar
        try:
            simplificada = self.simplificar()
            if simplificada:
                print(" Función simplificada:", simplificada)
        except:
            print(" No se pudo simplificar.")

        # Resolver
        try:
            respecto_resolver = input(" Resolver respecto a (x o y): ")
            sustitucion = input(f" Sustituir valor para {'x' if respecto_resolver == 'y' else 'y'} (deja vacío si no): ")
            sustitucion_valor = float(sustitucion) if sustitucion else None
            print(" Soluciones:", self.resolver(respecto_resolver, sustitucion_valor))
        except:
            print(" No se pudo resolver.")

if __name__ == '__main__':
    expr = input(" Ingresa una función implícita en x e y (ej. x**2 + y**2 - 1): ")
    f = FuncionImplicita(expr)
    f.interactuar()
    f.graficar()


