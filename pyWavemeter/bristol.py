import os
import sys
import socket
import telnetlib
import time


path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)
from pyDecorators import InOut


class Bristol(object):
    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip','10.0.0.29')
        self.port = kwargs.get('port',50000)
        self._connected = False

    def __enter__(self):
        self.connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connected = False
        return self

    def _EmptyBuffer(self, wait_sec = 0.1):
        skip_count = 0
        while True:
            out = self.socket.read_until(b'\n\n',wait_sec)
            if out == b'':
                skip_count += 1
            if skip_count > 2:
                break
    def _Querry(self, msg):
        read_msg = msg + b'\r\n'
        self.socket.write(read_msg)
        skip_count = 0
        out = b''
        while(True):
            out = self.socket.read_some()
            if out != b'' and out != b'1':
                # print(out)
                return out.decode().strip()

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, val):
        if val and not(self._connected):
            self.socket = telnetlib.Telnet(self.ip)
            self.socket.set_debuglevel(0)
            self._EmptyBuffer()
            self._connected = True
        elif not(val) and self._connected:
            self.socket.close()
            self._connected = False


    @property
    def lbd(self):
        self._lbd = float(self._Querry(b'READ:WAVelength?'))
        return self._lbd

    @property
    def freq(self):
        self._freq = float(self._Querry(b'READ:FREQuency?'))
        return self._freq

    @property
    def power(self):
        self._pow = float(self._Querry(b'READ:POWer?'))

        if self.power_unit == 'mW' :
            print(self._unit)
            self.pow = self._pow*1e-3
        return self._pow

    @property
    def power_unit(self):
        self._unit = self._Querry(b'UNIT:POWer?')
        return self._unit
