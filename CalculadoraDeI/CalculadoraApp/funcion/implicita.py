import sympy as sp
import numpy as np
import matplotlib.pyplot as mpp
from sympy.utilities.lambdify import lambdify
from scipy.optimize import fsolve

class Funcion_implicita:
    def __init__(self, expresion_str, variable_x ='x', variable_y='y'):
        self.x = sp.symbols(variable_x)
        self.y = sp.symbols(variable_y)

        try:
            self.expresion = sp.sympify(expresion_str)
            self.expresion_str = expresion_str
            self.historial = []
            self._crear_funcion()
        except sp.SympifyError as e:
            raise ValueError(f'Expresión inválida:{expresion_str}') from e
    
    def _crear_funcion(self):
        self.funcion_numerica = lambdify(
            (self.x, self.y),
            self.expresion, 
            modules =['numpy']
        )
    
    def evaluar(self, x_val, y_val):
        try: 
            resultado = self.funcion_numerica(x_val, y_val)
            self.historial.append(('evaluar', x_val, y_val, resultado))
            return resultado
        except Exception as e:
            print(f'Error al evaluar: {e}')
            return None
    
    def resolver_y(self, x_val, y_inicial = 0.0):
        try:
            def ecuacion(y):
                return self.funcion_numerica(x_val, y)
            solucion = fsolve(ecuacion, y_inicial)
            self.historial.append(('resolver', x_val, solucion[0]))
            return solucion[0]
        except Exception as e:
            print(f'Error para resolver y: {e}')
            return None
        
    def derivada(self, respecto_a='y'):
        try:
            if respecto_a == 'y':
                expr_derivada= sp.diff(self.expresion, self.y)
            elif respecto_a == 'x':
                expr_derivada= sp.diff(self.expresion, self.x)
            else:
                raise ValueError("respecto_a debe ser 'x' o 'y'")
            nueva_expresion= f'dF/d{respecto_a} = {str(expr_derivada)}'
            nueva_funcion= Funcion_implicita(str(expr_derivada))
            self.historial.append(('derivada', respecto_a, nueva_expresion))
            return nueva_funcion
        except Exception as e:
            print(f'Error al calcular derivada: {e}')
            return None
