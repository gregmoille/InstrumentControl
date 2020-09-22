from functools import wraps
from datetime import datetime
import time
from toptica.lasersdk.dlcpro.v2_0_3 import DLCpro, NetworkConnection, DeviceNotFoundError, DecopError, UserLevel
import sys
import numpy as np
import threading
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import ipdb
import scipy.io as io
from copy import copy
from matplotlib.animation import FuncAnimation
import h5py
from nidaqmx.constants import AcquisitionType, TaskMode
import nidaqmx
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, interactive, Layout
import nest_asyncio
nest_asyncio.apply()
import pandas as pd
from IPython.display import clear_output, display
import sys
path = os.path.realpath(r'Z:\GoogleDrive\Work\ExperimentalSetup\PythonSoftware\InstrumentControl')
if not path in sys.path:
    sys.path.insert(0, path)
from pyLaser import NewFocus6700
import TransmissionSetup as Tsetup
import numpy as np
import time
from nidaqmx.constants import AcquisitionType, TaskMode
import nidaqmx


def SetupNfScan(laser, lbd_scan = [765.0, 781.0], duration = 20):
    scan_width = np.abs(np.diff(lbd_scan)[0])
    laser.scan_limit = lbd_scan
    laser.scan_speed = scan_width/duration
    print('Scan limits: {}'.format(laser.scan_limit))
    time.sleep(0.5)
    print('Scan Duration: {}'.format(scan_width/laser.scan_speed))
    time.sleep(0.5)
    print('Waiting to park the laser....')
    lsr.lbd = lbd_scan[0]
    while True:
        time.sleep(0.2)
        if (lsr.lbd-lbd_scan[0]<0.1):
            break
                        
    time.sleep(3)
    print('DONE. Ready for scan')
                        
def ScanNf(lsr, device = 'cDAQ9181', duration= 20, clk = 1e6, ch = ['ai0', 'ai1', 'ai2']):
    duration = duration+5
    system = nidaqmx.system.System.local()
    dev = device
    device = system.devices[dev]
    device.reset_device()
    Npts = (duration)*clk
    print('Sampling Points = {}'.format(Npts))
    
    readtask = nidaqmx.Task()
    ch = dev + '/' +  ',{}/'.format(dev).join(ch)
    readtask.ai_channels.add_ai_voltage_chan(ch,min_val=-5, max_val=10)
    readtask.timing.cfg_samp_clk_timing(clk, sample_mode=AcquisitionType.FINITE,samps_per_chan=int(Npts))
    readtask.start()
    time.sleep(1)
    
    lsr.scan = True

    time.time()
    #     time.sleep(duration)
    start = time.time()
    while time.time()-start<=duration:
        pass
    #         clear_output(wait=True)
    #         print('Remaining time: {:.1f} s'.format(duration - (time.time()-start)), end = '\r')
    data =[]
    data += readtask.read(number_of_samples_per_channel=int(Npts))
    print('*'*30)
    print('Got DAQ data')
    readtask.stop()
    readtask.close()
    data = np.array(data)
    
    dfraw = pd.DataFrame({'S':data[0], 'V': data[1]})
    return dfraw


## do the tranmission

import gc
import time
dur = 20
clk = 1e6
lbd_scan = [765.0, 781.0]
channels = ['ai0', 'ai2']
SetupNfScan(lsr, duration= dur, )
df = ScanNf(lsr, duration= dur, ch = channels, clk = 1e6)
time.sleep(1)
gc.collect()


## display the data

start = df.V.loc[:1000].mean()
noise = df.V.loc[:1000].max() -  df.V.loc[:1000].min()
end = df.V.loc[df.V.size-1000: df.V.size].mean()

ind_start = np.where(df.V>start+2*noise)[0][0]
ind_end = np.where(df.V<end-2*noise)[0][-1]


S = df.S.loc[ind_start:ind_end]
V = df.V.loc[ind_start:ind_end]
lbd = np.linspace(lbd_scan[0], lbd_scan[-1], V.shape[0])
tr = [go.Scatter(x = lbd[::1000], y = S[::1000] ,name = 'S')]
# tr += [go.Scatter(y = V[::1000]/V.max() ,name = 'v')] 
iplot(go.Figure(data = tr))

#save the data

import os
import pandas as pd

[500, 520, 540, 560, 580]
[100, 150, 200, 250, 300, 350, 400, 450]


RW = 500
G = 250

path = './Data/Linear/NormalRings/Pol0/'
fname = 'RW{}G{}'.format(RW, G)
if os.path.exists(os.path.join(path,fname) + '.parquet'):
    print('FILE ALREADY EXIST!!!!')
else:
    print('Saving file : {}'.format(fname))
    df.to_parquet('{}.parquet'.format(os.path.join(path,fname)))
    
