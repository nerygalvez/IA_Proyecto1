#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,render_template,request,jsonify,redirect, abort, send_from_directory, url_for
import csv

from algoritmo import Algoritmo 

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
    print('T1')

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
    f = request.files['archivo1'] 
    fstring = f.read().decode("utf-8-sig").encode("utf-8")
    fieldnames = ['valor'] #Le voy a poner un valor que yo conozca a la columna porque no se definió el nombre para el archivo de entrada
    diccionario_csv = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), fieldnames=fieldnames, skipinitialspace=True)]
    
    #Elimino el primer elemento porque agrega el nombre de columna que yo le puse (fieldnames)
    diccionario_csv.pop(0)
    
    #for x in diccionario_csv:
        ##print(x['valor'])
        #print(x)


    #Obtengo los coeficientes del filtro que voy a usar para filtrar la señal
    arreglo_coeficientes = request.form['arreglo_coeficientes']
    #print('arreglo_coeficientes', arreglo_coeficientes)

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