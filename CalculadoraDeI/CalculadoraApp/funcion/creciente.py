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
            a, b = intervalo
            soluciones = sp.solve(derivada.expresion < 0, self.x)
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
        
    def encontrar (self):

        try:
            derivada = self.derivada(1)
            puntos_criticos = sp.solve(derivada.expresion, self.x)
            puntos_criticos = sorted({float(p.evalf()) for p in puntos_criticos if p.is_real})

            puntos_criticos = [-sp.oo] + puntos_criticos + [sp.Oo]
            intervalos_crecientes = []

            for i in range(len(puntos_criticos)-1):
                a = puntos_criticos[i]
                b = puntos_criticos[i+1]

                if a == -sp.oo and b == sp.oo:
                    punto_prueba = 0
                elif a == -sp.oo:
                    punto_prueba = b - 1
                elif b== sp.oo:
                    punto_prueba = a + 1
                else:
                    punto_prueba = (a + b )/2

                valor_derivada = derivada.evaluar(punto_prueba)

                if valor_derivada > 0:
                    intervalos_crecientes.append((a,b))
                
            self.historial.append(('encontrar_crecimiento', intervalos_crecientes))
            return intervalos_crecientes
        except Exception as e:
            print(f'Eror al encontrar intervalos de crecimiento: {e}')
            return None
            
    def graficar(self, rango_x=(-5, 5), puntos=1000):
             
            try:
                x_vals = np.linspace(rango_x[0], rango_x[1], puntos)
                y_vals = self.funcion_numerica(x_vals)
            
                derivada = self.derivada(1)
                dy_vals = derivada.funcion_numerica(x_vals)
            
                fig, (ax1, ax2) = mpp.subplots(2, 1, figsize=(10, 8))
            
            # Gráfica de la función
                ax1.plot(x_vals, y_vals, label=f'f(x) = {self.expresion_str}')
                ax1.set_title('Función')
                ax1.set_xlabel('x')
                ax1.set_ylabel('f(x)')
                ax1.grid(True)
                ax1.legend()
            
            # Gráfica de la derivada
                ax2.plot(x_vals, dy_vals, label=f"f'(x) = {derivada.expresion_str}", color='orange')
                ax2.axhline(0, color='red', linestyle='--', linewidth=0.5)
                ax2.set_title('Derivada')
                ax2.set_xlabel('x')
                ax2.set_ylabel("f'(x)")
                ax2.grid(True)
                ax2.legend()
            
                mpp.tight_layout()
                mpp.show()
            
                self.historial.append(('graficar', rango_x))
            except Exception as e:
                print(f'Error al graficar: {e}')
    
    def __str__(self):
        return f"f({self.x}) = {self.expresion_str}"

def main():
        print("Análisis de Funciones Crecientes")
    
        expresion = input("Ingresa una función en términos de x (ej. x**2, sin(x), exp(x)): ")
    
        try:
            f = FuncionCreciente(expresion)
            print(f"\nFuncióm creada: {f}")
        
            x_eval = float(input("\nIngresa un valor de x para evaluar la función: "))
            print(f"f({x_eval}) = {f.evaluar(x_eval)}")
        
            print("\nAnalizando crecimiento de la función")
            intervalos = f.encontrar_crecimiento()
        
            if intervalos:
                print("\nLa función es creciente en los siguientes intervalos:")
                for intervalo in intervalos:
                    a, b = intervalo
                    print(f"({a}, {b})")
            else:
                print("\nNo se encontraron intervalos donde la función sea creciente.")
        
            graficar = input("\n¿Deseas graficar la función y su derivada? (s/n): ").lower()
            if graficar == 's':
               x_min = float(input("Límite inferior de x para graficar: "))
               x_max = float(input("Límite superior de x para graficar: "))
               f.graficar((x_min, x_max))
    
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == '__main__':
    main()