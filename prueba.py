#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random
from Signal import Signal
from Filter import Filter


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


#Constantes que me van a servir
MAX_FLOAT = float(1000000000.0)
MIN_FLOAT = float(-1000000000.0)
pos_inf = float('inf')     # positive infinity
neg_inf = float('-inf')    # negative infinity

fc = 500
amplitud = 10

S1 = Signal()
S1.generate(fc - 200, amplitud, sinoidal=True)

#Creo una solución
solucion = []
for x in range(18):
    solucion.append(random.uniform(-3, 3)) #Número al azar entre [-3, 3]

#Para algunos coeficientes voy a modificar su valor a 1, porque sino tira error
# y el auxiliar nos dio esta solución
solucion[3] = 1
solucion[9] = 1
solucion[15] = 1













#Inicializo el filtro 1
filtro1 = Filter(solucion)
#Obtengo la señal de salida del filtro 1
T1 = filtro1.filter(S1)

#Calcular la potencia media de T1
arreglo_absolutos1 = np.absolute(T1.y)
arreglo_cuadrados1 = list(map(lambda elemento: cuadrado(elemento), arreglo_absolutos1))
sumatoria1 = sumatoria(arreglo_cuadrados1)
print('sumatoria1:', sumatoria1)
P1 = (float(1) / float(2 * len(T1.y) - 1)) * float(sumatoria1)
print('P1: ', P1)
