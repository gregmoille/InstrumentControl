from functools import wraps
from datetime import datetime
import time
import sys
import lttb
import numpy as np
import threading
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import ipdb
import scipy.io as io
from copy import copy
# from tranmission_Forge import MZCalibrate
from matplotlib.animation import FuncAnimation
work_dir = path = os.path.abspath(__file__ + '/..')
path = 'Z:/PythonSoftware/NewInstrumentControl'
if not path in sys.path:
    sys.path.insert(0, path)
# import pyUtilities as ut
# import msvcrt
from pyLaser import NewFocus6700,Toptica1050
from pyWavemeter import Wavemeter
from pyPowerMeter import ThorlabsP1xx
# from workers import DcScan, FreeScan
import h5py
from nidaqmx.constants import AcquisitionType, TaskMode
import nidaqmx
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, interactive, Layout


class DCScan():
    def __init__(self, **kwargs):
        self.lsr = kwargs.get('laser', None)
        self.wavemeter = kwargs.get('wavemeter', None)
        self.wavemeter_ch = kwargs.get('wavemeter_ch', 2)
        self.daq_ch = kwargs.get('daq_ch', ['ai0'])
        self.daq_dev = kwargs.get('daq_dev', 'Dev1')
        self.Pin_ratio = kwargs.get('Pin_ratio', 2/98)
        self.Pout_ratio = kwargs.get('Pout_ratio', 1/10)
        self.Pmeter_in = kwargs.get('Pmeter_in', None)
        self.Pmeter_out = kwargs.get('Pmeter_out',None)
        self._stop_shift = kwargs.get('_top_shift ',-1)
        self.sub = kwargs.get('sub', 200)
        init_notebook_mode(connected=True)
    def run(self):
        lsr = self.lsr
        time.sleep(0.05)
        wlm = self.wavemeter
        time.sleep(0.5)
        lim = lsr.scan_limit
        print('LIMITS: {}'.format(lim))
        time.sleep(0.05)
        lsr.lbd = lim[0]
        time.sleep(0.05)
        speed = lsr.scan_speed
        time.sleep(0.05)
        scan_time = np.diff(lim)[0]/speed

        print('-'*30)
        print('Limits: {} - {}nm'.format(lim[0], lim[1]))
        print('Scan Speed: {} nm/s'.format(speed))
        print('Scan Time: {}s'.format(scan_time))


        while lsr._is_changing_lbd or np.abs(lsr.lbd -lim[0])>0.5 :
            print('setting lbd: {:.3f}nm'.format(lsr.lbd),end = "\r")
            time.sleep(0.1)
        print('setting lbd: {:.3f}nm'.format(lsr.lbd))

        # -- Wait for stabilization --
        # -----------------------------------------------
        time.sleep(1)
        if wlm:
            wlm.pulsemode = False
            wlm.widemode = False
            wlm.fastmode = False
            wlm.channel = self.wavemeter_ch
            wlm.exposure = 'auto'
            wlm.acquire = True
            print('-'*30)
            print('Getting Wavemeter for Start Wavelength:')
            time.sleep(2.5)
            lbd_start = wlm.lbd
            wlm.acquire = False
            print("\tWavelength Start {:.3f}".format(lbd_start))

        else:
            lbd_start = lsr.lbd


        # Setup the DAQ
        ch = self.daq_ch
        dev = self.daq_dev
        system = nidaqmx.system.System.local()
        device = system.devices[dev]
        device.reset_device()
        clk = 0.5e6
        Npts = scan_time*clk
        self.readtask = nidaqmx.Task()


        if not type(ch)==list:
            ch = [ch]
        ch = dev + '/' +  ',{}/'.format(dev).join(ch)

        print('-'*30)
        print('Setting up DAQ')
        print('\tReading from {}'.format(ch))
        print('\tNpts: {}'.format(Npts))
        self.readtask.ai_channels.add_ai_voltage_chan(ch,min_val=-0.5, max_val=10)
        self.readtask.timing.cfg_samp_clk_timing(clk, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=int(Npts))

        # daq.SetupRead(read_ch=['ai0', 'ai23'])
        self._daqScanning = True
        self.data = []
        self.dt = []
        self._done_get_data = False
        def _GetData():
            self.time_start_daq = time.time()
            self.data += self.readtask.read(number_of_samples_per_channel=int(Npts), timeout = scan_time*1.5)
            self.time_end_daq = time.time()
            print('*'*30)
            print('Got DAQ data')
            self.readtask.stop()
            self.readtask.close()
            self.data = np.array(self.data)
            self._done_get_data = True



        threadDAQdata = threading.Thread(target=_GetData, args=())
        threadDAQdata.daemon = True
        # lim = lsr.scan_limit
        print(lim)
        lsr.scan = True
        self.readtask.start()
        t1 = time.time()
        _lbdscan = [lsr.lbd]
        # t_scan =
        threadDAQdata.start()
        print('-'*20 + 'Start Scan')
        print(lim)
        while _lbdscan[-1] <= lim[1] + self._stop_shift:# or not(lsr._lim[0] <= _lbdscan[-1] <= lsr._lim[1]):
            _lbdscan += [lsr.lbd]
            print('\t lbd: {:.3f}'.format(_lbdscan[-1]), end = '\r')
            time.sleep(0.001)

        lsr.scan = False
        self._daqScanning = False

        t2 = time.time()
        print('\t lbd: {:.3f}'.format(lsr.lbd))

        print('-'*20 + 'End Scan')
        t_end = t2-t1
        print("\tTime taken for scan: {}s".format(t_end))

        while not self._done_get_data:
            print('Waiting for the DAQ data', end = '\r')

        T = self.data[0]
        MZ = self.data[1]
        t_daq = np.linspace(0,self.time_end_daq-self.time_start_daq, T.size)
        _lbdscan = np.array(_lbdscan)
        t_scan = np.linspace(0, t_end, _lbdscan.size)
        lbdscan = np.interp(t_daq, t_scan,_lbdscan)



        ind = np.where(t_daq<=t_end)
        t_daq = t_daq[ind]
        T = T[ind]
        MZ= MZ[ind]
        lbdscan = lbdscan[ind]



        # -- Get Input and Output Power --
        # --------------------------------------------------------
        if self.Pmeter_in:
            self.Pmeter_in.lbd = 1050
            Pin = self.Pmeter_in.read*self.Pin_ratio
            Pin = 10*np.log10(Pin*1e3)
            # self.Pmeter_in._instr.close()
            print('-'*30)
            print('Power:')
            print('\tInput Power {:.3f}dBm'.format(Pin))
            if self.Pmeter_out:
                self.Pmeter_out.lbd = 1050
                Pout = self.Pmeter_out.read*self.Pout_ratio
                Pout = 10*np.log10(Pout*1e3)
                # self.Pmeter_out._instr.close()
                print('\tOutput Power {:.3f}dBm'.format(Pout))
                print('\tInsertion losses: {:.3f}dB'.format(Pin-Pout))
            else:
                Pout = None
        elif self.Pmeter_out:
            Pin = None
            self.Pmeter_out.lbd = 1050
            Pout = self.Pmeter_out.read/self.Pout_ratio
            Pout = 10*np.log10(Pout*1e3)
            # self.Pmeter_out._instr.close()
            print('\tOutput Power {:.3f}dBm'.format(Pout))
            print('\tInsertion losses: {:.3f}dB'.format(Pin-Pout))
        else:
            Pin = None
            Pout = None

        if wlm:
            wlm.pulsemode = False
            wlm.widemode = False
            wlm.fastmode = False
            wlm.channel = self.wavemeter_ch
            wlm.exposure = 'auto'
            wlm.acquire = True
            print('-'*30)
            print('Getting Wavemeter for End Wavelength:')
            time.sleep(2.5)
            lbd_stop = wlm.lbd
            wlm.acquire = False
            print("\tWavelength End {:.3f}".format(lbd_stop))
        else:
            lbd_stop = lsr.lbd

        # downsample the data
        dataT = np.array([lbdscan, T]).T
        dataMZ = np.array([lbdscan, MZ]).T
        # ipdb.set_trace()
        if self.sub >1:
            dataTsmall =  np.array([lbdscan[::self.sub], T[::self.sub]]).T
            dataMZsmall =  np.array([lbdscan[::self.sub], MZ[::self.sub]]).T

        else:
            dataTsmall = dataT
            dataMZsmall = dataMZ
        # # -- Dictionarry of full data --
        # --------------------------------------------------------
        full_data = {'lbd_start': lbd_start,
                    'lbd_stop': lbd_stop,
                    'lbd_scan': lbdscan,
                    'T': T,
                    'MZ': MZ,
                    'tdaq': t_daq,
                    'Pin': Pin,
                    'Pout': Pout}
        # # f, ax = plt.subplots()
        trace0 = go.Scatter(
                        x = dataTsmall[:,0],
                        y = dataTsmall[:,1]/dataTsmall[:,1].max(),
                        mode = 'lines',
                        name = 'T')
        trace1 = go.Scatter(
                        x = dataMZsmall[:,0],
                        y = dataMZsmall[:,1]/dataMZsmall[:,1].max(),
                        mode = 'lines',
                        name = 'MZ')
        data = [trace1, trace0]
        layout = dict(xaxis = dict(title = 'Wavelength (nm)'),
                  yaxis = dict(title = 'Signal (V)', rangemode = 'tozero'),
                  )
        print('figure')
        fig = go.Figure(data=data, layout=layout)
        print('displaying figure')
        iplot(fig)
        # ax.plot(MZ[::100])
        # ax.plot(T[::100])
        # f.show()
        # # lbd, T_cal = MZCalibrate(full_data, 42649513.76655776)
        # self.f, self.ax = plt.subplots()
        # self.ax.plot(lbd*1e9,T_cal)
        # self.f.show()

        return full_data

class FreeRun():
    def __init__(self,**kwargs):
        self.daq_ch = kwargs.get('daq_ch', 'ai0')
        self.daq_dev = kwargs.get('daq_dev', 'Dev1')
        self.lsr = kwargs.get('laser', None)

    def run(self):
        # -- set the laser piezo --
        clk = 0.1e6
        T = 1/20
        # _laser = self.lsr
        Npts = T*clk * 2
        # -- define the writting signal --
        t= np.linspace(0, 2*T, Npts)
        # -- setup the daq --
        dev = self.daq_dev
        ch = self.daq_ch
        system = nidaqmx.system.System.local()
        device = system.devices[dev]
        device.reset_device()
        if not type(ch)==list:
            ch = [ch]
        ch_read = dev + '/' +  ',{}/'.format(dev).join(ch)
        # ch_read = ch_read +  ',{}/{}'.format(dev,self.daq_probe)

         # -- Define the daq worker --
        def FetchDAQ(clk, Npts,dev, ch_read):
            readtask = nidaqmx.Task()
            # print(ch_read)
            readtask.ai_channels.add_ai_voltage_chan(ch_read,min_val=0, max_val=5)
            readtask.timing.cfg_samp_clk_timing(clk, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=int(Npts))
            data = readtask.read(number_of_samples_per_channel=int(Npts))
            readtask.close()
            return data

     # -- Define the Animation for Matplotlib --
        class MyDataFetchClass(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                # self._data =  dataClass
                self._period = 2*T+0.1
                self._nextCall = time.time()
                self._run = True
                self.clk = clk
                self.X = [[0,2*T]]
                self.Y = [[0, 5]]
                f, ax = plt.subplots()
                self.hLine = []
                self.hLine += ax.plot(self.X,self.Y)
                f.show()
                self.ani = FuncAnimation(f, self.update, frames =  2000000,interval = 10)
                self.f_num = f.number
                # self.lsr = _laser

            def update(self, i):
                for ii in range(len(self.X)):
                    self.hLine[ii].set_data(self.X[ii], self.Y[ii])




            def run(self):
                while True:
                    nt = int(Npts/2)
                    data = FetchDAQ(clk, Npts,dev, ch_read)
                    Trans  = np.array(data[0])
                    self.X = [t]
                    self.Y = [Trans]


        fetcher = MyDataFetchClass()

        # fetcher.daemon = True
        fetcher.start()
        # interact(Slide, x= widgets.FloatSlider(min=0,max=100, step = 0.01))

def PiezoSlide(lsr):
    def SlidePiezo(x):
        lsr.pzt = x
    _= interact(SlidePiezo, x= widgets.FloatSlider(description='Piezo:',min=0,max=100, step = 0.01, layout=Layout(width='100%')))

class PiezoScan():
    def __init__(self, **kwargs):
        self.lsr = kwargs.get('laser', None)
        self.Vmax = kwargs.get('Vmax', 140)
        self.Vmin = kwargs.get('Vmin', 140)
        self.Vcoeff = kwargs.get('Vcoeff', 23)
        self.daq_ch = kwargs.get('daq_ch', 'ai0')
        self.daq_write = kwargs.get('daq_write', 'ao0')
        self.daq_probe = kwargs.get('daq_probe', 'ai16')
        self.daq_dev = kwargs.get('daq_dev', 'Dev1')
        self.freq_scan = kwargs.get('freq_scan', 20)
        self.pzt_center = kwargs.get('pzt_center', 0)

    def Triangle(self, T, Npts):
        clk = 0.75e6
        Vmax = self.Vmax/self.Vcoeff
        Vmin = self.Vmin/self.Vcoeff
        t = np.linspace(0, 2*T, Npts)
        down = lambda x : x *(Vmin-Vmax)/(T*0.5) + Vmax
        up = lambda x : x *(Vmax-Vmin)/(T*0.5)
        t = np.linspace(0, 2*T, Npts)
        x = t[np.where(t<T/2)]
        ydown = list(down(x))
        yup = list(up(x))
        y = ydown + yup
        to_add = int(t.size/4)
        y = list(np.zeros(to_add)) + y + list(np.zeros(to_add))

        return (t, np.array(y))

        # ipdb.set_trace()
        # assert len(y) == len(t)
        return (t, np.array(y))

    def Slope(self, T, Npts):
        clk = 0.75e6
        Vmax = self.Vmax/self.Vcoeff
        Vmin = self.Vmin
        t = np.linspace(0, 2*T, Npts)
        up = lambda x : -x *(Vmax-Vmin)/T + Vmax
        t = np.linspace(0, 2*T, Npts)
        x = t[np.where(t<=T)]
        yup = list(up(x))
        y = yup
        to_add = int(t.size/4)
        y = list(np.zeros(to_add)) + y + list(np.zeros(to_add))

        return (t, np.array(y))

        # ipdb.set_trace()
        # assert len(y) == len(t)
        return (t, np.array(y))

    def run(self):
        # -- set the laser piezo --
        self.lsr.pzt = self.pzt_center
        Vmax = self.Vmax/self.Vcoeff
        Vmin = self.Vmin/self.Vcoeff
        Vcoeff = self.Vcoeff
        clk = 0.1e6
        T = 1/self.freq_scan
        Npts = T*clk * 2
        # -- define the writting signal --
        t, write = self.Slope(T, Npts)
        ind_T =  np.where(t<=T)[0][-1]
        # -- setup the daq --
        dev = self.daq_dev
        ch = self.daq_ch
        system = nidaqmx.system.System.local()
        device = system.devices[dev]
        device.reset_device()

        if not type(ch)==list:
            ch = [ch]
        ch_read = dev + '/' +  ',{}/'.format(dev).join(ch)
        ch_read = ch_read +  ',{}/{}'.format(dev,self.daq_probe)
        ch_write = self.daq_write

        # -- Define the daq worker --
        def WriteAndFetchDAQ(clk, Npts,dev, ch_read, ch_write):
            readtask = nidaqmx.Task()
            # print(ch_read)
            readtask.ai_channels.add_ai_voltage_chan(ch_read,min_val=-0.5, max_val=6)
            readtask.timing.cfg_samp_clk_timing(clk, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=int(Npts))

            writetask = nidaqmx.Task()
            writetask.ao_channels.add_ao_voltage_chan("{}/{}".format(dev, ch_write))
            writetask.timing.cfg_samp_clk_timing(int(clk),
                                                        sample_mode=AcquisitionType.CONTINUOUS,
                                                        samps_per_chan=int(Npts))
            writetask.write(write, auto_start=False)
            writetask.start()
            data = readtask.read(number_of_samples_per_channel=int(Npts))
            readtask.close()
            writetask.close()
            return data


        # -- Define the Animation for Matplotlib --
        class MyDataFetchClass(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                # self._data =  dataClass
                self._period = 2*T+0.1
                self._nextCall = time.time()
                self._run = True
                self.clk = clk
                self.X = [[0, self._period/2]]
                self.Y = [[0, Vmax]]
                f, ax = plt.subplots()
                self.hLine = []
                x = np.linspace(0, t[-1], write.size)
                self.hLine += ax.plot(x,write)
                self.hLine += ax.plot(x, write)
                f.show()
                self.ani = FuncAnimation(f, self.update, frames =  2000000,interval = 20)
                self.f_num = f.number

            def update(self, i):
                x = np.linspace(0, t[-1], write.size)
                for ii in range(len(self.X)):
                    self.hLine[ii].set_data(x, self.Y[ii])


            def run(self):
                while True:
                    if plt.fignum_exists(self.f_num):
                        nt = int(Npts/2)
                        data = WriteAndFetchDAQ(clk, Npts,dev, ch_read, ch_write)
                        Trans  = np.array(data[0])
                        probe = np.array(data[2])
                        self.X = [probe*Vcoeff]
                        self.Y = [Trans]
                    else:
                        print('stop')
                        break
        fetcher = MyDataFetchClass()

        fetcher.start()

def ReadPmeter(Pmeter, ratio):
    pass
    # while True:
    #     if msvcrt.kbhit():
    #         if ord(msvcrt.getch()) == 27:
    #             break
    #     else:
    #
    #         print("Power Read: {:.3f}uW".format(Pmeter.read*1e6 *ratio), end = "\r")

def SaveDCdata(data, path,fname):
    fname = path + fname
    h5f = h5py.File('{}.h5'.format(fname), 'w')
    h5f.create_dataset('lbd_start', data=[data['lbd_start']])
    h5f.create_dataset('lbd_stop', data=[data['lbd_stop']])
    h5f.create_dataset('lbd_scan', data=[data['lbd_scan']])
    h5f.create_dataset('T', data=data['T'])
    h5f.create_dataset('MZ', data=data['MZ'])
    h5f.create_dataset('tdaq', data=data['tdaq'])
    if data['Pin']  == None:
        h5f.create_dataset('Pin', data=[0])
    else:
        h5f.create_dataset('Pin', data=[data['Pin']])
    if data['Pout']  == None:
        h5f.create_dataset('Pout', data=[0])
    else:
        h5f.create_dataset('Pout', data=[data['Pout']])

if __name__ =="__main__":
        lsr = Toptica1050()
        lsr.connected = True
        lsr.scan_limit = [1020, 1070]
        lsr.scan_speed = 4
        daq_ch = ['ai0', 'ai23']
        # daq_ch = ['ai22']
        # wlm = Wavemeter()
        # Pmeter_in = ThorlabsP1xx(address='USB0::0x1313::0x807B::17121241::INSTR')
        # Pmeter_out = ThorlabsP1xx(address='USB0::0x1313::0x8072::P2009986::INSTR')


        Piezo = PiezoScan(laser = lsr,daq_ch = daq_ch, daq_dev = 'Dev3',
                        daq_probe = 'ai16', daq_write = 'ao0' )

        Free = FreeRun(laser = lsr,daq_ch = ['ai0'], daq_dev = 'Dev3',)


        DC = TopticaWorker(laser = lsr, wavemeter = None,
                             daq_ch = daq_ch, daq_dev = 'Dev3',
                            Pmeter_in = None, Pmeter_out = None,
                            Pin_ratio= 10, Pout_ratio= 10)
        # data = work.run()

        # path = 'Z:/Microcombs/ACES/Measurement/20180504-TemperatureMeasurement'
        # fname = 'LigentechG3_1b11_RW810G520_600mW'
        # # io.savemat(path + '/' + fname + '.mat', data)
        # plt.close('all')
        #
