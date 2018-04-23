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

class DcScan(QThread):
    '''
    ------------------------------------------------------
    tw = DcScan(laser = <class>, 
                            wavemeter = <class>,
                            *args, **kwargs) 

    Class for Transmission characterization of nanodevices.
    ------------------------------------------------------
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
        # super(TransmissionWorkers, self).__init__()


        # Misc
        self._is_Running = False

    def run(self):        
        # -- Fetch main parameters --
        laser = self.laser
        param = self.param
        wavemeter = self.wavemeter
        scan_limit = laser.scan_limit
        
        # -- More user friendly notation --
        daqParam = param['daqParam']
        wlmParam = param.get('wlmParam', None)

        # -- Wait until lbd start of scan --
        while laser._is_changing_lbd:
            time.sleep(0.25)
        
        # -- Wait for stabilization --
        time.sleep(1)

        # -- start the wavemeter if connected -- 
        if wavemeter:
            # check connect
            if not wavemeter.connected:
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
        else:
            self._DCscan.emit((2, laser.lbd, 0, None))

        # -- Setup DAQ for acquisition -- 
        scan_time = np.diff(laser.scan_limit)[0]/laser.scan_speed
        daq = DAQ(t_end = scan_time, dev = daqParam['dev'])
        daq.SetupRead(read_ch=daqParam['read_ch'])
        daq.readtask.start()
        time_start_daq = time.time()
        
        # -- Start laser scan -- 
        laser.scan = True
        self._is_Running = True
        
        # -- Fetch wavelength and progress of scan -- 
        lbd_probe = []
        time_probe = []
        while laser._is_scaning:
            lbd_scan = laser._lbdscan
            lbd_probe.append(lbd_scan)
            time_probe.append(time.time())
            prgs = np.floor(100*(lbd_scan-scan_limit[0])/np.diff(scan_limit)[0])
            self._DCscan.emit((1, lbd_scan, prgs, None))

        # -- Scan Finished, get DAQ data -- 
        daq.readtask.stop()
        time_stop_daq = time.time()
        data = daq.readtask.read(number_of_samples_per_channel=int(daq.Npts))
        daq.readtask.close()

        # -- Get Last wavelength of the scan -- 
        if wavemeter:
            wavemeter.acquire = True
            time.sleep(2)
            lbd_end = wavemeter.lbd
            wavemeter.acquire = False
            self._DCscan.emit((3, lbd_end, 100, None))
        else:
            self._DCscan.emit((3, laser.lbd, 100, None))
        
        # -- Process a bit the data --
        T = data[0]
        MZ = data[1]
        tdaq = np.linspace(time_start_daq,time_stop_daq,len(T))
        tdaq = t-time_start_daq 
        
        # -- Find out the wavelength during the scan --
        time_probe = np.array(time_probe)
        lbd_probe = np.array(lbd_probe)
        time_probe = time_probe - time_probe[0]

        # -- interpolate data for better precision --
        f_int = intpl.splrep(time_probe[:-1], lbd_probe)
        lbd_daq = intpl.splev(t, f_int)

        # -- Return data and= everything --
        to_return = (t_daq, t_probe, lbd_daq, [T, MZ])

        self._DCscan.emit((-1, laser.lbd, 0, to_return))
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