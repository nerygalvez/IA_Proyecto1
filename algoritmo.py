#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np
from nodo import Nodo
from Signal import Signal
from Filter import Filter

#CONSTANTES DEL ALGORITMO
maximo_generaciones = 2000 #Número máximo de generaciones que va a tener el algoritmo
tamano_poblacion = 20
tamano_padres_seleccionados = 10 #Número de padres a seleccionar entre los mejores padres
tamano_individuos = 18 #Porque son 18 coeficientes de un filtro
fitness_esperado = 6.3551731312595228e+303 #Si el 70% de la población tiene un valor fitness mayor a 'fitness_esperado' detengo el algoritmo
amplitud = 10 #Amplitud con la que se va a generar las señales



#CONSTANTES PARA EL CÁLCULO DE LA POTENCIA MEDIA
MAX_FLOAT = float(1000000000.0)
MIN_FLOAT = float(-1000000000.0)
pos_inf = float('inf')     # positive infinity
neg_inf = float('-inf')    # negative infinity





#FUNCIONES PARA EL CÁLCULO DE LA POTENCIA MEDIA
def verificarNumero(valor):
    return (MAX_FLOAT if valor == pos_inf else MIN_FLOAT if valor == neg_inf else 0 if str(valor) == 'nan' else valor)

def cuadrado(valor):
    #np.seterr(over='raise')
    np.seterr(all = 'raise')
    try:
        #Trato de reemplazar los inf, -inf y nan de una vez aquí
        valor = verificarNumero(valor)
        
        valor = valor **2 #Elevo al cuadrado
        #Vuelvo a verificar si el número no dio inf, -inf o nan
        return verificarNumero(valor)
    except :
        #Aquí debería de llegar al sacar el cuadrado de un número muy grande
        #Retorno el máximo positivo porque cualquier número al cuadrado es positivo
        return MAX_FLOAT #Si dio exception de overflow retorno el valor máximo

def sumatoria(arreglo):
    try:
        np.seterr(all = 'raise')
        suma = sum(arreglo)
        return verificarNumero(suma)
    except:
        #Aquí voy a retornar el valor máximo positivo, pero creo que a veces podría ser negativo
        #aunque no sé cómo ver si es negativa o positiva la suma
        return MAX_FLOAT #Si dio exception de overflow retorno el valor máximo






class Algoritmo:
    


    """
    *   @fc = frecuencia de corte
    *   @tfiltro = tipo de filtro
    """
    def __init__(self, fc, tfiltro):
        self.fc = fc
        self.tfiltro = tfiltro

        #Inicializo una señal S1
        self.S1 = Signal()

        #Inicializo una señal S2
        self.S2 = Signal()
        
    """
    *   Función que va a generar las señales con las que se va a calcular el valor fitness
    """
    def generarSenales(self):
        #Genero la señal S1
        self.S1.generate(self.fc - 200, amplitud, sinoidal=True)

        #Genero la señal S2
        self.S2.generate(self.fc + 200, amplitud, sinoidal=True)
        

    """
    *   Función que crea la población
    """
    def inicializarPoblacion(self):
        poblacion = []

        #Voy a crear una población de 20 individuos
        for solucion in range(tamano_poblacion):
            individuo = Nodo()
            for x in range(tamano_individuos):
                individuo.solucion.append(random.uniform(-3, 3)) #Número al azar entre [-3, 3]
            
            #Para algunos coeficientes voy a modificar su valor a 1, porque sino tira error
            # y el auxiliar nos dio esta solución
            individuo.solucion[3] = 1
            individuo.solucion[9] = 1
            individuo.solucion[15] = 1
            poblacion.append(individuo) #Agrego un nuevo individuo a la población
            #print('Individuo ', individuo.solucion)
    
        return poblacion #Retorno la población ya creada


    """
    *   Función que verifica si el algoritmo ya llegó a su fin
    """
    def verificarCriterio(self, poblacion, generacion):

        #Si ya llegó al máximo de generaciones lo detengo
        if generacion >= maximo_generaciones:
            #Calculo una última vez el valor fitness de los individuos
            for individuo in poblacion:
                individuo.fitness = self.evaluarFitness(individuo.solucion)
            
            return True
        
        #Voy a ver a qué valores llega para ver el mejor fitness
        #return None


        # Veo si el 70% de la población tiene un valor fitness mayor a 'fitness_esperado'
        # Busco a los mayores porque mientras más alto es el valor fitness mejor es la solución
        contador = 0
        for individuo in poblacion:
            #Actualizo el valor fitness del individuo
            individuo.fitness = self.evaluarFitness(individuo.solucion)
            contador += 1 if individuo.fitness > fitness_esperado else 0
        
        return True if contador >= len(poblacion) * 0.7 else None


    """
    *   Función que evalúa qué tan buena es una solución, devuelve el valor fitness de la solución
    *
    *   @solucion = arreglo con los coeficientes del filtro del cual se quiere obtener el valor fitness
    """
    def evaluarFitness(self, solucion):
        
        #Desde el inicio generé la señal S1
        #Filtro la señal S1 con los coeficientes de la solución que quiero evaluar
        #Inicializo el filtro 1
        filtro1 = Filter(solucion)
        #Obtengo la señal de salida del filtro 1
        T1 = filtro1.filter(self.S1)

        #Desde el principio generé la señal S2
        #Filtro la señal S2 con los coeficientes de la solución que quiero evaluar
        #Inicializo el filtro 2
        filtro2 = Filter(solucion)
        #Obtengo la señal de salida del filtro 2
        T2 = filtro2.filter(self.S2)

        #Calcular la potencia media de T1
        arreglo_absolutos1 = np.absolute(T1.y)
        arreglo_cuadrados1 = list(map(lambda elemento: cuadrado(elemento), arreglo_absolutos1))
        sumatoria1 = sumatoria(arreglo_cuadrados1)
        P1 = (float(1) / float(2 * len(T1.y) - 1)) * float(sumatoria1)
        #print('sumatoria1:', sumatoria1)
        #print('P1: ', P1)
        

        #Calcular la potencia media de T2
        arreglo_absolutos2 = np.absolute(T2.y)
        arreglo_cuadrados2 = list(map(lambda elemento: cuadrado(elemento), arreglo_absolutos2))
        sumatoria2 = sumatoria(arreglo_cuadrados2)
        P2 = (float(1) / float(2 * len(T2.y) - 1)) * float(sumatoria2)
        #print('sumatoria2:', sumatoria2)
        #print('P2: ', P2)

        if self.tfiltro == "pb": #Si el filtro es pasa bajos
            fitness = P1 - P2
            return fitness
        
        #De lo contrario el filtro es pasa altos
        fitness = P2 - P1
        return fitness


    """
    *   Función que verifica si el algoritmo ya llegó a su fin
    """
    def seleccionarPadres(self, poblacion):
        #Se elige a los mejores padres, quienes tengan un valor fitness más alto
        padres = sorted(poblacion, key=lambda item: item.fitness, reverse=True)[:tamano_padres_seleccionados] #Los ordena de mayor a menor
        return padres #Regreso solo a los padres seleccionados


    """
    *   Función que toma dos soluciones padres y las une para formar una nueva solución hijo
    """
    def cruzar(self, padre1, padre2):
        hijo = []
        for indice in xrange(0, len(padre1)):
            numero = random.uniform(0, 1) #Número al azar entre [0, 1]
            if numero > 0.5: #Se usa el valor de padre1
                hijo.append(padre1[indice])
            else: #Se usa el valor de padre2
                hijo.append(padre2[indice])

        return hijo #Retorno al hijo ya cruzado


    """
    *   Función que toma una solución y calcula si una posición muta o no
    """
    def mutar(self, solucion):
        numero = random.uniform(-0.5, 0.5) #Número al azar entre [-0.5, 0.5]
        posicion = random.randint(0, len(solucion) - 1) #Incluye ambos valores, por eso le quito uno al tamaño
        
        #En la mutación no se puede alterar el valor de los coeficientes en las posiciones 3, 9 y 15, estas siempre tienen valor 1
        while posicion == 3 or posicion == 9 or posicion == 15:
            posicion = random.randint(0, len(solucion) - 1) #Incluye ambos valores, por eso le quito uno al tamaño
        
        solucion[posicion] = solucion[posicion] + numero
        return solucion #Retorno la misma solución, solo que ahora mutó


    """
    *   Función que toma a los mejores padres y genera nuevos hijos
    *   la cantidad de hijos generados está calculado de la siguiente manera:
    *   nuevos_generados = tamano_poblacion - tamano_padres_seleccionados
    """
    def emparejar(self, padres):
        nuevos_generados = tamano_poblacion - tamano_padres_seleccionados

        #Genero la cantidad de nuevos individuos dado por el valor de 'nuevos_generados'
        for x in range(nuevos_generados):
            hijo = Nodo()
            #hijo.solucion = cruzar(padres[random.randint(0, 4)].solucion, padres[random.randint(5, 9)].solucion)
            #Para cruzar voy a tomar [0 , (cantidadPadres / 2 - 1)] y [cantidadPadres / 2, cantidadPadres - 1]
            hijo.solucion = self.cruzar(padres[random.randint(0, len(padres) / 2 - 1)].solucion, padres[random.randint(len(padres) / 2, len(padres) - 1)].solucion)
            hijo.solucion = self.mutar(hijo.solucion)
            padres.append(hijo) #Agrego el nuevo hijo a la lista de padres

        return padres #Retorno la nueva población










    """
    *   Método para imprimir los datos de una población
    """
    def imprimirPoblacion(self, poblacion):
        for individuo in poblacion:
            print('Fitness: ', individuo.fitness)




    """
    *   Método que ejecutará el algoritmo genético para obtener
    *   los coeficientes del filtro
    """
    def ejecutar(self):
        #np.seterr(over='raise')
        print("Algoritmo corriendo")

        generacion = 0
        poblacion = self.inicializarPoblacion()
        fin = self.verificarCriterio(poblacion, generacion)
        while(fin == None):
            padres = self.seleccionarPadres(poblacion)
            poblacion = self.emparejar(padres)
            generacion += 1 #Lo pongo aquí porque en teoría ya se creó una nueva generación
            fin = self.verificarCriterio(poblacion, generacion)
            #generacion += 1

        print('Cantidad de generaciones:', generacion)
        self.imprimirPoblacion(poblacion)

        #Obtengo la mejor solución, este va a ser el arreglo de coeficientes para el filtro
        coeficientes = sorted(poblacion, key=lambda item: item.fitness, reverse=True)[:1] #Los ordena de mayor a menor


        #Devuelvo el arreglo de coeficientes del filtro
        #coeficientes = [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        return coeficientes[0].solucion