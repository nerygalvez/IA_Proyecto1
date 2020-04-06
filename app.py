#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,render_template,request,jsonify,redirect, abort, send_from_directory, url_for
import csv
import matplotlib.pyplot as chart

from algoritmo import Algoritmo
from Filter import Filter
from Signal import Signal


app = Flask(__name__)

"""
*   Función para cargar la página principal de la aplicación
"""
@app.route('/')
def index():
    return render_template('index.html')


"""
*   Ruta para ejecutar la generación del filtro
"""
@app.route('/generarFiltro', methods=["POST"])
def generarFiltro():

    #Obtengo el valor de los parámetros
    frecuencia = request.form['frecuencia']
    tipoFiltro = request.form['tipoFiltro']
    print('frecuencia', frecuencia)
    print('tipoFiltro', tipoFiltro)

    #Inicializo un algoritmo
    algoritmo = Algoritmo(int(frecuencia), tipoFiltro)
    
    #genero las señales con las que se calcula el valor fitness
    algoritmo.generarSenales()
    #print("******************************************")
    #print(algoritmo.S1.y)
    #print("******************************************")

    #Obtengo el arreglo de coeficientes del filtro
    coeficientes = algoritmo.ejecutar()

    #Devuelvo el arreglo con los coeficientes del filtro
    return jsonify(
                    coeficientes=coeficientes,
                   )




"""
*   Ruta para ejecutar la función de filtrar
"""
@app.route('/filtrar', methods=["POST"])
def filtrar():

    #Obtengo el archivo que se cargó
    #Los archivos tienen que tener nombre en la columna obligatoriamente para que me funcione
    f = request.files['archivo1'] 
    fstring = f.read().decode("utf-8-sig").encode("utf-8")
    fieldnames = ['valor'] #Le voy a poner un valor que yo conozca a la columna porque no se definió el nombre para el archivo de entrada
    diccionario_csv = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), fieldnames=fieldnames, skipinitialspace=True)]
    
    #Elimino el primer elemento porque agrega el nombre de columna que yo le puse (fieldnames)
    diccionario_csv.pop(0)
    
    #Creo el arreglo de la señal de entrada para el filtro
    arreglo_senal_entrada = []
    for x in diccionario_csv:
        ##print(x['valor'])
        #print(x)
        arreglo_senal_entrada.append(float(x['valor']))


    #Creo la señal
    senal = Signal()
    senal.y = arreglo_senal_entrada


    #Obtengo los coeficientes del filtro que voy a usar para filtrar la señal
    arreglo_coeficientes = []
    arreglo_coeficientes.append(float(request.form['b0']))
    arreglo_coeficientes.append(float(request.form['b1']))
    arreglo_coeficientes.append(float(request.form['b2']))
    arreglo_coeficientes.append(float(request.form['b3']))
    arreglo_coeficientes.append(float(request.form['b4']))
    arreglo_coeficientes.append(float(request.form['b5']))
    arreglo_coeficientes.append(float(request.form['b6']))
    arreglo_coeficientes.append(float(request.form['b7']))
    arreglo_coeficientes.append(float(request.form['b8']))
    arreglo_coeficientes.append(float(request.form['b9']))
    arreglo_coeficientes.append(float(request.form['b10']))
    arreglo_coeficientes.append(float(request.form['b11']))
    arreglo_coeficientes.append(float(request.form['b12']))
    arreglo_coeficientes.append(float(request.form['b13']))
    arreglo_coeficientes.append(float(request.form['b14']))
    arreglo_coeficientes.append(float(request.form['b15']))
    arreglo_coeficientes.append(float(request.form['b16']))
    arreglo_coeficientes.append(float(request.form['b17']))
    print("***** COEFICIENTES *****")
    print(arreglo_coeficientes)


    #Creo el filtro con los coeficientes del filtro
    #arreglo_coeficientes = [0.5999402, -0.5999402, 0, 1, -0.7265425, 0, 1, -2, 1, 1, -1.52169043, 0.6, 1, -2, 1, 1, -1.73631017, 0.82566455]
    #print(arreglo_coeficientes)

    filtro = Filter(arreglo_coeficientes)

    #Se filtra la señal de entrada
    salida = filtro.filter(senal)

    #Genero las gráficas
    fig, (ax1, ax2) = chart.subplots(2, 1, sharex=True)
    #ax1.plot(input.t, input.y)
    #ax1.plot([], senal.y)
    ax1.plot(senal.t, senal.y)
    ax1.set_title('Entrada del filtro')
    ax1.axis([0, 1, -10, 10])

    ax2.plot(salida.t, salida.y)
    ax2.set_title('Salida del filtro')
    ax2.axis([0, 1, -10, 10])
    ax2.set_xlabel('Tiempo [segundos]')

    chart.tight_layout()
    #chart.show()
    chart.savefig("salida.png", transparent=True)
    #plt.savefig("Ejemplo1.jpg")
    



    #Devuelvo una respuesta cualquiera
    return jsonify(
                    estado=200,
                    mensaje='La operación de filtrar se realizó con éxito',
                   )





"""
*   Ruta para ejecutar el servidor de Flask
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)