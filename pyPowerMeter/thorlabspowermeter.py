
import visa
import numpy as np
from pyDecorators import InOut, ChangeState, Catch

class ThorlabsP1xx(object):

    def __init__(self,address='USB0::0x1313::0x807B::17121241::INSTR'):
        rm = visa.ResourceManager()
        if address in rm.list_resources():
            self._instr = rm.open_resource(address)
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
        else
            return self.Query('POW:RANGE:UPP?')


if __name__ == "__main__":
    P = ThorlabsP100()
    print("Power Read: {}".format(P.read))
