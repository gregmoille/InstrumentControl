import visa
import numpy as np
import time

class Keysight8164B():

    def __init__(self, **kwargs):
        self.address = kwargs.get('address', "GPIB0::20::INSTR")
        self._lbd = None
        self._power = None
        self._attenuation = None
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
                    word = 'OUTP:POW:UNIT DBM'
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
        self._lbd = self._instr.query('WAV?')
        self._lbd = float(self._lbd.strip())
        return self._lbd*1e9


    @lbd.setter
    @_isOpen
    def lbd(self, val):
        word = 'WAV {:.3f}E-9'.format(val)
        self._instr.write(word)

    @property
    @_isOpen
    def power(self):
        self._power = self._instr.query('POW?')
        self._power = float(self._power.strip())
        return self._power

    @power.setter
    @_isOpen
    def power(self, val):
        word = "POW {:.3f} DBM".format(val)
        self._instr.write(word)

    @property
    @_isOpen
    def attenuation(self):
        self._attenuation = self._instr.query('INP:ATT?')
        self._attenuation = float(self._attenuation.strip())
        return self._attenuation

    @attenuation.setter
    @_isOpen
    def attenuation(self,val):
        word = "INP:ATT {:.3f}".format(val)
        self._instr.write(word)

    @property
    @_isOpen
    def attenuation_lbd(self):
        self._attenuation = self._instr.query('INP:ATT?')
        self._attenuation = float(self._attenuation.strip())*1e9
        return self._attenuation

    @attenuation_lbd.setter
    @_isOpen
    def attenuation_lbd(self,val):
        word = "INP:WAV {:.3f}E-9".format(val)
        self._instr.write(word)

    @property
    @_isOpen
    def reset(self):
        return self._reset

    @reset.setter
    @_isOpen
    def reset(self, val):
        if val:
            word = "SOUR0:WAV:SWEEP 0"
            self._instr.write(word)
            time.sleep(0.5)
            # Changing unit to dBm
            word = 'OUTP:POW:UNIT DBM'
            self._instr.write(word)


    @property
    @_isOpen
    def track(self):
        return self._instr.query('OUTPut:TRACk?')

    @reset.setter
    @_isOpen
    def track(self, val):
        if val:
            word = "OUTPut:TRACk 1"
            self._instr.write(word)
        else:
            word = "OUTPut:TRACk 0"
            self._instr.write(word)
if __name__ == "__main__":
    lsr = Keysight8164B()
