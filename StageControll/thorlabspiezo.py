import numpy as np
import os
import visa
import time
import re


class Piezo(object):
    def __init__(self, **kwargs):
        address = kwargs.get('address', None)


        rm = visa.ResourceManager()
        self.instr = rm.open_resource(address)

        # empty the buffer
        word = ''
        while not word.strip() == '!':
            word = self.instr.query('')


    def SetVoltage(self,V, axis):
        # empty the buffer in case
        word = axis  + 'voltage='

        dummy = self.instr.query(word + str(V))
        dummy = self.instr.query('')
        dummy = self.instr.query('')
        dummy = self.instr.query('')
        dummy = self.instr.query('')



    def GetVoltage(self,axis):
        word = axis  + 'voltage?'
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