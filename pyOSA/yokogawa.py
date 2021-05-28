import socket
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import pandas as pd
import logging
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
        self._BUFFER_SIZE = 256


        # self.socket = self.OpenTCPsocket()
        # self.InitConnection()
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
        return self

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, val):
        if val and not(self._connected):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            cnt = 0
            try:
                s.connect((self.ip, self.port))
                self.socket = s
                self._InitConnection()
                self._connected = True
            except socket.error as exc:
                print(f'Error Conection: {exc}')
                self._connected = False
                # ret = s.error
                # self._connected =s.error
        elif not(val) and self._connected:
            self.socket.close()
            self._connected = False

    def _InitConnection(self):
        Opening = 'open "anonymous"\n'
        buf = self._QuerryData(Opening , self._BUFFER_SIZE)
        buf = self._QuerryData(" " + "\n" , self._BUFFER_SIZE) #LOGIN step2
        self.EmptyBuffer()

    def _Write_OSA(self, MESSAGE):
        N = self.socket.send(MESSAGE.encode())
        return N

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

    def EmptyBuffer(self):
        ReadBuffer = b''
        self.socket.send(b' \n')
        while not ReadBuffer == b'\n':
            try:
                ReadBuffer = self.socket.recvfrom(1)[0]
            except:
                break

    @property
    def identity(self):
        ID = self._QuerryData("*IDN?\n", 1).strip().split(',')

        return dict(maker = ID[0],
                    model = ID[1],
                    SN = ID[2])

    @property
    def trace(self):
        try:
            N = self._QuerryData(":TRACe:SNUMber? " +  self._trace +"\n", 1)
            X = self._QuerryData(":TRACe:X? " + self._trace  + "\n" , int(N))
            Y = self._QuerryData(":TRACe:Y? " + self._trace + "\n" , int(N))
            X = np.array([float(xx) for xx in X.split(',')])
            Y = np.array([float(xx) for xx in Y.split(',')])
            return pd.DataFrame({'lbd':X, 'S':Y})
        except:
            return None

    @trace.setter
    def trace(self, val):
        self._trace = val

    @property
    def settings(self):
        self._params['centwlgth'] = float(self._QuerryData(":SENSe:WAVelength:CENTer?\n", 256).strip())
        self._params['span'] = float(self._QuerryData(":SENSe:WAVelength:SPAN?\n", 256).strip())
        self._params['resol'] = float(self._QuerryData(":SENSe:SENSe?\n", 256).strip())
        self._params['pts'] = float(self._QuerryData(":SENSe:SWEep:POINts?\n", 256).strip())
        self._params['pts_auto'] = float(self._QuerryData(":SENSe:SWEep:POINts:AUTO?\n", 256).strip())
        self._params['bdwdth'] = float(self._QuerryData(":SENSe:BANDwidth?\n", 256).strip())

        return self._params

    @settings.setter
    def settings(self, val):
        self._params['centwlgth'] = val['centwlgth']
        self._params['span'] = val['span']
        self._params['resol'] = val['resol']
        self._params['pts'] = val['pts']
        self._params['pts_auto'] = val['pts_auto']
        self._params['bdwdth'] =  val['bdwdth']


        self._Write_OSA(":SENSe:WAVelength:CENTer " + str(self._params['centwlgth']*1e9) + 'nm\n')
        self._Write_OSA(":SENSe:BANDwidth " + str(self._params['bdwdth']*1e9) + 'nm\n')
        self._Write_OSA(":SENSe:SENSe "+ str(self._params['resol']) + '\n')
        self._Write_OSA(":SENSe:WAVelength:SPAN "+ str(self._params['span']*1e9) + 'nm\n')

    @property
    def scan(self):
        return self._scan

    @scan.setter
    def scan(self, ScanType):
        if ScanType.lower() == 'repeat':
            self._Write_OSA(":INITiate:SMODe 2\n")
            self._Write_OSA(":INITiate\n")
            self._scanStatus = 2

        elif ScanType.lower() == 'single':
            self._Write_OSA(":INITiate:SMODe 1\n")
            self._Write_OSA(":INITiate\n")
            self._scanStatus = 0

        elif ScanType.lower() == 'stop':
            self._Write_OSA(":Abort\n")
            self._scanStatus = 0

    def SaveTrace(self,fname):
        x,y = self.trace
        with open(fname, 'w') as fid:
            for ii in range(x.size):
                fid.write('{},{}\n'.format(x[ii], y[ii]))

    def PlotlyTrace(self, xlim = [], ylim = [], freq= False):
        init_notebook_mode(connected=True)
        c = 299792458
        df = self.trace
        lbd = df.lbd.values
        S = df.S.values
        if freq:
            x = 1e-12*c/lbd
            xlabel = 'Frequency (THz)'
        else:
            xlabel = 'Wavelength (nm)'
            x = lbd*1e9
        trace0 = go.Scatter(
                        x = x,
                        y = S,
                        mode = 'lines',
                        name = 'T')
        data = [trace0]
        layout = dict(xaxis = {'title' : xlabel,
                            'showspikes': True, 'spikethickness':1},
                  yaxis = {'title': 'Signal (dBm)',
                            'showspikes': True, 'spikethickness':1},
                  )
        if xlim:
            layout['xaxis'].update(range = xlim)
        if ylim:
            layout['yaxis'].update(range = ylim)
        fig = go.Figure(data=data, layout = layout)
        iplot(fig)
        return fig
