import numpy as np
import os
try:
    import visa
except:
    print('\033[93m' + '-'*10 + 'EXCEPTION:')
    print(__file__)
    print(e)
    print('-'*10 + 'end exception' + '\033[0m')
import time
import re


class Piezo(object):
    def __init__(self, **kwargs):
        address = kwargs.get('address', "ASRL3::INSTR")


        rm = visa.ResourceManager()
        self.instr = rm.open_resource(address)
        self.instr.timeout = 1550

        # empty the buffer
        self._debug = False
        self._empty_buff()
        self._axis = 'x'
       


    def Query(self, word):
        return self.instr.query(word)

    def _empty_buff(self):
        cdt = '_'
        while not cdt == '!':
            word = self.instr.query('')
            try:
                cdt = word.strip()[-1]
                if self._debug:
                    print('coucou')
            except:
                cdt = word.strip()
            if self._debug:
                print(cdt)

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
        self.instr.query(word)
        while True:
            if self._debug:
                print('loop')
            V = self.instr.query(word)
            if self._debug:
                print(V)
            try:
                V = re.findall(r'\d+\.\d+', V)
                V = float(V[0])
                break
            except:
                pass

        self._empty_buff()
        return V

    @V.setter
    def V(self, V):
        axis = self._axis.upper()
        word = axis  + 'voltage='
        self.instr.query(word + str(V))
        self._empty_buff()

if __name__ == '__main__':
    pzt = Piezo()

    