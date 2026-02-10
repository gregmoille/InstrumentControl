import pyvisa as visa
import numpy as np
import scipy as sp
import pandas as pd
import time

class RSA5106(object):
    """
    RSA function
    """

    __author__ = "Greg Moille"
    __version__ = "0.1"
    __date__ = "2023-11-01"

    def __init__(self, **kargs):
        self.ip = kargs.get("ip", None)
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
            self._inst = self._rm.open_resource(f"TCPIP0::{self.ip}::inst0::INSTR")
            self._inst.timeout = 10000
            try:
                self.idn = self._inst.query("*IDN?")
                print(f"Successfully connected to instrument:{self.idn}")
                self._connected = True
            except:
                print("Unable to connect to instrument!")
        else:
            self._inst.close()
            self._connected = False
            print("Connection closed")


    @property
    def continuous(self):
        return self._inst.query("INITiate:CONTinuous??").strip()
        
    @continuous.setter
    def continuous(self, value):
        if value:
            self._inst.write("INITiate:CONTinuous ON")
        else:
            self._inst.write("INITiate:CONTinuous OFF")
    
    @property
    def running(self):
        return int(self._inst.query("STATus:OPER:COND?").strip())
    
    @running.setter
    def running(self, value):
        if value:
            self._inst.write("INITiate:IMMediate")
        else:
            self._inst.write("ABORt")
        time.sleep(0.1)

    def getTrace(self):

        param = dict()
        param["fstart"] = float(self._inst.query("SENSE:SPEC:FREQ:START?").strip())
        param["fstop"] = float(self._inst.query("SENSE:SPEC:FREQ:STOP?").strip())
        #param["fspan"] = float(self._inst.query("SENSE:SPEC:FREQ:SPAN?").strip())
        param["Npts"] = int(
            self._inst.query("SENSE:SPEC:POINTS:COUNT?").strip().replace("P", "")
        )
        #param["RBW"] = float(
        #    self._inst.query("SENSE:SPEC:BAND:RES?").strip()
        #)
        #param["VBW"] = float(
        #    self._inst.query("SENSE:SPEC:BAND:VID?").strip()
        #)

        S = self._inst.query_binary_values("FETCH:SPEC:TRACE1?")
        freq = np.linspace(param["fstart"], param["fstop"], param["Npts"])
        df = pd.DataFrame(dict(freq=freq, S=S))
            
        return param, df

if __name__ == "__main__":
    with RSA5106(ip = "10.0.0.37") as rsa: 
        pram, df = rsa.getTrace()
        rsa.continuous = False
        rsa.running = 1

        while not rsa.running == 0:
            print("waiting")
            time.sleep(0.5)
        print("scane Done")
        rsa         