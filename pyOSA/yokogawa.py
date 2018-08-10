import socket
import numpy


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


    def __init__(self):
        self.ip = '169.254.122.111'
        self.port = 10001
        self._BUFFER_SIZE = 256


        self.socket = self.OpenTCPsocket()
        self.InitConnection()
        self._scanStatus = 0


    def OpenTCPsocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((self.ip, self.port))
            ret = s
        except:
            ret = s.error

        return ret

    def InitConnection(self):
        Opening = 'open "anonymous"\n'
        buf = self.QuerryData(Opening , self._BUFFER_SIZE)
        print(buf)
        buf = self.QuerryData(" " + "\n" , self._BUFFER_SIZE) #LOGIN step2
        print(buf)
        self.EmptyBuffer()

    def Write_OSA(self, MESSAGE):
        N = self.socket.send(MESSAGE.encode())
        return N

    def QuerryData(self,MESSAGE, BUFFER_SIZE):
        N = self.socket.send(MESSAGE.encode())
        readout = ''
        ReadBuffer = b' '
        KeepDoing = True
        while not ReadBuffer.decode()[-1] == '\n' :
            ReadBuffer = self.socket.recvfrom(BUFFER_SIZE)[0]
            readout = readout + ReadBuffer.decode()
        return readout

    def EmptyBuffer(self):
        ReadBuffer = b''
        self.socket.send(b' \n') 
        while not ReadBuffer == b'\n':
            try:
                ReadBuffer = self.socket.recvfrom(1)[0]
            except:
                break

    def GetTrace(self, trace):
        X = self.QuerryData(":TRACe:X? " + trace  + "\n" , int(N)*100000)
        Y = self.QuerryData(":TRACe:X? " + trace + "\n" , int(N)*100000)
        X = np.array([float(xx) for xx in X.split(',')])
        Y = np.array([float(xx) for xx in Y.split(',')])
        return (X,Y)

    def SetParam(self):
        pass

    def Scan(self, ScanType):

        if ScanType == 'Repeat' and self._scanStatus == 0:
            self.Write_OSA(":INITiate:SMODe 2\n")
            self.Write_OSA(":INITiate\n")
            self._scanStatus = 2
            
        elif ScanType == 'Single' and self._scanStatus == 0:
            self.Write_OSA(":INITiate:SMODe 1\n")
            self.Write_OSA(":INITiate\n")
            self._scanStatus = 1

        elif ScanType == 'Stop' and not self._scanStatus ==0 :
            self.Write_OSA(":Abort\n")
            self._scanStatus = 0