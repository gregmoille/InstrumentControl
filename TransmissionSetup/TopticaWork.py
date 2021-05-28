
from functools import wraps
from datetime import datetime
import time
import sys
import numpy as np
import threading
import os
import ipdb
import scipy.io as io
from copy import copy
work_dir = path = os.path.abspath(__file__ + '/..')
path = os.path.abspath(work_dir + '/../')
if not path in sys.path:
    sys.path.insert(0, path)
    print(path)
# import pyUtilities as ut
from pyLaser import NewFocus6700,Toptica1050  
from pyWavemeter import Wavemeter
from pyPowerMeter import ThorlabsP1xx
from workers import DcScan, FreeScan

from nidaqmx.constants import AcquisitionType, TaskMode
import nidaqmx

import matplotlib.pyplot as plt

# import matplotlib.pyplot as plt

class TopticaWorker():
    def __init__(self, **kwargs):
        self.lsr = kwargs.get('laser', None)
        self.wavemeter = kwargs.get('wavemeter', None)
        self.wavemeter_ch = kwargs.get('wavemeter_ch', 2)
        self.daq_ch = kwargs.get('daq_ch', 'ai0')
        self.daq_dev = kwargs.get('daq_dev', 'Dev1') 
    def run(self):
        lsr = self.lsr
        wlm = self.wavemeter
        lsr.lbd = lsr.scan_limit[0]
        lim = lsr.scan_limit
        while lsr._is_changing_lbd:
            print('setting lbd: {}nm'.format(lsr.lbd),end = "\r")
            time.sleep(0.1)
        print('setting lbd: {}nm'.format(lsr.lbd))
        # -- Wait for tabilization --
        # -----------------------------------------------
        time.sleep(1)


        if wlm:
            wlm.pulsemode = False
            wlm.widemode = False
            wlm.fastmode = False
            wlm.channel = self.wavemeter_ch
            wlm.exposure = 'auto'
            wlm.acquire = True
            print('Getting wavemeter')
            time.sleep(2.5)
            lbd_start = wlm.lbd
            wlm.acquire = False
            print('-'*30)
            print("Wavelength Start {:.3f}".format(lbd_start))
            print('-'*30)

        scan_time = np.diff(lsr.scan_limit)[0]/lsr.scan_speed

        print('-'*30)
        print('Scan Time: {}s'.format(scan_time))
        print('Limits: {} - {}nm'.format(lsr.scan_limit[0], lsr.scan_limit[1]))

        # Setup the DAQ
        ch = self.daq_ch
        dev = self.daq_dev
        system = nidaqmx.system.System.local()
        device = system.devices[dev]
        device.reset_device()
        clk = 0.75e6
        Npts = scan_time*clk*1.2
        self.readtask = nidaqmx.Task()


        if not type(ch)==list:
            ch = [ch]
        ch = dev + '/' +  ',{}/'.format(dev).join(ch)

        self.readtask.ai_channels.add_ai_voltage_chan(ch)
        self.readtask.timing.cfg_samp_clk_timing(clk, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=int(Npts)) 
        # test = nidaqmx.stream_readers.AnalogSingleChannelReader

        print('-'*30)
        print('Npts: {}'.format(Npts))
        # daq.SetupRead(read_ch=['ai0', 'ai23'])
        self._daqScanning = True
        self.data = []
        self.dt = []
        self._done_get_data = False
        def _GetData():
            # while self._daqScanning:
            self.time_start_daq = time.time()
            self.data += self.readtask.read(number_of_samples_per_channel=int(Npts), timeout = scan_time*1.5)
            self.time_end_daq = time.time()
            
            print('*'*30)
            self.readtask.stop()
            self.readtask.close()
            self.data = np.array(self.data)
            self._done_get_data = True

        threadDAQdata = threading.Thread(target=_GetData, args=())
        threadDAQdata.daemon = True
        lim = lsr.scan_limit
        lsr.scan = True
        self.readtask.start()
        t1 = time.time()
        threadDAQdata.start()
        print('-'*20 + 'Starscan')
        while True:
            print(lsr._lbdscan,end = "\r")
            if lsr._lbdscan >lim[1]-1:
                lsr.scan = False
                self._daqScanning = False
                break
            time.sleep(0.001)
        t2 = time.time()
        print(lsr._lbdscan)

        print('-'*30)
        print('End scan')

        t_end = t2-t1
        print("Time taken for scan: {}s".format(t_end))

        if wlm:
            wlm.pulsemode = False
            wlm.widemode = False
            wlm.fastmode = False
            wlm.channel = self.wavemeter_ch
            wlm.exposure = 'auto'
            wlm.acquire = True
            print('Getting wavemeter')
            time.sleep(2.5)
            lbd_stop = wlm.lbd
            wlm.acquire = False
            print('-'*30)
            print("Wavelength End {:.3f}".format(lbd_stop))
            print('-'*30)

        # data = readtask.read(number_of_samples_per_channel=int(t_end*clk))
        # self.readtask.close()
        while not self._done_get_data:
            print('waiting for the data')
            time.sleep(1)

        T = self.data[0]
        MZ = self.data[1]
        self.readtask.close() 
        t_daq = np.linspace(0,self.time_end_daq-self.time_start_daq, T.size) 

        ind = np.where(t_daq<=t_end)
        t_daq = t_daq[ind]
        T = T[ind]
        MZ= MZ[ind]

        # get Input and Output Power
        PwrMin = ThorlabsP1xx(address='USB0::0x1313::0x807B::17121241::INSTR')
        PwrMout = ThorlabsP1xx(address='USB0::0x1313::0x8072::P2009986::INSTR')
        PwrMin.lbd = 1050
        PwrMout.lbd = 1050
        Pin = PwrMin.read/0.1
        Pout = PwrMout.read/0.02

        PwrMin._instr.close()
        PwrMout._instr.close()
        full_data = {'lbd_start': lbd_start,
                    'lbd_stop': lbd_stop, 
                    'T': T,
                    'MZ': MZ,
                    'tdaq': t_daq,
                    'Pin': Pin,
                    'Pout': Pout}

        return full_data


if __name__ =="__main__":
        lsr = Toptica1050()
        lsr.connected = True
        lsr.scan_limit = [1020, 1070]
        daq_ch = ['ai0', 'ai23']
        wlm = Wavemeter()

        work = TopticaWorker(laser = lsr, wavemeter = wlm, daq_ch = daq_ch, daq_dev = 'Dev1')
        data = work.run()

        path = 'Z:/Microcombs/ACES/Measurement/20180504-TemperatureMeasurement'
        fname = 'LigentechG3_1b11_RW810G520_600mW'
        # io.savemat(path + '/' + fname + '.mat', data)
        plt.close('all')
        f, ax = plt.subplots()
        ax.plot(data['tdaq'],data['T'])
        f.show()