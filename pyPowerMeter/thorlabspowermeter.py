

import numpy as np
import os
import sys
import time
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
    def __init__(self,address='USB0::0x1313::0x8072::P2009986::INSTR'):
        rm = visa.ResourceManager('@py')
        if address in rm.list_resources():
            self._instr = rm.open_resource(address,timeout = 0.25)
            self._open = True
        else:
            print('Please connect or provide the correct address for the powermeter')
            self._open = False

    def isOpen(fun):
        def wrapper(*args, **kwargs):
            self_app = args[0]
            if self_app._open:
                out = fun(*args, **kwargs)
                return out
        return wrapper 

    def Query(self, word):
        return self._instr.query(word).strip()

    def Write(self, word):
        return self._instr.write(word)

    @property
    @InOut.output(float)
    def read(self):
        return self.Query('READ?')

    @property
    @isOpen
    @InOut.output(float)
    def identity(self):
        word = "*IDN?"
        return self.Query(word)

    @property
    @isOpen
    def range(self):
        auto = self.Querry('POW:RANGE:AUTO?')
        if auto: 
            return 'auto'
        else:
            return self.Query('POW:RANGE:UPP?')


    def close(self):
        self._instr.close()
    

    @property
    @isOpen
    @InOut.output(float)
    def lbd(self):
        word = 'SENSE:CORRECTION:WAVELENGTH?'
        return self.Query(word)

    @lbd.setter
    @InOut.accepts(float)
    def lbd(self, val):
        word = 'SENSE:CORRECTION:WAVELENGTH {}'.format(val)
        self.Write(word)

if __name__ == "__main__":
    P = ThorlabsP1xx()
    P.lbd = 1050
    while True:
        print("Power Read: {:.3f}uW".format(P.read*1e6 /(0.02)), end = "\r")
        time.sleep(0.1)