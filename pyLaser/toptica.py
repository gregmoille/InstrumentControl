import sys
import time
import ipdb
import numpy as np

import os
try:
    import clr
    clr.AddReference(r'mscorlib')
    from System.Text import StringBuilder
    from System import Int32
    from System.Reflection import Assembly
except:
    pass
import ipdb

path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)
from pyDecorators import InOut, ChangeState, Catch


class Toptica1050():

    __author__ = "Gregory Moille"
    __copyright__ = "Copyright 2018, NIST"
    __credits__ = ["Gregory Moille",
                   "Xiyuan Lu",
                   "Kartik Srinivasan"]
    __license__ = "GPL"
    __version__ = "1.0.0"
    __maintainer__ = "Gregory Moille"
    __email__ = "gregory.moille@mist.gov"
    __status__ = "Development"

    def __init__(self, **kwargs):
        super(Toptica1050, self).__init__()
        # some misc
        self._set = "param-set!"
        self._get = "param-ref"
        self._lsr = "'laser1"
        self._exec = 'exec '


    # -- Methods -- 
    # ---------------------------------------------------------
    def Querry(self, word):
        pass

    # -- Decorators --
    # ---------------------------------------------------------
    @property
    def connected(): 
        pass

    @property
    @InOut.output(bool)
    def lbd(self):
        word = '({} {}:ctl:wavelength-act)'.format(self._set, self._lsr)
        return self.Querry(word)

    @lbd.setter
    @Catch.error
    @InOut.accepts(float)
    def lbd(self, value):
        word = '({} {}:ctl:wavelength-set {:.3f})'.format(self._set, 
                                                        self._lsr,
                                                        value)
        self.Querry(word)

    @property
    def current(self):
        word = '({} {}dl:cc:current-act)'.format(self._set, self._lsr)
        return self.Querry(word)
    
    @current.setter
    def current(self, value):
        word = '({} {}:dl:cc:current-set {:.3f})'.format(self._set, 
                                                        self._lsr,
                                                        value)
        self.Querry(word)

    @property
    @InOut.output(float,float)
    def scan_limit(self):
        word1 = '({} {}ctl:scan:wavelength-begin)'.format(self._set, self._lsr)
        word2 = '({} {}ctl:scan:wavelength-end)'.format(self._set, self._lsr)
        self._scan_lim = [self.Querry(word1),
                        self.Querry(word2)]
        return self._scan_lim

    @scan_limit.setter
    @Catch.error
    @InOut.accepts(list)
    def scan_limit(self, value):
        start = value[0]
        stop = value[1]
        word1 = '({} {}:ctl:scan:wavelength-begin {:.3f})'.format(self._set, 
                                                        self._lsr,
                                                        value)
        self.Querry(word1)
        word2 = '({} {}:ctl:scan:wavelength-end {:.3f})'.format(self._set, 
                                                        self._lsr,
                                                        value)
        self.Querry(word2)
        self._scan_lim = value

    @property
    @Catch.error
    @InOut.output(float)
    def scan_speed(self):
        word = '({} {}:ctl:scan:speed'.format(self._set, self._lsr)
        return self.Querry(word)

    @scan_speed.setter
    @Catch.error
    @InOut.accepts(float)
    def scan_speed(self, value):
        word = 'ctl:scan:speed {}'.format(value)
        self.Querry(word)
        self._scan_speed = value

    @property
    @InOut.output(float)
    def scan(self):
        word = 'SOUR:WAVE:DESSCANS?'
        return self.Querry(word)

    @scan.setter
    @Catch.error
    @ChangeState.scan("OUTPut:SCAN:START",'OUTPut:SCAN:STOP')
    @InOut.accepts(bool)
    def scan(self, value):
        self._scan = value
        if self._scan:
            word = '({} {}:ctl:scan:start'.format(self._set, self._lsr)
        else:
            word = '({} {}:ctl:scan:stop'.format(self._set, self._lsr)
        self.Querry(word)

    @property
    @InOut.output(float)
    def pzt(self):
        pass
        # word = 'SOUR:VOLT:PIEZ?'
        # self._pzt = self.Querry(word)
        # return self._pzt

    @pzt.setter
    @Catch.error
    @InOut.accepts(float)
    def pzt(self, value):
        pass
        # word = 'SOUR:VOLT:PIEZ {}'.format(value)
        # self.Querry(word)
        # self._pzt = value

    @property
    @InOut.output(bool)
    def beep(self):
        pass
        # word = 'BEEP?'
        # self._beep = self.Querry(word)
        # return self.beep

    @beep.setter
    @Catch.error
    @InOut.accepts(bool)
    def beep(self, value):
        word = 'BEEP '.format(int(value))
        self.Querry(word)
        self._beep = value

    @property
    def identity(self):
        word = "*IDN?"
        return self.Querry(word)

    @property
    @InOut.output(str)
    def error(self):
        pass
        # word = 'ERRSTR?'
        # self._error = ''
        # err = self.Querry(word)
        # return err

    @property
    @InOut.output(bool)
    def has_error(self):
        pass
        # word = '*STB?'
        # dum = self.Querry(word)
        # if dum =='128': self._haserr = True
        # if dum == '0': self._haserr = False
        # return self._haserr

    @property
    def _is_scanning(self):
        word = '({} {}:ctl:state'.format(self._set, self._lsr)
        dum = self.Querry(word)
        # need to pass word

    @property
    def _is_changing_lbd(self): 
        word = '({} {}:ctl:state'.format(self._set, self._lsr)
        dum = self.Querry(word)
        # need to pass word

    @property
    def _lbdscan(self):
        if self._is_scanning:
            word = '({} {}:ctl:scan:progress'.format(self._set, self._lsr)
            return self.Querry(word)
        else:
            return self.lbd

