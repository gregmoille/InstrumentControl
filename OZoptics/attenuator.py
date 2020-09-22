import visa
import numpy as np
import re

class Attenuator():
    '''
    Class to controll the DA-100 OZ optics digital attenuator.
    The serial chip is a Silicon Industry CP2102 that need the driver
    to be installed in order to use it, see:
    https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers


    - initilising the class:
        att = Attenuator(address=<add>) , where address is the com address of the attenuator

    - propetries:
        - self.connected
        - self.wavelength
        - self.attenuation
        - self.insertion_losses

    '''

    __author__ = "Gregory Moille"
    __copyright__ = "Copyright 2019, NIST"
    __credits__ = ["Gregory Moille",
                   "Xiyuan Lu",
                   "Kartik Srinivasan"]
    __license__ = "GPL"
    __version__ = "1.0.0"
    __maintainer__ = "Gregory Moille"
    __email__ = "gmoille@umd.edu"
    __status__ = "Development"

    def __init__(self, **kwargs):
        self._address = kwargs.get('address', None)
        self._connected = False
        self._lbd = None
        self._att = None
        self._il = None
        self._instr = None

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, val):
        if type(val) == bool:
            if self._connected:
                if not val:
                    self._instr.clear()
                    self._instr.close()
            else:
                if val:
                    rm = visa.ResourceManager()
                    self._instr = rm.open_resource('ASRL3::INSTR')
                    self._instr.clear()
    @property
    def wavelength(self):
        word = 'W?'
        self._instr.clear()
        self._instr.query(word)
        _val = self._instr.read()
        self._instr.read()
        self._lbd = float(re.findall(r"[-+]?\d*\.\d+|\d+", _val)[0])
        return self._lbd
    @wavelength.setter
    def wavelength(self, val):
        if type(val) == float or type(val) == int:
            word = 'W{:.0f}'.format(val)
            self._instr.write(word)

    @property
    def attenuation(self):
        word = 'A?'
        self._instr.clear()
        self._instr.query(word)
        _val = self._instr.read()
        self._instr.read()
        self._att = float(re.findall(r"[-+]?\d*\.\d+|\d+", _val)[0])
        return self._att

    @attenuation.setter
    def attenuation(self, val):
        if type(val) == float or type(val) == int:
            word = 'A{:.2f}'.format(val)
            self._instr.write(word)

    @property
    def insertion_losses(self):
        return self._lbd
