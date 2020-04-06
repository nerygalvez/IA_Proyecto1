#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scipy.signal as sig

from Signal import Signal
class Filter:

    values = []

    def __init__(self, constants):
        if len(constants) == 18:
            self.values = [constants[:6], constants[6:12], constants[12:18]]

    def filter(self, input):
        output = Signal()
        output.y = sig.sosfilt(self.values, input.y)

        #print('***** Salida del filtro *****')
        #print(output.y)

        return output
