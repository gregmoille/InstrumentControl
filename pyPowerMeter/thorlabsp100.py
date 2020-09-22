
import visa
import numpy as np

class ThorlabsP100(object):

    def __init__(self,address='USB0::0x1313::0x8078::P0010609::INSTR')
        rm = visa.ResourceManager()
        if address in rm.list_ressources():
            self._instr = rm.open_resource('USB0::0x1313::0x8078::P0010609::INSTR')
        else:
            print('Please connect or provide the correct address for the powermeter')
            break

    def Read(self)
        self._power = float(self._inst.query('READ?').strip())
        return self._power

    @property
    def contrast(self,cntrst)
        self._inst.write('DISP:CONT {}'.format(cntrst))
    @property
    def brightness(self):
        self._brightness = self._inst.write('DISP:BRIG 1')
        return self._brightmess

    @brightness.setter
    def brightness(self, brght)
        if brght:
            self._inst.write('DISP:BRIG 1')
        else:
            self._inst.write('DISP:BRIG 0')
            