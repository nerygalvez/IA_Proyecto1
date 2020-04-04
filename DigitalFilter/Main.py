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
#individuo1 = [0.5999402, -0.5999402, 0, 1, -0.7265425, 0, 1, -2, 1, 1, -1.52169043, 0.6, 1, -2, 1, 1, -1.73631017, 0.82566455]

individuo1 = [-1.0680269827643445, -0.5713375209620128, -2.5686810550062686, 1, -1.507492099868706, 1.1328639399494786, -2.0312789297904277, 2.2819167893422474, 1.0782562420903563, 1, -2.406622049318159, 2.8184691203296985, 1.1009934668113424, 2.937768404798515, -1.2879034426159903, 1, 1.0779804598027694, 0.26138695967438075]

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

