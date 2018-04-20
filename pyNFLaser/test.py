import numpy as numpy
import sys
import time
import ipdb
import numpy as np
import clr
import os
clr.AddReference(r'mscorlib')
from System.Text import StringBuilder
from System import Int32
from System.Reflection import Assembly
import ipdb

path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)
from pyDecorators import InOut, ChangeState


class MyDec():
    def TestQuerry(fun):
        def wrapper(*args, **kwargs):

            while True:
                try:
                    out = fun(*args, **kwargs)
                    break
                except:
                    print('communication error... retrying...')
                    print(args[0].error)
                    time.sleep(0.5)

            return out
        return wrapper

class NewFocus6700(object):
    def __init__(self, **kwargs):
        super(NewFocus6700, self).__init__()
        # Load usb ddl Newport
        try:

            dllpath = 'C:\\Anaconda3\\DLLs\\'
            Assembly.LoadFile(dllpath + 'UsbDllWrap.dll')
            clr.AddReference(r'UsbDllWrap')
            import Newport
            self._dev = Newport.USBComm.USB()
        except:
            self._dev = None
        # Laser state
        self._open = False
        self._DeviceKey = kwargs.get('key', None)
        self._idLaser = kwargs.get('id', None)
        # Laser properties
        self._lbd = '0'
        self._cc = 0
        self._scan_lim = []
        self._scan_speed = 0
        self._scan = 0
        self._beep = 0
        self._output = 0
        self._is_scaning = False
        self._is_changing_lbd = False

        # Miscs
        self._buff = StringBuilder(64)

    def Querry(self, word):
        self._buff.Clear()
        self._dev.Query(self._DeviceKey, word , self._buff)
        return self._buff.ToString()


    # -- Properties --
    # ---------------------------------------------------------
    @property
    def connected(self):
        return self._open

    @connected.setter
    def connected(self,value):
        # ipdb.set_trace()
        if value:
            if self._DeviceKey:
                try: 
                    out = self._dev.OpenDevices(self._idLaser, True)
                    dum = self._dev.Query('',self._DeviceKey, self._buff)
                    if out :
                        self._open = True
                        print('Laser Connected')
                except:
                    pass
            time.sleep(0.2)
        else:
            self._dev.CloseDevices()
            self._open = False

    @property
    @InOut.output(float)
    def lbd(self):
        word = 'SENSe:WAVElength?'
        self._lbd = self.Querry(word)
        return self._lbd

    @lbd.setter
    def lbd(self, value):
        self._targetlbd = value
        self.Querry('OUTP:TRACK 1')
        word =  'SOURCE:WAVE {}'.format(value)
        self.Querry(word)
        self._lbd = value

    @property
    def error(self):
        word = 'ERRSTR?'
        self._error = self.Querry(word)
        return self._error




if __name__ == '__main__':
    idLaser = 4106
    DeviceKey = '6700 SN10027'
    laser = NewFocus6700(id =idLaser, key = DeviceKey)
    laser.connected = True
    old_lbd = laser.lbd
    print('Laser wavelength:')
    print("\t{}".format(old_lbd))