import visa
import numpy as np

def KeysightLaser():

    def __init__(self, **kwargs):
        self.address = kwargs.get('address', "GPIB0::20::INSTR")
        self._lbd = None
        self._power = None
        self._attenuation = None
        self._reset = None

    @property
    def lbd(self):
        lbd = self.instr.querry('WAV?')
        return lbd*1e9

    ~@lbd.setter
    def lbd(self, val):
        self._lbd = 'WAV {:3.f}E-9'.format(val)
        self.instr.write(self._lbd)

    @property
    def power(self):
        self._power = self.instr.querry('POW?')
        return self._power

    @power.setter
    def power(self, val):
        word = "POW {:.3f}dBm".format(val)
        self.instr.write(word)

    @property
    def reset(self):
        return self._reset
    
    @reset.setter
    def reset(self, val):
        if val:
            word = "*RST"
            self.instr.write(word)
            # need to change everything in dBm

    @property
    def attenuation(self):
        self._attenuation = self.instr.querry('INP:ATT?')
        return self._attenuation
    
    @attenuation.setter
    def attenuation(self,val):
        word = "INP:ATT {:.3f}".format(val)
        self.instr.write(word)



