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

class TransmissionWorkers():
    '''
    ------------------------------------------------------
    tw = TransmissionWorkers(laser = <class>, 
                            wavemeter = <class>,
                            *args, **kwargs) 

    Class for Transmission characterization of nanodevices.
    ------------------------------------------------------
    Args:
        laser: laser object to control the equipement (c.f.
                pyNFLaser package)
        wavemeter: wavemeter object to controll the
                   equipement (c.f. pyWavemeter package)
        If no wavemeter if passed, the class will work 
        without it and will trust the wavelength provided
        byt the laser internal detector
    Methods:
        self.DCscan: See method doc string
        self.PiezoScan: See method doc string

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

    _DCscan = (None, None, None, None)

    def __init__(self, **kwargs):
        super(TransmissionWorkers, self).__init__()

        # Setup pyQt Signal
        # ---------------------------------------------
        self._PiezoScan = pyqtSignal(tuple)

        # Retrieve equipement
        # ---------------------------------------------
        

        # Misc
        self._is_Running = False

    def DCscan(self, **kwargs):
        '''
        ------------------------------------------------------
        self.DCscan(self, param = <dict>, *args, **kwargs))

        Args: 
            laser: object of a laser from pyNFLaser
            wavemeter: wavementer object from pyWavemeter
            param: dictionarry with 'laserParam', 
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
        Return <tuple>:
            (t, lbd_daq, [T, MZ])
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
        '''
        


        laser = kwargs.get('laser', None)
        wavemeter = kwargs.get('wavemeter',None)
        
        # More user frienldy notation
        # ---------------------------------------------
        param = kwargs.get('param', None)
        daqParam = param['daqParam']
        wlmParam = param.get('wlmParam', None)


        #wait a bit for stabilization
        time.sleep(1)
        # start the wavemeter if connected
        # ---------------------------------------------
        if wavemeter:
            # check connect
            if not wavemeter.connected:
                wavemeter.connected = 'hide'
                time.sleep(1)
            wavemeter.pulsemode = False
            wavemeter.widemode = False
            wavemeter.fastmode = False
            wavemeter.channel = wlmParam['channel']
            wavemeter.exposure = 'auto'

        # # Go to start of the scan
        # # ---------------------------------------------
        # laser.lbd = laserParam['scan_limit'][0]
        # time.sleep(0.1)
        # Display wavelength changing with
        # ---------------------------------------------
        while laser._is_changing_lbd:
            # ipdb.set_trace()
            print("chanign lbd")
            # self._DCscan.emit((0, laser.lbd, 0, True))
            

        # Get First wavelength of the scan
        # ---------------------------------------------
        if wavemeter:
            # get it through the wavemeter
            wavemeter.acquire = True
            print('Getting wavemeter')
            time.sleep(1)
            lbd_start = wavemeter.lbd
            wavemeter.acquire = False
            self._DCscan.emit((2, lbd_start, 0, True))
        else:
            self._DCscan.emit((2, laser.lbd, 0, True))

        # Setup DAQ for acquisition
        # ---------------------------------------------
        # ipdb.set_trace()
        scan_time = np.diff(laser.scan_limit)[0]/laser.scan_speed
        # daq = DAQ(t_end = scan_time, dev = daqParam['dev'])
        # daq.SetupRead(read_ch=daqParam['read_ch'])
        # daq.readtask.start()
        time_start_daq = time.time()
        # Start laser scan
        # ---------------------------------------------
  
        laser.scan = True
        self._is_Running = True
        # daq.ReadData()

        # Fetch wavelength and progress of scan
        # ---------------------------------------------
        lbd_probe = []
        time_probe = []
        while laser._is_scaning:
            lbd_scan = laser._lbdscan
            # lbd_probe.append(lbd_scan)
            # time_probe.append(time.time())
            prgs = np.floor(100*(lbd_scan-laserParam['scan_limit'][0])/np.diff(laserParam['scan_limit'])[0])
            self._DCscan.emit((1, lbd_scan, prgs, True))
            print(prgs)
        # daq.readtask.stop()
        time_stop_daq = time.time()
        
        # Get Last wavelength of the scan
        # ---------------------------------------------
        if wavemeter:
            # get it through the wavemeter
            wavemeter.acquire = True
            print('Getting wavemeter')
            time.sleep(1)
            lbd_end = wavemeter.lbd
            wavemeter.acquire = False
            self._DCscan.emit((3, lbd_end, 100, True))
        else:
            self._DCscan.emit((3, laser.lbd, 100, True))
   
        # Retrieve DAQ red data
        # ---------------------------------------------
        # Ntry = 0
        # while Ntry<10:
            # try:
        # data = daq.readtask.read(number_of_samples_per_channel=int(daq.Npts/2))
        
            # except Exception as e: 
            #     print(e)
            #     time.sleep(2)
            #     Ntry += 1
        
        # T = data[0]
        # MZ = data[1]
        # t = np.linspace(time_start_daq,time_stop_daq,len(T))
        # t = t-time_start_daq 
        
        # Find out the wavelength during the scan
        # ---------------------------------------------
        # time_probe = np.array(time_probe)
        # lbd_probe = np.array(lbd_probe)
        # time_probe = time_probe - time_probe[0]

        # ipdb.set_trace()
        # intpl.splrep(time_probe[:-1], lbd_probe)
        # lbd_daq = intpl.splev(t, f_int)

        # Return data and emit everything
        # to_return = (t, lbd_daq, [T, MZ])

        # self._DCscan.emit(-1, to_return, 0, False)
        self._DCscan.emit((-1, 0, 0, False))
        self._is_Running = False
        # print("Nprobe laser {}".format(len(lbd_probe)))
        # return to_return

    def PiezoScan(self, **kwargs):
        '''
        self.PiezoScan(self, param = <dict>, *args, **kwargs))
        '''
        # Create the pattern to write to the DAQ

        self._is_Running = True
        while self._is_Running:
            daq.SetupReadDaq(daqParam)
            daq.SetupWriteDaq(daqParam)
            Data = daq.GetData()

        # PostProcess to stabilize read/write



    def FreeScan(self, **kwargs):
        pass

    def MZpostProces(self, **kwargs):
        pass

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