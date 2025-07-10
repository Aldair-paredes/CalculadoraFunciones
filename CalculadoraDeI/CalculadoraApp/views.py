from django.shortcuts import render
from .explicita import calcular_funcion_explicita 
import io, base64
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np



def pagprincipal(request):
    return render(request, 'pagprincipal.html')

def temas (request):
    return render(request, 'temas.html')

def tema_funciones (request):
    return render(request, 'tema_funciones.html')



def calculadora_explicita(request):

    result = None
    error = None
    function_input = ""
    operation_select = ""

   
    if request.method == 'POST':
        function_input = request.POST.get('function_input', '').strip()
        operation_select = request.POST.get('operation_select', '').strip()
        variable_input = request.POST.get('variable_input', '').strip()
        limit_point_input = request.POST.get('limit_point_input', '').strip()
        evaluate_values_input = request.POST.get('evaluate_values_input', '').strip()

    
        kwargs_para_funcion = {}
        if operation_select in ['derivar', 'limite', 'resolver']:
            kwargs_para_funcion['variable_derivacion'] = variable_input 
            kwargs_para_funcion['variable_integracion'] = variable_input
            kwargs_para_funcion['variable_limite'] = variable_input
            kwargs_para_funcion['variable_resolver'] = variable_input
        
        if operation_select == 'limite':
            kwargs_para_funcion['punto_limite'] = limit_point_input
        
        if operation_select == 'evaluar':
            kwargs_para_funcion['valores_evaluacion_str'] = evaluate_values_input

        
        result, error = calcular_funcion_explicita(function_input, operation_select, **kwargs_para_funcion)

    
    context = {
        'function_input': function_input,
        'operation_select': operation_select,
        'result': result,
        'error': error,
    }
    return render(request, 'funcion_explicita.html', context)
#Decreciente Agustin

def analizarfuncionview(request):
    if request.method == 'POST':
        try:
            # Recoger los datos del formulario
            funcion = request.POST.get('funcion')
            intervalo_min = float(request.POST.get('intervalo_min'))
            intervalo_max = float(request.POST.get('intervalo_max'))
            punto_limite = float(request.POST.get('punto_limite'))
            graficar = request.POST.get('graficar') == 's'

            x = sp.symbols('x')
            f = sp.sympify(funcion)

            resultado = f"\nFunción original: f(x) = {f}\n"

            # Derivar
            derivada = sp.diff(f, x)
            resultado += f"Derivada: f'(x) = {derivada}\n"

            # Simplificar
            simplificada = sp.simplify(f)
            resultado += f"Función simplificada: {simplificada}\n"

            # Resolver f(x)=0
            soluciones = sp.solve(f, x)
            resultado += f"Soluciones a f(x)=0: {soluciones if soluciones else 'No hay soluciones reales encontradas.'}\n"

            # Calcular límite
            limite = sp.limit(f, x, punto_limite)
            resultado += f"Límite de f(x) cuando x → {punto_limite}: {limite}\n"

            # Analizar si es decreciente
            puntos = np.linspace(intervalo_min, intervalo_max, 100)
            derivadas_numericas = [float(derivada.subs(x, punto)) for punto in puntos]
            decreciente = all(valor <= 0 for valor in derivadas_numericas)

            if decreciente:
                resultado += "\nConclusión: La función es decreciente en todo el intervalo."
            else:
                resultado += "\nConclusión: La función no es completamente decreciente en el intervalo."

            grafico_url = None

            # Graficar si el usuario lo pidió
            if graficar:
                f_lambd = sp.lambdify(x, f, modules=['numpy'])
                deriv_lambd = sp.lambdify(x, derivada, modules=['numpy'])
                y_f = f_lambd(puntos)
                y_df = deriv_lambd(puntos)

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

                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                grafico_base64 = base64.b64encode(image_png).decode('utf-8')
                grafico_url = f"data:image/png;base64,{grafico_base64}"
                plt.close()

            return render(request, 'Decreciente.html', {
                'resultado': resultado,
                'grafico_url': grafico_url
            })

        except Exception as e:
            return render(request, 'Decreciente.html', {
                'error': f"Error al analizar la función: {str(e)}"
            })

    return render(request, 'Decreciente.html')

#Inyectiva Agustin

from django.shortcuts import render
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings

def funcion_inyectiva(request):
    resultado = {}
    
    if request.method == 'POST':
        expresion = request.POST.get('funcion')
        operacion = request.POST.get('operacion')
        valor_x = request.POST.get('valor_x')

        x = sp.Symbol('x')
        try:
            funcion = sp.sympify(expresion)
        except:
            resultado = {'expresion': expresion, 'operacion': operacion, 'valor': 'Error: función inválida'}
            return render(request, 'inyectiva.html', {'resultado': resultado})

        valor = None

        try:
            if operacion == 'derivar':
                valor = sp.diff(funcion, x)
            elif operacion == 'evaluar':
                valor = funcion.subs(x, float(valor_x))
            elif operacion == 'limite':
                valor = sp.limit(funcion, x, float(valor_x))
            elif operacion == 'simplificar':
                valor = sp.simplify(funcion)
            elif operacion == 'resolver':
                valor = sp.solve(funcion, x)
        except Exception as e:
            valor = f'Error al calcular: {str(e)}'

        resultado = {
            'expresion': expresion,
            'operacion': operacion,
            'valor': valor
        }

    return render(request, 'inyectiva.html', {'resultado': resultado})
