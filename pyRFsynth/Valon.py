import pyvisa as visa
import serial 
import struct
import re
import time


class Valon5105(object):
    def __init__(self, port = 'COM4'):
        rm = visa.ResourceManager()
        self._instr = serial.Serial()
        self._instr.port = port
        self._instr.timeout = 0.2
        self._instr.baudrate = 9600
        self._instr.open()
        self._clearBuffer()
    
    def _clearBuffer(self):
        self._query('', clear_after = False)    


    def _write(self, cmd):
        self._instr.write(cmd.encode() + b'\r')
    
    def _query(self, cmd, clear_after = True):
        self._instr.write(cmd.encode() + b'\r')
        out = []
        line = 'dum'
        while line != '':
            line = self._instr.readline().decode().strip()
            out.append(line)
        return '\n'.join(out)

    @property
    def identity(self):
        return self._query('ID')
    @property
    def status(self):
        return self._query('STAT')
    
    @property
    def RFout(self):
        out = self._query('OEN')
        return bool(int(re.findall("OEN.*(\d).*", out)[0]))
    
    @RFout.setter
    def RFout(self, val):
        self._write(f'OEN {int(val)}')

    @property
    def frequency(self):
        out = self._query('FREQ')
        val = re.findall(".*Act (\d+(?:\.\d+)?).*", out)[0]
        unit = re.findall(f".*Act {val} (.*)", out)[0]
        if unit == "Hz":
            return float(val)
        elif unit == "kHz":
            return float(val) * 1e3
        elif unit == "MHz":
            return float(val) * 1e6
        elif unit == "GHz":
            return float(val) * 1e9

    @frequency.setter
    def frequency(self, val):
        self._write(f'FREQ {int(val)} Hz')

    @property 
    def power(self):
        out = self._query('PWR')
        return float(re.findall(".*PWR ((?:\-)?\d+(?:\.\d+)?);.*", out)[0])

    @power.setter
    def power(self, val):
        self._write(f'PWR {val}')

if __name__ == '__main__':
    v = Valon5105()
    v.RFout
