import sympy as sp
import numpy as np
import matplotlib.pyplot as plt 
import io 
import base64 

class FuncionImplicita:
    def __init__(self, expresion_str, variable_x='x', variable_y='y'):
        self.x = sp.symbols(variable_x)
        self.y = sp.symbols(variable_y)

        try:
            expresion_str = expresion_str.replace('pi', 'sympy.pi').replace('e', 'sympy.E')
            self.expresion = sp.sympify(expresion_str)
            self.expresion_str = expresion_str
        except (sp.SympifyError, TypeError) as e:
            raise ValueError(f'Expresión inválida: "{expresion_str}". Asegúrate de usar operadores válidos (ej. ** para potencia) y nombres de variables (x, y). Detalle: {e}')

    def evaluar(self, x_val_str, y_val_str):
        try:
            sustituciones = {}
            if x_val_str:
                x_val = sp.sympify(x_val_str)
                sustituciones[self.x] = x_val
            if y_val_str:
                y_val = sp.sympify(y_val_str)
                sustituciones[self.y] = y_val
            
            resultado_simbolico = self.expresion.subs(sustituciones)
            
            if isinstance(resultado_simbolico, (sp.Float, float)):
                return f"{float(resultado_simbolico):.5f}"
            return str(sp.simplify(resultado_simbolico))
        except (sp.SympifyError, ValueError, TypeError) as e:
            raise ValueError(f'Error al evaluar la expresión con los valores proporcionados. Asegúrate de que los valores sean numéricos o expresiones válidas. Detalle: {e}')

    def derivada(self, respecto_a, orden_str='1'):
        try:
            orden = int(orden_str) if orden_str else 1
            if orden < 1:
                raise ValueError("El orden de la derivada debe ser al menos 1.")

            if respecto_a == 'y':
                var_diff = self.y
            elif respecto_a == 'x':
                var_diff = self.x
            else:
                raise ValueError("La variable para derivar debe ser 'x' o 'y'.")
            
            if self.x in self.expresion.free_symbols and self.y in self.expresion.free_symbols:
                if respecto_a == 'x':
                    derivada_parcial_x = sp.diff(self.expresion, self.x)
                    derivada_parcial_y = sp.diff(self.expresion, self.y)
                    
                    if derivada_parcial_y == 0:
                        raise ValueError("No se puede calcular dy/dx implícitamente, dF/dy es cero.")
                    
                    if orden == 1:
                        resultado_simbolico = -sp.simplify(derivada_parcial_x / derivada_parcial_y)
                        return f"dy/dx = {resultado_simbolico}"
                    else: 
                        raise ValueError("Las derivadas implícitas de orden superior no están implementadas para esta calculadora.")
                        
                elif respecto_a == 'y': 
                    derivada_parcial_x = sp.diff(self.expresion, self.x)
                    derivada_parcial_y = sp.diff(self.expresion, self.y)
                    
                    if derivada_parcial_x == 0:
                        raise ValueError("No se puede calcular dx/dy implícitamente, dF/dx es cero.")
                    
                    if orden == 1:
                        resultado_simbolico = -sp.simplify(derivada_parcial_y / derivada_parcial_x)
                        return f"dx/dy = {resultado_simbolico}"
                    else:
                        raise ValueError("Las derivadas implícitas de orden superior no están implementadas para esta calculadora.")
            else:
                derivada_simple = sp.diff(self.expresion, var_diff, orden)
                return str(derivada_simple)
        except (ValueError, TypeError, sp.SympifyError) as e:
            raise ValueError(f'Error al calcular la derivada: {e}')

    def limite(self, variable, punto_str, direccion=''):
        try:
            var = self.x if variable == 'x' else self.y
            
            if punto_str.lower() in ['oo', 'infinito']:
                punto_eval = sp.oo
            elif punto_str.lower() in ['-oo', '-infinito']:
                punto_eval = -sp.oo
            else:
                punto_eval = sp.sympify(punto_str)

            lim_dir = None
            if direccion == '+':
                lim_dir = '+'
            elif direccion == '-':
                lim_dir = '-'

            if lim_dir:
                lim = sp.limit(self.expresion, var, punto_eval, dir=lim_dir)
            else:
                lim = sp.limit(self.expresion, var, punto_eval)
            
            return str(lim)
        except (sp.SympifyError, ValueError, TypeError) as e:
            raise ValueError(f'Error al calcular el límite. Asegúrate de que el punto y la dirección sean válidos. Detalle: {e}')

    def simplificar(self):
        try:
            expr_simplificada = sp.simplify(self.expresion)
            return str(expr_simplificada)
        except (ValueError, TypeError, sp.SympifyError) as e:
            raise ValueError(f'Error al simplificar la expresión: {e}')

    def resolver(self, respecto_a, valor_sustitucion_str=None):
        try:
            target_var = self.y if respecto_a == 'y' else self.x
            other_var = self.x if respecto_a == 'y' else self.y
            
            expr_to_solve = self.expresion
            
            if valor_sustitucion_str:
                parts = valor_sustitucion_str.split('=')
                if len(parts) == 2:
                    sub_var_str = parts[0].strip()
                    sub_val_str = parts[1].strip()
                    sub_var_sym = sp.symbols(sub_var_str)
                    sub_val_sym = sp.sympify(sub_val_str)

                    if sub_var_sym == target_var:
                        raise ValueError(f"No puedes sustituir la variable '{sub_var_str}' si es la que deseas despejar.")
                    
                    if sub_var_sym == other_var:
                        expr_to_solve = expr_to_solve.subs(other_var, sub_val_sym)
                    else:
                        raise ValueError(f"La variable de sustitución '{sub_var_str}' no es reconocida o es la variable a despejar.")
                elif len(parts) == 1:
                    sub_val_sym = sp.sympify(valor_sustitucion_str)
                    expr_to_solve = expr_to_solve.subs(other_var, sub_val_sym)
                else:
                    raise ValueError("Formato de sustitución inválido. Usa 'variable=valor' (ej: 'x=2') o solo el valor (ej: '2').")

            soluciones = sp.solve(expr_to_solve, target_var)
            
            soluciones_str = []
            for sol in soluciones:
                try:
                    if sol.is_number:
                        soluciones_str.append(f"{float(sol):.5f}")
                    else:
                        soluciones_str.append(str(sp.simplify(sol)))
                except Exception:
                    soluciones_str.append(str(sp.simplify(sol)))
            
            if not soluciones_str:
                return "No se encontraron soluciones."
            
            if len(soluciones_str) > 1:
                return [f"{respecto_a} = {sol}" for sol in soluciones_str]
            else:
                return f"{respecto_a} = {soluciones_str[0]}"

        except (sp.SympifyError, ValueError, TypeError) as e:
            raise ValueError(f'Error al resolver la expresión: {e}')

    def graficar(self, rango_x=(-5, 5), rango_y=(-5, 5), puntos=200):
       
        try:
            funcion_numerica = sp.lambdify((self.x, self.y), self.expresion, modules=['numpy'])

            x_vals = np.linspace(rango_x[0], rango_x[1], puntos)
            y_vals = np.linspace(rango_y[0], rango_y[1], puntos)
            X, Y = np.meshgrid(x_vals, y_vals)

            Z = funcion_numerica(X, Y)

            fig, ax = plt.subplots(figsize=(8, 6)) 
            
            ax.contour(X, Y, Z, levels=[0], colors='blue', linewidths=2)
            
            ax.set_title(f'Gráfica de {sp.latex(self.expresion)} = 0') 
            ax.set_xlabel(f'${sp.latex(self.x)}$') 
            ax.set_ylabel(f'${sp.latex(self.y)}$')
            ax.grid(True, linestyle='--', alpha=0.7) 

            ax.axhline(0, color='gray', linewidth=0.8)
            ax.axvline(0, color='gray', linewidth=0.8)

            ax.set_aspect('equal', adjustable='box')

            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0) 

            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig) 
            
            return image_base64

        except Exception as e:
            plt.close('all') 
            raise ValueError(f'Error al generar la gráfica: {e}')