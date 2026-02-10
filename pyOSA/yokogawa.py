import socket
import numpy as np
import pandas as pd
import logging
<<<<<<< HEAD
import time
import sys
=======
>>>>>>> 30e7bbfd2f73f5821b3ddd766d9abac5a294c22d
logger = logging.getLogger()

class Yokogawa(object):

    """
    To Do:
        - detect when the OSA is back on local mode
            - add a close buton
            - automatically reopen a socket when pressing connect
              but cannot fetch any response from the OSA
        - add a parameter strcture when .mat is saved
        - everything is shift from 1 index in the resolution
    """


    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip','169.254.122.111')
        self.port = 10001
        self._BUFFER_SIZE = 3145728

        self._scanStatus = 0
        self._params = {}
        self._connected = False
        self._trace = 'TRA'
        self._scan = 'stop'

    def __enter__(self):
        self.connected = True
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connected = False
<<<<<<< HEAD
        time.sleep(0.2)
=======
>>>>>>> 30e7bbfd2f73f5821b3ddd766d9abac5a294c22d
        return self

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, val):
        if val and not(self._connected):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
<<<<<<< HEAD
            s.settimeout(0.2)
            s.setblocking(True)
=======
            s.settimeout(0.5)
>>>>>>> 30e7bbfd2f73f5821b3ddd766d9abac5a294c22d
            cnt = 0
            try:
                s.connect((self.ip, self.port))
                self.socket = s
                self._InitConnection()
                self._connected = True
            except socket.error as exc:
                print(f'Error Conection: {exc}')
                self._connected = False
<<<<<<< HEAD
=======
                # ret = s.error
                # self._connected =s.error
>>>>>>> 30e7bbfd2f73f5821b3ddd766d9abac5a294c22d
        elif not(val) and self._connected:
            self.socket.close()
            self._connected = False

    def _InitConnection(self):
<<<<<<< HEAD
        MESSAGE = 'open "anonymous"\r\n'
        self.socket.send(MESSAGE.encode())
        readout = self.socket.recvfrom(self._BUFFER_SIZE)

        MESSAGE = "*CLS\r\n"
        self.socket.send(MESSAGE.encode())
        readout = self._QuerryData(MESSAGE, self._BUFFER_SIZE)
        print(f'*CLS {readout.decode()}')

        MESSAGE = '*STB?\r\n'
        readout =  self._QuerryData(MESSAGE, self._BUFFER_SIZE)
        print(f'*STB? {readout.decode()}')

        print(self.identity)
=======
        Opening = 'open "anonymous"\n'
        buf = self._QuerryData(Opening , self._BUFFER_SIZE)
        buf = self._QuerryData(" " + "\n" , self._BUFFER_SIZE) #LOGIN step2
        self.EmptyBuffer()
>>>>>>> 30e7bbfd2f73f5821b3ddd766d9abac5a294c22d

    def _Write_OSA(self, MESSAGE):
        N = self.socket.send(MESSAGE.encode())
        return N

<<<<<<< HEAD
    def _QuerryData(self, MESSAGE, BUFFER_SIZE):
        readout = b''
        self.socket.send(MESSAGE.encode())
        while not readout.endswith(b'\r\n'):
            # print(readout)
            readout += self.socket.recvfrom(BUFFER_SIZE)[0]
        return readout
=======
    def _QuerryData(self,MESSAGE, BUFFER_SIZE):
        try:
            N = self.socket.send(MESSAGE.encode())
            readout = ''
            ReadBuffer = b' '
            KeepDoing = True
            while not ReadBuffer.decode()[-1] == '\n' :
                ReadBuffer = self.socket.recvfrom(BUFFER_SIZE)[0]
                readout = readout + ReadBuffer.decode()
            return readout
        except:
            return None
>>>>>>> 30e7bbfd2f73f5821b3ddd766d9abac5a294c22d


    @property
    def identity(self):
        try:
            MESSAGE = "*IDN?\r\n"
            readout =  self._QuerryData(MESSAGE, self._BUFFER_SIZE)
            return readout.decode()
        except Exception as e:
            print(f"Error in identity property: {e}")
            return None

    @property
    def identity(self):
        ID = self._QuerryData("*IDN?\n", 1).strip().split(',')

        return dict(maker = ID[0],
                    model = ID[1],
                    SN = ID[2])

    @property
    def trace(self):
        try:
<<<<<<< HEAD
            MESSAGE = ":TRACe:DATA:X? TRA\r\n"
            xread =  self._QuerryData(MESSAGE, self._BUFFER_SIZE)
            x = [float(xx) for xx in xread.decode().split(',')]

            MESSAGE = ":TRACe:DATA:Y? TRA\r\n"
            yread = self._QuerryData(MESSAGE, self._BUFFER_SIZE)
            y = [float(xx) for xx in yread.decode().split(',')]
            trace = pd.DataFrame({'lbd': x, 'S': y})
            return trace
        except Exception as err:
            print(err)
=======
            N = self._QuerryData(":TRACe:SNUMber? " +  self._trace +"\n", 1)
            X = self._QuerryData(":TRACe:X? " + self._trace  + "\n" , int(N))
            Y = self._QuerryData(":TRACe:Y? " + self._trace + "\n" , int(N))
            X = np.array([float(xx) for xx in X.split(',')])
            Y = np.array([float(xx) for xx in Y.split(',')])
            return pd.DataFrame({'lbd':X, 'S':Y})
        except:
>>>>>>> 30e7bbfd2f73f5821b3ddd766d9abac5a294c22d
            return None

    @trace.setter
    def trace(self, val):
        self._trace = val


    @property
    def settings(self):
        if not self._connected:
            print("OSA not connected")
            return
        else:
            self._params['centwlgth'] = float(self._QuerryData(":SENSe:WAVelength:CENTer?\n", 256).strip())
            self._params['span'] = float(self._QuerryData(":SENSe:WAVelength:SPAN?\n", 256).strip())
            self._params['sensitivity'] = float(self._QuerryData(":SENSe:SENSe?\n", 256).strip())
            self._params['pts'] = float(self._QuerryData(":SENSe:SWEep:POINts?\n", 256).strip())
            self._params['pts_auto'] = float(self._QuerryData(":SENSe:SWEep:POINts:AUTO?\n", 256).strip())
            self._params['resolution'] = float(self._QuerryData(":SENSe:BANDwidth?\n", 256).strip())
            self._params['calib_zero'] = float(self._QuerryData(":CALibration:ZERO:AUTO?\n", 256).strip())

            return self._params

    @settings.setter
    def settings(self, val):
        if not self._connected:
            print("OSA not connected")
            return
        try:
            print("Setting OSA parameters...")
            
            # Update internal parameters
            self._params['centwlgth'] = val['centwlgth']
            self._params['span'] = val['span']
            self._params['sensitivity'] = val['sensitivity']
            self._params['pts'] = val.get('pts', None)
            self._params['pts_auto'] = val.get('pts_auto', False)
            self._params['resolution'] = val['resolution']
            self._params['calib_zero'] = val.get('calib_zero',True)

            # Send commands to OSA
            success = True
            success &= self._Write_OSA(":SENSe:WAVelength:CENTer " + str(self._params['centwlgth']*1e9) + 'nm\n')
            success &= self._Write_OSA(":SENSe:BANDwidth " + str(self._params['resolution']*1e9) + 'nm\n')
            success &= self._Write_OSA(":SENSe:SENSe " + str(int(self._params['sensitivity'])) + '\n')
            if self._params['pts']:
                success &= self._Write_OSA(":SENSe:SWEep:POINts " + str(int(self._params['pts'])) + '\n')   
            else:
                if self._params['pts_auto']:
                    auto = "ON"
                else:
                    auto = "OFF"
                success &= self._Write_OSA(f":SENSe:SWEep:POINts:AUTO {auto}\n")
            success &= self._Write_OSA(":SENSe:WAVelength:SPAN " + str(self._params['span']*1e9) + 'nm\n')        
            if self._params['calib_zero']:
                calib = "ON"
            else:
                calib = "OFF"
            success &= self._Write_OSA(f":CALibration:ZERO:AUTO {calib}\n")
            if success:
                print("Successfully set OSA parameters")
            else:
                print("Some OSA parameters may not have been set properly")
                
        except Exception as e:
            print(f"Error setting OSA parameters: {e}")


    @property
    def status(self):
        if not self._connected:
            print("OSA not connected")
            return None
        try:
            MESSAGE = ":STATus:OPERation:CONDition?\r\n"
            cond = self._QuerryData(MESSAGE, self._BUFFER_SIZE)
            cond = int(cond.decode())
            return cond
        except Exception as e:
            print(f"Error getting OSA status: {e}")
            return None
        
        
    @property
    def scan(self):
        scan_type = {1: 'single', 2: 'repeat', 0: 'stop'}

        message = ":STATus:OPERation:CONDition?\r\n"
        cond = self._QuerryData(message,self._BUFFER_SIZE)
        cond = int(cond.decode())
        if cond: 
            message = ":INITiate:SMODe?\r\n"
            self._scanStatus = self._QuerryData(message,self._BUFFER_SIZE)
            self._scanStatus = int(self._scanStatus.decode())
        else:
            self._scanStatus = cond
        self._scan = scan_type[self._scanStatus]
        return self._scan

    @scan.setter
    def scan(self, ScanType):
        scan_type = {1: 'single', 2: 'repeat', 0: 'stop'}
        if ScanType.lower() == 'repeat':
            self._Write_OSA(":INITiate:SMODe 2\n")
            self._Write_OSA(":INITiate\n")
            self._scanStatus = 2

        elif ScanType.lower() == 'single':
            self._Write_OSA(":INITiate:SMODe 1\n")
            self._Write_OSA(":INITiate\n")
            self._scanStatus = 1

        elif ScanType.lower() == 'stop':
            self._Write_OSA(":Abort\n")
            self._scanStatus = 0

        self._scan = scan_type[self._scanStatus]
        
    
if __name__ == '__main__':
    ip = "10.0.0.21"
    with Yokogawa(ip = ip) as osa: 
        pass
    # f, ax = plt.subplots()
    # ax.plot(trace.lbd, trace.S)
    # f.show()