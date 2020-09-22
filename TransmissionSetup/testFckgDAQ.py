
from nidaqmx.constants import AcquisitionType, TaskMode
import nidaqmx
import numpy as np
import time


fSampling = 0.75e6
dtMax = 2 #seconds
data = []
ttot = 0
Npts = int(1e5)
data = np.zeros(Npts,)
system = nidaqmx.system.System.local()
device = system.devices['Dev1']
device.reset_device()

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(fSampling)
    test = nidaqmx.stream_readers.AnalogSingleChannelReader(test)
    test.read_many_sample(data, number_of_samples_per_channel=1e5)