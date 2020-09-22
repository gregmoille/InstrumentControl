import os
import sys
import time
import  numpy as np
import scipy.interpolate as intpl
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)
from pyNiDAQ import DAQ
import ipdb
import threading

class DcScan(QThread):
    '''
    ---------------------------------------------------------
    tw = DcScan(laser = <class>, 
                            wavemeter = <class>,
                            *args, **kwargs) 

    Class for DC Transmission characterization of nanodevices.

    For a full description of the algorithm , go please
    check the alogorigram in the Docs
    ----------------------------------------------------------
    Args:
        laser: laser object to control the equipement (c.f.
                pyNFLaser package)
        wavemeter: wavemeter object to controll the
                   equipement (c.f. pyWavemeter package)
                  If no wavemeter if passed, the class will 
                  work without it and will trust the 
                  wavelength provided by the laser internal
                  detector
        param: dictionary with 'laserParam', 
                   'daqParam' and 'wlmParam' keys
                laserParam keys (cf laser properties): 
                    - scan_speed
                    - scan_limit
                wlmParam keys (cf wavemeter properties):
                    - channel
                    - exposure 
                daqParam keys:
                    - read_ch
                    - write_ch
                    - dev
    Methods:
        self.run: See method doc string

    pyQtSlot emissions:
            self._DCscan <tupple>:
                [0] Code for where the  program is in 
                the algorithm:
                    -1 : no scan / end of scan
                    0 : setting up the start of scan
                    1 : scanning
                    2: return wavemeter of begining of scan
                    3: return wavemeter at end of scan
                [1] Laser current wavelength
                [2] Progress bar current %
                [3] Blinking State


    ------------------------------------------------------
    G. Moille - NIST - 2018
    ------------------------------------------------------
    '''
    __author__ = "Gregory Moille"
    __copyright__ = "Copyright 2018, NIST"
    __credits__ = ["Gregory Moille",
                   "Xiyuan Lu",
                   "Kartik Srinivasan"]
    __license__ = "GPL"
    __version__ = "1.0.0"
    __maintainer__ = "Gregory Moille"
    __email__ = "gregory.moille@mist.gov"
    __status__ = "Development"
    _DCscan = pyqtSignal(tuple)

    def __init__(self, **kwargs):
        QThread.__init__(self)
        self.laser = kwargs.get('laser', None)
        self.wavemeter = kwargs.get('wavemeter',None)
        self.param = kwargs.get('param',None)
        self._debug = kwargs.get('debug', False)

        # Misc
        self._is_Running = False

    def run(self):        
        # -- Fetch main parameters --
        laser = self.laser
        param = self.param
        wavemeter = self.wavemeter
        scan_limit = laser.scan_limit
        if self._debug:
            print("Scan limit: {}nm - {}nm".format(scan_limit[0], scan_limit[1]))
        
        # -- More user friendly notation --
        daqParam = param['daqParam']
        wlmParam = param.get('wlmParam', None)

        # -- Wait until lbd start of scan --
        while True:
            lbd = laser.lbd
            changing = laser._is_changing_lbd
            delta = lbd - scan_limit[0]
            cdt = not(changing) and np.abs(delta)<0.2
            if self._debug:
                print('-'*30)
                print('Is Changing: {}'.format(changing))
                print('Wavelength : {}nm'.format(lbd))
                print('Wavelength Difference: {:.3f}nm'.format(delta))
                print("Stop loop: {}".format(cdt))
                print('-'*30)
            if cdt:
                break
            time.sleep(0.25)
        
        # -- Wait for stabilization --
        time.sleep(2)

        # -- start the wavemeter if connected -- 
        if wavemeter:
            # check connect
            if not wavemeter.connected:
                if self._debug:
                    wavemeter.connected = 'show'
                else:
                    wavemeter.connected = 'hide'
                time.sleep(5)
            wavemeter.pulsemode = False
            wavemeter.widemode = False
            wavemeter.fastmode = False
            wavemeter.channel = wlmParam['channel']
            wavemeter.exposure = 'auto'

        # -- Get First wavelength of the scan -- 
        if wavemeter:
            # get it through the wavemeter
            wavemeter.acquire = True
            print('Getting wavemeter')
            time.sleep(2.5)
            lbd_start = wavemeter.lbd
            wavemeter.acquire = False
            print("Wavelength end {:.3f}".format(lbd_start))
            self._DCscan.emit((2, lbd_start, 0, None))
            if self._debug:
                print('Wavemeter start scan: {}nm'.format(lbd_start))
        else:
            self._DCscan.emit((2, laser.lbd, 0, None))

        # -- Setup DAQ for acquisition  and create the reading 
        #.   THread -- 
        scan_time = np.diff(scan_limit)[0]/laser.scan_speed 
        if self._debug:
            print('Scan time: {}s'.format(scan_time))
        daq = DAQ(t_end = scan_time, dev = daqParam['dev'])
        daq.SetupRead(read_ch=daqParam['read_ch'])
        self._done_get_data = False

        def _GetData():
            self.time_start_daq = time.time()
            self.data = daq.readtask.read(number_of_samples_per_channel=int(daq.Npts), timeout = scan_time*1.5)
            self.time_stop_daq = time.time()
            self._done_get_data = True
            print('*'*30)
            time.sleep(2)
            print('*'*30)
            daq.readtask.stop()
            daq.readtask.close()

        self.threadDAQdata = threading.Thread(target=_GetData, args=())
        self.threadDAQdata.daemon = True
        
        # -- Fetch wavelength and progress of scan -- 
        lbd_probe = []
        time_probe = []
        t_step = scan_time/1000

        if self._debug:
            print('Begining of Scan: '+ '-'*30)
            print('Time sleeping between steps: {}'.format(t_step))

        # -- Start laser scan --
        self._is_Running = True
        laser.scan = True
        self.threadDAQdata.start()
        while laser._is_scaning:
            lbd_scan = laser._lbdscan
            lbd_probe.append(lbd_scan)
            time_probe.append(time.time())
            prgs = np.floor(100*(lbd_scan-scan_limit[0])/np.diff(scan_limit)[0])
            if self._debug:
                print('Wavelength: {}nm'.format(lbd_scan))
                print('Progress: {}%'.format(prgs))
            self._DCscan.emit((1, lbd_scan, prgs, None))
            # time.sleep(t_step)
            if scan_limit[1] -lbd_scan < 0.75:
                laser.scan = False
                break  
        
        if self._debug:
            print('End of Scan: '+ '-'*30)

        # -- Scan Finished, get Data -- 
        while not self._done_get_data:
            if self._debug:
                print('Waiting for daq')
            time.sleep(0.1)

        

        # -- Get Last wavelength of the scan -- 
        if wavemeter:
            wavemeter.acquire = True
            time.sleep(2)
            lbd_end = wavemeter.lbd
            wavemeter.acquire = False
            self._DCscan.emit((3, lbd_end, 100, None))
            if self._debug:
                print('Wavemeter end scan: {}nm'.format(lbd_end))
        else:
            self._DCscan.emit((3, laser.lbd, 100, None))
        
        # -- Processing of the Data --
        # -----------------------------------------------------------------

        # -- Better notation of Data --
        data = np.array(self.data)
        T = data[0]
        MZ = data[1]
        time_probe = np.array(time_probe)
        lbd_probe = np.array(lbd_probe)
        time_probe = time_probe - time_probe[0]
        if self._debug:
            print("Time End of scan: {}s".format(time_probe[-1]))

        # -- Retrieve the time taken by the daq --
        tdaq = np.linspace(0,self.time_stop_daq-self.time_start_daq,len(T))

        # -- Only get the data while the scan was running --
        ind_max = np.where(tdaq<=time_probe[-1])[0][-1]
        if self._debug:
            print("Index End of scan: {}s".format(ind_max))
        tdaq = tdaq[:ind_max+1]
        MZ = MZ[:ind_max+1]
        T = T[:ind_max+1]

        # -- remove any moment the laser had an issue and
        # and return 0 or None --
        # cdt = [not(aa==0) and not(np.isnan(aa)) for aa in lbd_probe]
        # time_probe = time_probe[cdt]
        # lbd_probe = lbd_probe[cdt]

        # -- interpolate data for better precision --
        # f_int = intpl.splrep(time_probe, lbd_probe,1)
        # lbd_daq = intpl.splev(tdaq, f_int)

        # ipdb.set_trace()
        # -- Return data and= everything --
        # to_return = (tdaq, time_probe, lbd_daq,lbd_probe, [T, MZ])
        to_return = (tdaq, time_probe,lbd_probe, [T, MZ])

        self._DCscan.emit((-1, laser.lbd, 0, to_return))
        self._is_Running = False
        if self._debug:
            print('Done DC Scan')

    def stop(self):
        pass


class FreeScan(QThread):
    __author__ = "Gregory Moille"
    __copyright__ = "Copyright 2018, NIST"
    __credits__ = ["Gregory Moille",
                   "Xiyuan Lu",
                   "Kartik Srinivasan"]
    __license__ = "GPL"
    __version__ = "1.0.0"
    __maintainer__ = "Gregory Moille"
    __email__ = "gregory.moille@mist.gov"
    __status__ = "Development"
    _Freescan = pyqtSignal(list)

    def __init__(self, **kwargs):
        QThread.__init__(self)
        self.laser = kwargs.get('laser', None)
        self.param = kwargs.get('param', None)
        self._debug = kwargs.get('debug', False)
        self._is_Running = True
    
    def run(self):
        daqParam = self.param['daqParam']
        daq = DAQ(t_end = 0.1, dev = daqParam['dev'])

        def _GetData():
            self._done_get_data = False
            self.time_start_daq = time.time()
            self.data = daq.readtask.read(number_of_samples_per_channel=int(daq.Npts))
            self.time_stop_daq = time.time()
            self._done_get_data = True
            daq.readtask.stop()
            daq.readtask.close()

        while self._is_Running:
            self.threadDAQdata = threading.Thread(target=_GetData, args=())
            self.threadDAQdata.daemon = True

            daq.SetupRead(read_ch=daqParam['read_ch'])
            self.threadDAQdata.start()
            while not self._done_get_data:
                pass
            self._Freescan.emit(self.data[::100])

    def stop(self):
        self._is_Running = False

if __name__ == "__main__":
    from pyNFLaser import NewFocus6700
    from pyWavemeter import Wavemeter
    import matplotlib.pyplot as plt
    # Connect the laser
    idLaser = 4106
    DeviceKey = '6700 SN10027'
    laser = NewFocus6700(id =idLaser, key = DeviceKey)
    laser.connected = True

    # Connect the wavemeter
    wlm = Wavemeter()

    wlm.connected = 'show'
    param = {
            'laserParam': {'scan_limit': [1520.0, 1530.0],
                            'scan_speed': [5, 0.1],
            },
            'daqParam' : {'read_ch': ['ai0', 'ai1'],
                        'dev': 'Dev1'
            },
            'wlmParam': {'exposure': 'auto',
                        'channel': 4,
            }
    }



    worker = TransmissionWorkers()
    worker.DCscan(laser= laser,
                  wavemeter = wlm,
                  param = param)