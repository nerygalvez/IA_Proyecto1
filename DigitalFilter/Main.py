#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DTS.Signal import Signal
from DTS.Filter import Filter
import matplotlib.pyplot as chart

# Se inicializa la señal
input = Signal()

# Se genera una señal de 300 Hz
# El primer parametro es la frecuencia
# El segundo parametro es la amplitud
# El tercer parametro indica si sera una funcion Seno o Coseno
input.generate(300, 10, sinoidal=True)

# Coeficientes del filtro
individuo1 = [0.5999402, -0.5999402, 0, 1, -0.7265425, 0, 1, -2, 1, 1, -1.52169043, 0.6, 1, -2, 1, 1, -1.73631017, 0.82566455]

# Se instancia el filtro
filtro = Filter(individuo1)

# Se obtiene la señal de salida del filtro
output = filtro.filter(input)

# Generacion de grafica

fig, (ax1, ax2) = chart.subplots(2, 1, sharex=True)
ax1.plot(input.t, input.y)
ax1.set_title('Entrada del filtro')
ax1.axis([0, 1, -10, 10])
ax2.plot(output.t, output.y)
ax2.set_title('Salida del filtro')
ax2.axis([0, 1, -10, 10])
ax2.set_xlabel('Tiempo [segundos]')
chart.tight_layout()
chart.show()

