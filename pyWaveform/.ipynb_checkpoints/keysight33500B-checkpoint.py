import socket
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import pandas as pd


class Keysight335500B(object):

    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip','A-33522B-12849.local')
        self.port = kwargs.get('port', 5025)
        self._BUFFER_SIZE = 256
        self._connected = False
        self._trace = 'TRA'

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, val):
        if val:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                s.connect((self.ip, self.port))
                self.socket = s
                self._InitConnection()
                self._connected = True
            except Exception as err:
                print(err)

    def _QuerryData(self,MESSAGE, BUFFER_SIZE):
        N = self.socket.send(MESSAGE.encode())
        readout = ''
        ReadBuffer = b' '
        KeepDoing = True
        while not ReadBuffer.decode()[-1] == '\n' :
            ReadBuffer = self.socket.recvfrom(BUFFER_SIZE)[0]
            readout = readout + ReadBuffer.decode()
        return readout

    def WriteData(self, MESSAGE):
        self.socket.send(MESSAGE.encode())

    def EmptyBuffer(self):
        ReadBuffer = b''
        self.socket.send(b' \n')
        while not ReadBuffer == b'\n':
            try:
                ReadBuffer = self.socket.recvfrom(1)[0]
            except:
                break

    def _InitConnection(self):
        Opening = '*IDN?\n'
        buf = self._QuerryData(Opening , self._BUFFER_SIZE)
        print(buf.strip())
        # buf = self._QuerryData(" " + "\n" , self._BUFFER_SIZE) #LOGIN step2
        # print(buf)
        self.EmptyBuffer()

    # ---------

    @property
    def output(self):
        msg = 'OUTPut?\n'
        return float(self._QuerryData(msg , self._BUFFER_SIZE))

    @output.setter
    def output(self, val):
        if val:
            word = 'ON'
        else:
            word = 'OFF'
        msg = 'OUTPut {}\n'.format(word)
        self.WriteData(msg)

    # ---------

    @property
    def function(self):
        msg = 'OUTPut?\n'
        return float(self._QuerryData(msg , self._BUFFER_SIZE))

    @function.setter
    def function(self, val):
        if val.lower() in ['sine', 'square', 'ramp', 'pulse', 'noise', 'dc', 'user']:
            msg = 'OUTPut {}\n'.format(val)
            self.WriteData(msg)

    # ---------

    @property
    def Vhigh(self):
        msg = 'VOLTAGE:HIGH?\n'
        return float(self._QuerryData(msg , self._BUFFER_SIZE))

    @Vhigh.setter
    def Vhigh(self, val):
        msg = 'VOLTAGE:HIGH {:.3f}\n'.format(val)
        self.WriteData(msg)

    # ---------

    @property
    def Vlow(self):
        msg = 'VOLTAGE:LOW?\n'
        return float(self._QuerryData(msg , self._BUFFER_SIZE))

    @Vlow.setter
    def Vlow(self, val):
        msg = 'VOLTAGE:LOW {:.3f}\n'.format(val)
        self.WriteData(msg)

    # ---------

    @property
    def Vamp(self):
        msg = 'VOLTage?\n'
        return float(self._QuerryData(msg , self._BUFFER_SIZE))

    @Vamp.setter
    def Vamp(self, val):
        msg = 'VOLTage {:.3f}\n'.format(val)
        self.WriteData(msg)

    # ---------

    @property
    def freq(self):
        msg = 'FREQUENCY?\n'
        return float(self._QuerryData(msg , self._BUFFER_SIZE))

    @freq.setter
    def freq(self, val):
        msg = 'FREQUENCY {:.3f}\n'.format(val)
        self.WriteData(msg)

    # ---------

    @property
    def rampSymmetry(self):
        msg = 'FUNCtion:RAMP:SYMMetry?\n'
        return float(self._QuerryData(msg , self._BUFFER_SIZE))

    @rampSymmetry.setter
    def rampSymmetry(self, val):
        msg = 'FUNCtion:RAMP:SYMMetry {:.3f}\n'.format(val)
        self.WriteData(msg)

    # ---------

    @property
    def squareDutyCycle(self):
        msg = 'FUNCtion:SQUare:DCYCle?\n'
        return float(self._QuerryData(msg , self._BUFFER_SIZE))

    @squareDutyCycle.setter
    def squareDutyCycle(self, val):
        msg = 'FUNCtion:SQUare:DCYCle {:.3f}\n'.format(val)
        self.WriteData(msg)

if __name__ == '__main__':
    k = Keysight335500B()
    k.connected = True
