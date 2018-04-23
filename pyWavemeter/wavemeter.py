import ctypes
from ctypes import c_double, c_long, c_bool, c_ushort,c_double
import time
import os
import sys
path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)
from pyDecorators import InOut


class Wavemeter(object):

    def __init__(self, **kwargs):
        super(Wavemeter, self).__init__()

        # load dll library
        self.dllpath = kwargs.get('dll', 'wlmData.dll')
        self.lib = ctypes.cdll.LoadLibrary(self.dllpath)
        self._ch = 0
        self._set_control()
        self._set_ctypes()

    def _set_control(self):
        self._show_hide = {'show': 1,
                           'hide': 2,
                           'silent': 64+ 3,
                           'exit': 3}
        self._wlm_status = {'connected': -1,
                            'controll': 3}

    def _set_ctypes(self):
        '''
        Define ctypes of C++ dll function 
        based on what is seen in the library
        '''
        self.lib.GetWavelengthNum.restype = c_double
        self.lib.GetWavelengthNum.argtypes = [c_long,  # input 1
                                              c_double]
        self.lib.Instantiate.restype = c_long
        self.lib.Instantiate.argtypes = [c_long]

        self.lib.SetExposureModeNum.restype = c_long
        self.lib.SetExposureModeNum.argtypes = [c_long, c_bool]

        self.lib.GetExposureModeNum.restype = c_long
        self.lib.GetExposureModeNum.argtypes = [c_long, c_bool]

        self.lib.SetExposureNum.restype = c_long
        self.lib.SetExposureNum.argtypes = [c_long, c_long, c_long]

        self.lib.GetExposureNum.restype = c_long
        self.lib.GetExposureNum.argtypes = [c_long, c_long, c_long]

        self.lib.Operation.restype = c_long
        self.lib.Operation.argtypes = [c_ushort]

        self.lib.GetSwitcherChannel.restype = c_long
        self.lib.GetSwitcherChannel.argtypes = [c_long]

        self.lib.SetSwitcherChannel.restype = c_long
        self.lib.SetSwitcherChannel.argtypes = [c_long]

        self.lib.GetWideMode.restype = c_ushort
        self.lib.GetWideMode.argtypes = [c_ushort]

        self.lib.SetWideMode.restype = c_long
        self.lib.SetWideMode.argtypes = [c_ushort]

        self.lib.GetFastMode.restype = c_bool
        self.lib.GetFastMode.argtypes = [c_bool]

        self.lib.SetFastMode.restype = c_long
        self.lib.SetFastMode.argtypes = [c_bool]

        self.lib.GetPulseMode.restype = c_ushort
        self.lib.GetPulseMode.argtypes = [c_ushort]

        self.lib.SetPulseMode.restype = c_long
        self.lib.SetPulseMode.argtypes = [c_ushort]

        self.lib.GetResultMode.restype = c_ushort
        self.lib.GetResultMode.argtypes = [c_ushort]

        self.lib.SetResultMode.restype = c_long
        self.lib.SetResultMode.argtypes = [c_ushort]

    @property
    @InOut.output(int)
    def channel(self):
        self._ch = self.lib.GetSwitcherChannel(0)
        return self._ch

    @channel.setter
    @InOut.accepts(int)
    def channel(self, value):
        self.lib.SetSwitcherChannel(value)
        self._ch = value

    @property
    @InOut.output(float)
    def lbd(self):
        return self.lib.GetWavelengthNum(self._ch, 0)

    @property
    def exposure(self):
        auto = self.lib.GetExposureModeNum(self._ch, 0)
        if auto:
            return 'automatic', self.lib.GetExposureNum(self._ch, 1, 0)
        else:
            return 'manual', self.lib.GetExposureNum(self._ch, 1, 0)

    @exposure.setter
    def exposure(self, value):
        if value == 'auto':
            self.lib.SetExposureModeNum(self._ch, 1)
        else:
            self.lib.SetExposureModeNum(self._ch, 0)
            self.lib.SetExposureNum(self._ch,1,value)


    @property
    @InOut.output(bool)
    def widemode(self):
        return self.lib.GetWideMode(0)

    @widemode.setter
    @InOut.accepts(bool)
    def widemode(self,value):
        self.lib.SetWideMode(int(value))

    @property
    @InOut.output(bool)
    def fastmode(self):
        return self.lib.GetFastMode(0)

    @fastmode.setter
    @InOut.accepts(bool)
    def fastmode(self, value):
        self.lib.SetFastMode(int(value))

    @property
    @InOut.output(bool)
    def pulsemode(self):
        return self.lib.GetPulseMode(0)

    @pulsemode.setter
    @InOut.accepts(bool)
    def pulsemode(self, value):
        self.lib.SetPulseMode(int(value))

    @property
    @InOut.output(bool)
    def acquire(self):
        pass

    @acquire.setter
    @InOut.accepts(bool)
    def acquire(self, value):
        if value:
            self.lib.Operation(2)
        else:
            self.lib.Operation(0)

    @property
    @InOut.output(bool)
    def connected(self):
        return self.lib.Instantiate(self._wlm_status['connected'])

    @connected.setter
    @InOut.accepts(str)
    def connected(self, view):
        assert view in self._show_hide, "Please specified 'show', 'hide' or 'exit'"
        out = self.lib.ControlWLMEx(self._show_hide[view], 0, 0)
        if view == 'exit':
            while self.connected:
                pass
            print('Wavemeter Disconnected!!')
            
        else:
            while not self.connected:
                pass
            print('Wavemeter Connected!!')
        return out

    @property
    @InOut.output(str)
    def resultmode(self):
        out = self.lib.GetResultMode(0)
        if out == 0:
            return 'vacuum'
        if out == 1:
            return 'air'
        if out ==2:
            return 'frequency'
        if out == 3:
            return 'wavenumber'
        if out == 4:
            return 'photonenergy'

    @resultmode.setter
    @InOut.output(str)
    def resultmode(self, val):
        if val == 'vacuum':
            word =  0
        if val == 'air':
            word =  1
        if val =='frequency':
            word =  2
        if val == 'wavenumber':
            word =  3
        if val == 'photonenergy':
            word =  4
        self.lib.SetResultMode(word)

if __name__ == '__main__':
        win = 'hide'
        wlm = Wavemeter()
        # wlm.Connect()
        # wlm.channel = 4
        # wlm.exposure = 'auto'
        # wlm.
        # time.sleep(2)
        # Set exposure to automatic
