

import numpy as np
import os
import sys
import time
import platform
import pyvisa.errors as VisaError
from visa import constants
path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)
from pyDecorators import InOut, ChangeState, Catch

try:
    import visa
except Exception as e:
    print('\033[93m' + '-'*10 + 'EXCEPTION:')
    print(__file__)
    print(e)
    print('-'*10 + 'end exception' + '\033[0m')


class ThorlabsP1xx(object):
    #USB0::0x1313::0x807B::17121241::INSTR
    def __init__(self,address='USB0::0x1313::0x807B::190218320::INSTR'):
        try:
            self._rm = visa.ResourceManager()
        except:
            # Get only pythonistic version of pyvisq
            self._rm =  visa.ResourceManager('@py')
        self._address = address
        self._open = False

    def isOpen(fun):
        def wrapper(*args, **kwargs):
            self_app = args[0]
            if self_app._open:
                out = fun(*args, **kwargs)
                return out
        return wrapper

    def waiter(fun):
        def wrapper(*args, **kwargs):
            out = fun(*args, **kwargs)
            time.sleep(0.2)
            return out
        return wrapper

    def Query(self, word):
        return self._instr.query(word).strip()

    def Write(self, word):
        return self._instr.write(word)

    @property
    def connected(self):
        return self._open

    @connected.setter
    def connected(self, val):
        if val:
            if not self._open:
                if self._address in self._rm.list_resources():
                    self._instr = self._rm.open_resource(self._address,timeout = 10)
                    self._instr.write_termination = '\r\n'
                    self._instr.read_termination = '\n'
                    self._instr.timeout = 10000
                    self._open = True

                else:
                    print('Please connect or provide the correct address for the powermeter')
                    self._open = False
        else:
            if self._open:
                self._instr.close()
                self._open = False

    @property
    @InOut.output(float)
    @waiter
    def power(self):
        self._instr.write('Measure:Power?')

        try:
            data = self._instr.read()
            return data.strip()
        except Exception as err:
            print(err)
            self._instr.write('*RST')
            self._instr.write('*CLS')
            self._instr.close()
            self._instr = self._rm.open_resource(self._address,timeout = 10)
            self._instr.timeout = 10000
    # return self.Query('Measure:Power?')

    @property
    @isOpen
    @waiter
    def identity(self):
        word = "*IDN?"
        return self.Query(word)

    @property
    @isOpen
    @InOut.output(float)
    @waiter
    def lbd(self):
        word = 'SENSE:CORRECTION:WAVELENGTH?'
        return self.Query(word)

    @lbd.setter
    @InOut.accepts(float)
    @waiter
    def lbd(self, val):
        word = 'SENSE:CORRECTION:WAVELENGTH {}'.format(val)
        self.Write(word)

    def __repr__(self):
        s = ['Thorlabs Power Meter Class']
        s += ['Use the self.power, self.lbd properties to use the pmeter']
        s += ['---------------------------------------------------------']
        s += ['Detector head:']
        try:
            s += ['\t' + self.identity]
        except:
            s += ['\tConnect to the detector using self.connected = True']
        return '\n'.join(s)

if __name__ == "__main__":
    P = ThorlabsP1xx()
    P.connected = True
    P.lbd = 1550
    while True:
        print("Power Read: {:.3f}uW".format(P.power*1e6 /(0.02)), end = "\r")
