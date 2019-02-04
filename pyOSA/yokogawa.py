import socket
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

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


        self.socket = self.OpenTCPsocket()
        self.InitConnection()
        self._scanStatus = 0
        self._params = {}

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

    def GetTrace(self, trace = 'TRA'):
        N = self.QuerryData(":TRACe:SNUMber? TRA\n", 1)
        X = self.QuerryData(":TRACe:X? " + trace  + "\n" , int(N)*100000)
        Y = self.QuerryData(":TRACe:Y? " + trace + "\n" , int(N)*100000)
<<<<<<< HEAD
        X = np.array([float(xx) for xx in X.split(',')])
=======
        c = 299792458
        X = c/np.array([float(xx) for xx in X.split(',')])
>>>>>>> 646110f4d9a998e5ac97c2cd100b192191a06a36
        Y = np.array([float(xx) for xx in Y.split(',')])
        return (X,Y)


    @property
    def params(self):
        self._params['centwlgth'] = float(self.QuerryData(":SENSe:WAVelength:CENTer?\n", 256).strip())
        self._params['span'] = float(self.QuerryData(":SENSe:WAVelength:SPAN?\n", 256).strip())
        self._params['resol'] = float(self.QuerryData(":SENSe:SENSe?\n", 256).strip())
        self._params['pts'] = float(self.QuerryData(":SENSe:SWEep:POINts?\n", 256).strip())
        self._params['pts_auto'] = float(self.QuerryData(":SENSe:SWEep:POINts:AUTO?\n", 256).strip())
        self._params['bdwdth'] = float(self.QuerryData(":SENSe:BANDwidth?\n", 256).strip())

        return self._params

    @params.setter
    def params(self, val):
        self._params['centwlgth'] = val['centwlgth']
        self._params['span'] = val['span']
        self._params['resol'] = val['resol']
        self._params['pts'] = val['pts']
        self._params['pts_auto'] = val['pts_auto']
        self._params['bdwdth'] =  val['bdwdth']


        self.Write_OSA(":SENSe:WAVelength:CENTer " + str(self._params['centwlgth']*1e9) + 'nm\n')
        self.Write_OSA(":SENSe:BANDwidth " + str(self._params['bdwdth']*1e9) + 'nm\n')
        self.Write_OSA(":SENSe:SENSe "+ str(self._params['resol']) + '\n')
        self.Write_OSA(":SENSe:WAVelength:SPAN "+ str(self._params['span']*1e9) + 'nm\n')




    def Scan(self, ScanType):

        if ScanType.lower() == 'repeat':
            self.Write_OSA(":INITiate:SMODe 2\n")
            self.Write_OSA(":INITiate\n")
            self._scanStatus = 2

        elif ScanType.lower() == 'single':
            self.Write_OSA(":INITiate:SMODe 1\n")
            self.Write_OSA(":INITiate\n")
            self._scanStatus = 0

        elif ScanType.lower() == 'stop':
            self.Write_OSA(":Abort\n")
            self._scanStatus = 0

    def SaveTrace(self,fname):
        x,y = self.GetTrace()
        with open(fname, 'w') as fid:
            for ii in range(x.size):
                fid.write('{},{}\n'.format(x[ii], y[ii]))

    def PlotlyTrace(self, xlim = [], ylim = [], freq= False):
        init_notebook_mode(connected=True)
        c = 299792458
        lbd, S = self.GetTrace('TRA')
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
