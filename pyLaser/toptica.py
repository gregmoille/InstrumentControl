import sys
import time
import ipdb
import numpy as np

import os

import socket

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
        self._addrs = kwargs.get('address', '169.254.122.1')
        self._port = kwargs.get('port', 1998)
        self._open = False
        self._lbd = 0
        self._cc = 0
        self._scan_lim = []
        self._scan_speed = 0
        self._scan = 0
        self._beep = 0
        self._output = 0
        self._is_scaning = False
        # self._is_changing_lbd = False
        # self._no_error = <>
        self._haserr = False
        # Miscs
        self._err_msg = ''
        self._set = "param-set! "
        self._get = "param-ref "
        self._lsr = "'laser1:"
        self._exec = 'exec '
    # -- Methods --
    # ---------------------------------------------------------

    def Query(self, word):
        if not word is '':
            self._dev.send(word.strip().encode() + b'\n')
        time.sleep(0.001)
        read = ''
        while True:
            try:
                read +=self._dev.recv(1).decode()
                if read[-1] is '>':
                    break

            except:
                break
        return read.replace('>', '').strip()




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
            self._dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._dev.settimeout(0.01)
            self._dev.connect((self._addrs, self._port))
            self._open = True
            time.sleep(0.5)
            dum = b''
            while True:
                try: 
                    dum += self._dev.recv(1)
                    print(dum)
                    time.sleep(0.001)
                    if b'DeCoF Command Line\r\n ' in dum:
                        print(dum)
                        break
                except Exception as e:
                    print(e)
                    print(dum)
                    break
        else:
            self._dev.close()
            self._open = False

    @property
    @InOut.output(bool)
    def output(self):
        # word = <>
        self._output = self.Query(word)
        return self._output

    @output.setter
    # @Catch.error
    @InOut.accepts(bool)
    def output(self,value):
        # word = <>
        self.Query(word)
        self._output = value

    @property
    # @InOut.output(float)
    def lbd(self):
        word = "({} {}ctl:wavelength-act)".format(self._get, self._lsr)
        self._lbd = self.Query(word)
        return self._lbd

    @lbd.setter
    @InOut.accepts(float)
    # @Catch.error
    def lbd(self, value):
        word = "({} {}ctl:wavelength-set {:.3f})".format(self._set  , self._lsr, value)
        self.Query(word)
        self._lbd = value

    @property
    @InOut.output(float)
    def current(self):
        word = "({} {}dl:cc:current-act)".format(self._get, self._lsr)
        self._cc = self.Query(word)
        return self._cc

    @current.setter
    # @Catch.error
    @InOut.accepts(float)
    def current(self, value):
        word = "({} {}dl:cc:current-set {:.3f})".format(self._set, self._lsr, value)
        self.Query(word)
        self._cc = value

    @property
    @InOut.output(float,float)
    def scan_limit(self):
        word1 = "({} {}ctl:scan:wavelength-begin)".format(self._get, self._lsr)
        word2 = "({} {}ctl:scan:wavelength-end)".format(self._get, self._lsr)
        self._scan_lim = [self.Query(word1),
                        self.Query(word2)]
        return self._scan_lim

    @scan_limit.setter
    # @Catch.error
    @InOut.accepts(list)
    def scan_limit(self, value):
        start = value[0]
        stop = value[1]
        word1 = "({} {}ctl:scan:wavelength-begin {:.3f})".format(self._set, self._lsr, start)
        self.Query(word1)
        word2 = "({} {}ctl:scan:wavelength-end {:.3f})".format(self._set, self._lsr, stop)
        self.Query(word2)
        self._scan_lim = value

    @property
    @Catch.error
    # @InOut.output(float)
    def scan_speed(self):
        word1 = 'SOUR:WAVE:SLEW:FORW?'
        self._scan_speed = self.Query(word1)
        return self._scan_speed

    @scan_speed.setter
    # @Catch.error
    @InOut.accepts(float)
    def scan_speed(self, value):
        # word = <>
        self.Query(word)
        # word = <>
        self.Query(word)
        self._scan_speed = value

    @property
    @InOut.output(float)
    def scan(self):
        # word = <>
        self._scan = self.Query(word)
        return self._scan

    @scan.setter
    @Catch.error
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
        # word = <>
        self._pzt = self.Query(word)
        return self._pzt

    @pzt.setter
    @Catch.error
    @InOut.accepts(float)
    def pzt(self, value):
        # word = <>
        self.Query(word)
        self._pzt = value

    @property
    @InOut.output(bool)
    def beep(self):
        # word = <>
        self._beep = self.Query(word)
        return self.beep

    @beep.setter
    @Catch.error
    @InOut.accepts(bool)
    def beep(self, value):
        # word = <>
        self.Query(word)
        self._beep = value

    @property
    def identity(self):
        # word = <>
        self._id = self.Query(word)
        return self._id

    @property
    def error(self):
        # word = <>
        self._error = ''
        err = self.Query(word)
        return err

    # @property
    # def has_error(self):
    #     # word = <>
    #     dum = self.Query(word)
    #     if dum =='128': self._haserr = True
    #     if dum == '0': self._haserr = False
    #     return self._haserr

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


if __name__ is '__main__':
    lsr = Toptica1050()