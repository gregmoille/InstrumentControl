import visa
import numpy as np
import time

class Keysight7744A():


    def __init__(self, **kwargs):
            self.address = kwargs.get('address', "USB0::0x0957::0x3718::SG48101083::INSTR")
            self._lbd = None
            self._power = None
            self._reset = None
            self._connected = False


    def _isOpen(fun):
            def wrapper(*args, **kwargs):
                self_app = args[0]
                if self_app._connected:
                    out = fun(*args, **kwargs)
                    return out
            return wrapper 

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, val):
        if val: 
            try:
                rm = visa.ResourceManager()
                if self.address in rm.list_resources():
                    self._instr = rm.open_resource(self.address)
                    self._connected = True
                    word = 'SENS:POW:UNIT W'
                    self._instr.write(word)
            except Exception as e:
                self._connected = False
                print(e)
        else:
            self._inst.close()
            self._connected = False

    @property
    @_isOpen
    def lbd(self):

        self._lbd = self._instr.query('SENS:POW:WAV?')
        self._lbd = float(self._lbd.strip())
        return self._lbd*1e9


    @lbd.setter
    @_isOpen
    def lbd(self, val):
        word = 'SENS:POW:WAV {:.3f}E-9'.format(val)
        self._instr.write(word)

    @property
    @_isOpen
    def power(self):
        self._instr.write('INIT:CHAN1:CONT 1')
        self._power = self._instr.query('FETC:CHAN1:POW?')
        self._power = float(self._power.strip())*1e3
        return self._power

    @property
    @_isOpen
    def reset(self):
        return self._reset
    
    @reset.setter
    @_isOpen
    def reset(self, val):
        if val:
            word = "WAVE:SWEEP:STAT 0"
            self._instr.write(word)
            time.sleep(0.5)
            # Changing unit to dBm
            word = 'SENS:POW:UNIT W'
            self._instr.write(word)
