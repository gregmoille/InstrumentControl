import numpy as np
import os
# import visa
import time
import re


class Piezo(object):
    def __init__(self, **kwargs):
        address = kwargs.get('address', None)


        rm = visa.ResourceManager()
        self.instr = rm.open_resource(address)

        # empty the buffer
        self._empty_buff()
        self._axis = 'x'

    def Query(self, word):
        return self.instr.query(word)

    def _empty_buff(self):
        word = ''
        while not word.strip() == '!':
            word = self.Query('')


    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, value):
        if value.lower() in ['x', 'y', 'z']:
            self._axis = value.lower()

    @property
    def V(self):
        word = self._axis.upper()  + 'voltage?'
        dummy = self.instr.query(word)
        while True:
            V = self.instr.query('')
            try:
                V = re.findall(r'\d+\.\d+', V)
                V = float(V[0])
                break
            except:
                pass

        return V

    @V.setter
    def V(self, V):
        axis = self._axis.upper()
        V = val
        word = axis  + 'voltage='
        self.instr.query(word + str(V))
        self._empty_buff()


    