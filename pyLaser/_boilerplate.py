import sys
import time
import ipdb
import numpy as np
import os
path = os.path.realpath('../')
if not path in sys.path:
sys.path.insert(0, path)
from pyDecorators import InOut, ChangeState, Catch


class <YourLaserName>(object):
def __init__(self, **kwargs):
    super(<YourLaserName>, self).__init__()
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
    self._no_error = <>
    self._haserr = False
    # Miscs
    self._err_msg = ''
# -- Methods --
# ---------------------------------------------------------

def Query(self, word):
    #querry method for your laser
    pass

# -- Properties --
# ---------------------------------------------------------
@property
@InOut.output(bool)
def connected(self):
    return self._open

@connected.setter
@Catch.error
def connected(self,value):
    pass

@property
@InOut.output(bool)
def output(self):
    word = <>
    self._output = self.Query(word)
    return self._output

@output.setter
@Catch.error
@InOut.accepts(bool)
def output(self,value):
    word = <>
    self.Query(word)
    self._output = value

@property
@InOut.output(float)
def lbd(self):
    word = <>
    self._lbd = self.Query(word)
    return self._lbd

@lbd.setter
@InOut.accepts(float)
@Catch.error
def lbd(self, value):
    self._targetlbd = value
    self.Query('OUTP:TRACK 1')
    word = <>
    self.Query(word)
    self._lbd = value

@property
@InOut.output(float)
def current(self):
    word = <>
    self._cc = self.Query(word)
    return self._cc

@current.setter
@Catch.error
@InOut.accepts(float)
def current(self, value):
    word = <>
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
@Catch.error
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
@Catch.error
@InOut.output(float)
def scan_speed(self):
    word1 = 'SOUR:WAVE:SLEW:FORW?'
    self._scan_speed = self.Query(word1)
    return self._scan_speed

@scan_speed.setter
@Catch.error
@InOut.accepts(float)
def scan_speed(self, value):
    word = <>
    self.Query(word)
    word = <>
    self.Query(word)
    self._scan_speed = value

@property
@InOut.output(float)
def scan(self):
    word = <>
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
    word = <>
    self._pzt = self.Query(word)
    return self._pzt

@pzt.setter
@Catch.error
@InOut.accepts(float)
def pzt(self, value):
    word = <>
    self.Query(word)
    self._pzt = value

@property
@InOut.output(bool)
def beep(self):
    word = <>
    self._beep = self.Query(word)
    return self.beep

@beep.setter
@Catch.error
@InOut.accepts(bool)
def beep(self, value):
    word = <>
    self.Query(word)
    self._beep = value

@property
def identity(self):
    word = <>
    self._id = self.Query(word)
    return self._id

@property
def error(self):
    word = <>
    self._error = ''
    err = self.Query(word)
    return err

@property
def has_error(self):
    word = <>
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
    pass