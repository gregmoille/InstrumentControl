from toptica.lasersdk.dlcpro.v2_0_3 import DLCpro, NetworkConnection, DeviceNotFoundError, DecopError, UserLevel
import toptica.lasersdk.utils.dlcpro as utls
import matplotlib.pyplot as plt
import socket
import time
import pandas as pd
import numpy as np


def SetupWideScan(ip = '169.254.122.1'):
    with DLCpro(NetworkConnection(ip)) as dlc:
        print(dlc.laser1.recorder.sample_count_set.set(int(5e6)))
        Npts = dlc.laser1.recorder.sample_count.get()
        print('Sampling Points = {}'.format(Npts))
        scan = [dlc.laser1.wide_scan.scan_begin.get(),
                dlc.laser1.wide_scan.scan_end.get()]
        print('Scan limits: {}'.format(scan))
        step = np.diff(scan)[0]/Npts
        dlc.laser1.wide_scan.shape.set(0)
        dlc.laser1.wide_scan.recorder_stepsize_set.set(step)



    # dlc.laser1.wide_scan.start()
def FetchWideScan(ip = '169.254.122.1'):
    with DLCpro(NetworkConnection(ip)) as dlc:
        Npts = dlc.laser1.recorder.sample_count.get()
        λ = []
        S = []
        MZ = []
        N = 0
        while N < Npts:
            data = utls.extract_float_arrays('xyY',dlc.laser1.recorder.data.get_data(N, 1024))
            λ += list(data['x'])
            S += list(data['y'])
            # MZ += list(data['Y'])
            N += 1024

        df = pd.DataFrame({'λ': λ, 'S': S})
        df.set_index(['λ'], inplace = True)

    return df
#     dlc.system_label.set('Please do not touch!')
#     print(dlc.laser1.recorder)
# # #
# f, ax = plt.subplots()
# ax.plot(data['y'])
# f.show()
