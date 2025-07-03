import sympy as sp
import numpy as np
import matplotlib.pyplot as mpp
from sympy.utilities.lambdify import lambdify

class FuncionCreciente:
    def __init__(self, expresion_str, variable='x'):
        self.x = sp.symbols(variable)

        try:
            self.expresion = sp.sympify(expresion_str)
            self.expresion_str = expresion_str
            self.historial = []
            self._crear_funcion()
        except sp.SympifyError as e:
            raise ValueError(F'Expresión invalida: {expresion_str}') from e
        
    def _crear_funcion(self):
        self.funcion_numerica = lambdify(self.x, self.expresion, modules=['numpy']) 

    def evaluar(self, x_val):

        try:
            resultado = self.funcion_numerica(x_val)
            self.historial.append(('evaluar', x_val, resultado))
            return resultado
        except Exception as e:
            print(f'Error al evaluar: {e}')
            return None
        
    def derivada(self, orden=1):

        try:
            expr_derivada = sp.diff(self.expresion, self.x, orden)      
            nueva_expre = f'd^{orden}f/dx^{orden} ={str(expr_derivada)}'
            nueva_funcion = FuncionCreciente(str(expr_derivada))
            self.historial.append(('derivada', orden, nueva_expre))
            return nueva_funcion
        except Exception as e:
            print(f'Error al calcular derivada: {e}')
            return None
        
        def _creciente(self, intervalo=(-sp.oo, sp.oo)):
            
            try:
                derivada = self.derivada(1)
                a, b = sp.solve(derivada.expresion < 0, self.x)
                if not soluciones:
                    return True
                for sol in soluciones:
                    if sol > a and sol < b:
                        return False
                if derivada.evaluar(a) < 0 or derivada.evaluar(b) < 0:
                    return False
                
                return True
            except Exception as e:
                print(f'Error al determinar crecimiento: {e}')
                return None