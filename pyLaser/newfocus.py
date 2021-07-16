import sys
import time
# import ipdb
import numpy as np
import platform
import os

if platform.system().lower() == 'windows':
    # try:
    import clr
    clr.AddReference(r'mscorlib')
    from System.Text import StringBuilder
    from System import Int32
    from System.Reflection import Assembly
    # except Exception as err:
    #     print(err)
else:
    pass

# import ipdb

path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)
from pyDecorators import InOut, ChangeState, Catch


class NewFocus6700(object):
    '''
    Class for Newfocus 67xx laser control through USB with proper
    usb driver installed.

    Args:
        key: laser DeviceKey
        id:  laser id
    Methods:
        Open: open laser instance
        Close: close laser instance
    Properties (Fetch/Set):
        self.connected: laser connection active or no
        self.output: ON/OFF output state of the laser
        self.lbd :float: laser wavelength in nm
        self.current :float: laser current in A
        self.scan_limit :[float, float]: DC scan limit in nm
        self.scan_speed :float: DC scan speed in nm
        self.scan :bool: dc scan status
        self.beep :bool: set/disabel beep
        self.error :(read only): fetch error laser and wipe
        self.identity :(read only): fetch laser identity
    Utilities:
        self._open: flag if opening of laser successful
        self._dev : laser usb socket
        self._buff : buffer reading the laser status
        self._is_changing_lbd : track if wavelength is still
                                changing after the user set a
                                wavelength
        self._is_scaning : track in background if the scan is
                           still ongoing

    Example:
        import time
        import numpy as np
        import matplotlib.pyplot as plt
        from NewFocus6700 import NewFocus6700

        idLaser = 4106
        DeviceKey = '6700 SN10027'
        laser = NewFocus6700(id =idLaser, key = DeviceKey)
        laser.connected = True
        old_lbd = laser.lbd
        print(f'Laser wavelength: {old_lbd}nm')
        laser.scan_limit = [1520, 1550]
        laser.scan_speed = 10
        laser.lbd = laser.scan_limit[0]
        print('waiting until laser parked at correct lbd')
        while laser._is_changing_lbd:
            time.sleep(0.25)
        print(f'Current wavelength: {laser.lbd}nm')
        print('Now turning on the laser')
        laser.output = True
        t = np.array([])
        lbd = np.array([])
        print('Starting scan')
        laser.scan = True
        while laser._is_scaning:
            pass
        print('Finished scanning... now turning off the laser')
        laser.output = False
        print('All Done!')
    '''

    __author__ = "Gregory Moille"
    __copyright__ = "Copyright 2021, JQI"
    __credits__ = ["Gregory Moille",
                   "Kartik Srinivasan"]
    __license__ = "GPL"
    __version__ = "1.0.1"
    __maintainer__ = "Gregory Moille"
    __email__ = "gmoille@umd.edu"
    __status__ = "Development"

    def __init__(self, **kwargs):
        super(NewFocus6700, self).__init__()
        # Load usb ddl Newport
        try:
            # dllpath = 'C:\\ProgramData\\Anaconda3\\DLLs\\'
            # dllpath = 'C:\\Users\\Greg\\Anaconda3\\DLLs\\'
            dllpath = 'C:\\ProgramData\\Anaconda3\\DLLs\\'
            Assembly.LoadFile(dllpath + 'UsbDllWrap.dll')
            clr.AddReference(r'UsbDllWrap')
            import Newport
            self._dev = Newport.USBComm.USB()

        except Exception as err:
            print(err)
            self._dev = None
        # Laser state
        self._open = False
        self._DeviceKey = kwargs.get('key', None)
        self._idLaser = kwargs.get('id', 4106)
        # Laser properties
        self._lbd = '0'
        self._cc = 0
        self._scan_lim = []
        self._scan_speed = 0
        self._scan = 0
        self._beep = 0
        self._output = 0
        self._is_scaning = False
        # self._is_changing_lbd = False
        self._no_error = '0,"NO ERROR"'
        self._haserr = False
        # Miscs
        self._buff = StringBuilder(64)
        self._err_msg = ''

    # -- Decorators --
    # ---------------------------------------------------------
    def Checkopen(fun):
        def wrapper(*args, **kwargs):
            self = args[0]
            # if self._open and self._DeviceKey:
            if self._open and self._DeviceKey:
                out = fun(*args, **kwargs)
                return out
            else:
                pass
        return wrapper

    # -- Methods --
    # ---------------------------------------------------------

    def Query(self, word):
        self._buff.Clear()
        self._dev.Query(self._DeviceKey, word , self._buff)
        return self._buff.ToString()


    # -- Properties --
    # ---------------------------------------------------------
    @property
    @InOut.output(bool)
    def connected(self):
        return self._open

    @connected.setter
    # @Catch.error
    def connected(self,value):
        if value:
            if self._DeviceKey:
                # try:
                while True:
                    out = self._dev.OpenDevices(self._idLaser, True)
                    tab = self._dev.GetDeviceTable()
                    #empty buffer
                    out = self._dev.Read(self._DeviceKey, self._buff)
                    # ipdb.set_trace()
                    while not (out == -1 or  out == -2 or  out == int("-2")):
                        out = self._dev.Read(self._DeviceKey, self._buff)
                        print('Empyting the buffer: {}'.format(out))
                        time.sleep(0.5)
                    idn = self.identity
                    if not idn == "":
                        print("\nLaser connected: {}".format(idn))
                        break
                    else:
                        print('Ok reconection try')
                        self._dev.CloseDevices()
                        time.sleep(0.2)

                    # ipdb.set_trace()
                    self.error
                    self._open = True
                # except Exception as e:
                #     print(e)

        else:
            self._dev.CloseDevices()
            self._open = False

    @property
    @InOut.output(bool)
    def output(self):
        word = 'OUTPut:STATe?'
        self._output = self.Query(word)
        return self._output

    @output.setter
    # @Catch.error
    @InOut.accepts(bool)
    def output(self,value):
        word = "OUTPut:STATe {}".format(int(value))
        self.Query(word)
        self._output = value

    @property
    @InOut.output(float)
    def lbd(self):
        word = 'SENSe:WAVElength?'
        self._lbd = self.Query(word)
        return self._lbd

    @lbd.setter
    @InOut.accepts(float)
    # @Catch.error
    def lbd(self, value):
        self._targetlbd = value
        self.Query('OUTP:TRACK 1')
        word =  'SOURCE:WAVE {}'.format(value)
        self.Query(word)
        self._lbd = value

    @property
    @InOut.output(float)
    def current(self):
        word = 'SOUR:CURR:DIOD?'
        self._cc = self.Query(word)
        return self._cc

    @current.setter
    # @Catch.error
    @InOut.accepts(float)
    def current(self, value):
        word = 'SOUR:CURR:DIOD {}'.format(value)
        self.Query(word)
        self._cc = value

    @property
    @InOut.output(float,float)
    def scan_limit(self):
        word1 = 'SOUR:WAVE:START?'
        word2 = 'SOUR:WAVE:STOP?'
        self._scan_lim = [self.Query(word1),
                        self.Query(word2)]
        return self._scan_lim

    @scan_limit.setter
    # @Catch.error
    @InOut.accepts(list)
    def scan_limit(self, value):
        start = value[0]
        stop = value[1]
        word1 = 'SOUR:WAVE:START {}'.format(start)
        self.Query(word1)
        word2 = 'SOUR:WAVE:STOP {}'.format(stop)
        self.Query(word2)
        self._scan_lim = value

    @property
    # @Catch.error
    @InOut.output(float)
    def scan_speed(self):
        word1 = 'SOUR:WAVE:SLEW:FORW?'
        self._scan_speed = self.Query(word1)
        return self._scan_speed

    @scan_speed.setter
    # @Catch.error
    @InOut.accepts(float)
    def scan_speed(self, value):
        word = 'SOUR:WAVE:SLEW:FORW {}'.format(value)
        self.Query(word)
        word = 'SOUR:WAVE:SLEW:RET {}'.format(0.1)
        self.Query(word)
        self._scan_speed = value

    @property
    @InOut.output(float)
    def scan(self):
        word = 'SOUR:WAVE:DESSCANS?'
        self._scan = self.Query(word)
        return self._scan

    @scan.setter
    # @Catch.error
    @ChangeState.scan("OUTPut:SCAN:START",'OUTPut:SCAN:STOP')
    @InOut.accepts(bool)
    def scan(self, value):
        self.Query('SOUR:WAVE:DESSCANS 1')
        self._scan = value
        if self._scan:
            self.Query("OUTPut:SCAN:START")
        else:
            self.Query("OUTPut:SCAN:STOP")


    @property
    @InOut.output(float)
    def pzt(self):
        word = 'SOUR:VOLT:PIEZ?'
        self._pzt = self.Query(word)
        return self._pzt

    @pzt.setter
    # @Catch.error
    @InOut.accepts(float)
    def pzt(self, value):
        word = 'SOUR:VOLT:PIEZ {}'.format(value)
        self.Query(word)
        self._pzt = value

    @property
    @InOut.output(bool)
    def beep(self):
        word = 'BEEP?'
        self._beep = self.Query(word)
        return self.beep

    @beep.setter
    # @Catch.error
    @InOut.accepts(bool)
    def beep(self, value):
        word = 'BEEP '.format(int(value))
        self.Query(word)
        self._beep = value

    @property
    def identity(self):
        word = "*IDN?"
        self._id = self.Query(word)
        return self._id

    @property
    def error(self):
        word = 'ERRSTR?'
        self._error = ''
        err = self.Query(word)
        return err

    @property
    def has_error(self):
        word = '*STB?'
        dum = self.Query(word)
        if dum =='128': self._haserr = True
        if dum == '0': self._haserr = False
        return self._haserr

    @property
    @InOut.output(bool)
    def _is_changing_lbd(self):
        return self.Query('OUTP:TRACK?')

    @property
    def clear(self):
        pass

    @clear.setter
    @InOut.accepts(bool)
    def clear(self,val):
        if val:
            self.Query('*CLS')



if __name__ == '__main__':
    idLaser = 4106
    DeviceKey = '6700 SN10027'
    laser = NewFocus6700(id =idLaser, key = DeviceKey)
    # laser.beep = False
    laser.connected = True
    print("First error caught: {}".format(laser.error))
    # ipdb.set_trace()
    old_lbd = laser.lbd
    pzt = laser.pzt
    # laser.lbd = old_lbd +2
    print('Laser wavelength:')
    print("\t{}".format(old_lbd))
    print('Laser piezo:')
    print("\t{}".format(pzt))
    # laser.connected = False
