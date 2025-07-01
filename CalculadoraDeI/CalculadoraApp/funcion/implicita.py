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
        
    def derivada(self, respecto_a='y', orden=1):
        try:
            if respecto_a == 'y':
                expr_derivada= sp.diff(self.expresion, self.y, orden)
            elif respecto_a == 'x':
                expr_derivada= sp.diff(self.expresion, self.x, orden)
            else:
                raise ValueError("respecto_a debe ser 'x' o 'y'")
            nueva_expresion= f'df_{orden}/d{respecto_a} = {str(expr_derivada)}'
            nueva_funcion= Funcion_implicita(str(expr_derivada))
            self.historial.append(('derivada', respecto_a, orden, nueva_expresion))
            return nueva_funcion
        except Exception as e:
            print(f'Error al calcular derivada: {e}')
            return None
        
    def limite( self, variable, punto, direccion='+'):
        try: 
           var = self.x if variable == 'x' else self.y
           lim = sp.limit(self.expresion, var, punto, dir=direccion)
        
           self.historial.append(('limite', variable, punto, direccion, lim))
           return lim
        except Exception as e:
         print(f'Error al calcular límite: {e}')
         return None

    def simplificador(self):
        try:
            expr_simplificada = sp.simplify(self.expresion)
            nueva_funcion = Funcion_implicita(str(expr_simplificada))
            self.historial.append(('simplificar'), str(expr_simplificada))
        except