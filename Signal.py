#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

SAMPLE_FRECUENCY = 10000
#SAMPLE_FRECUENCY = 200

class Signal:
    y = []
    t = []

    def __init__(self):
        self.t = np.linspace(0, 1, SAMPLE_FRECUENCY, False, dtype=np.dtype(np.float64))
        
        #self.t = np.linspace(0, 10000, SAMPLE_FRECUENCY, False, dtype=np.dtype(np.int64))
        #self.t = np.linspace(0, 10, SAMPLE_FRECUENCY, False, dtype=np.dtype(np.float64))
        #print('***** Tiempos generados para la señal *****')
        #print(self.t)
        #self.t = np.linspace(0, 20, SAMPLE_FRECUENCY, False)

    def generate(self, frecuency, amplitude, sinoidal):
        if sinoidal:
            self.y = amplitude*np.sin(2*np.pi*frecuency*self.t)
            #print('***** Salida de la señal generada con la función seno *****')
            #print(self.y)
        else:
            self.y = amplitude*np.cos(2*np.pi*frecuency*self.t)
