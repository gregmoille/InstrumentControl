import socket
import numpy as np
import pandas as pd
import logging
import time
import pyvisa as visa
logger = logging.getLogger()

class KeysightE36100B(object):
    """
    DC power supply function
    """

    __author__ = "Greg Moille"
    __version__ = "0.1"
    __date__ = "2024-08-19"

    def __init__(self, **kargs):
        self.address = kargs.get("address", "USB0::0x2A8D::0x1902::MY61001585::INSTR")
        self._connected = False
        self._rm = visa.ResourceManager()

    def __enter__(self):
        self.connect = True
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect = False
        return self

    @property
    def connect(self):
        if self._connect:
            return self.idn
        else:
            return self._connected

    @connect.setter
    def connect(self, value):
        if value:
            self._inst = self._rm.open_resource(self.address)
            self._inst.timeout = 10000
            print("opened")
            # try:
            self.idn = self._inst.query("*IDN?")
            print(f"Successfully connected to instrument:{self.idn}")
            self._connected = True
            # except:
            #     print("Unable to connect to instrument!")
        else:
            self._inst.close()
            self._connected = False
            print("Connection closed")

    @property
    def identity(self):
        return self._inst.query("*IDN?")

    @property
    def voltage(self):
        return float(self._inst.query("VOLT?").strip())
    
    @voltage.setter
    def voltage(self, value):
        self._inst.write(f"VOLT {value}")

    @property
    def current(self):
        return float(self._inst.query("CURR?").strip())

    @current.setter
    def current(self, value):
        self._inst.write(f"CURR {value}")

    @property
    def output(self):
        return self._inst.query("OUTP?")
    
    @output.setter
    def output(self, value):
        if value:
            self._inst.write("OUTP ON")
        else:
            self._inst.write("OUTP OFF")

if __name__ == "__main__":
    with KeysightE36100B(ip = "10.0.0.37") as dc: 
        dc.voltage = 3.4
        dc.output = True
        time.sleep(2)
        print(dc.voltage)
        print(dc.current)
        dc.output = False