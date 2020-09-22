try:
    from nidaqmx.constants import AcquisitionType, TaskMode
    import nidaqmx
except:
    pass


class DAQ(object):
    '''
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


    def __init__(self, **kwargs):
        super(DAQ, self).__init__()
        self.t_end = kwargs.get('t_end', None)
        self._dev = kwargs.get('dev', None)
        self.clock = kwargs.get('clock', 0.75e6)
        self.Npts = self.t_end*self.clock
        
        system = nidaqmx.system.System.local()
        self.device = system.devices[self._dev]
        self.device.reset_device()
        
    def SetupWrite(self,**kwargs):
        

        t_end = self.t_end
        self.write_ch = kwargs.get('write_ch', [])
        if not type(self.write_ch) == list:
            self.write_ch = [self.write_ch]

        self.write_ch = self._dev + '/' + ''.join(self.write_ch)
        writetask = nidaqmx.Task()
        writetask.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        writetask.timing.cfg_samp_clk_timing(int(self.clock),
                                                        sample_mode=AcquisitionType.CONTINUOUS,
                                                        samps_per_chan=int(Npts))
        # AcquisitionType.FINITE,
        self.writetask = writetask
        return writetask

    def SetupRead(self, **kwargs):
        
        t_end = self.t_end
        self.read_ch = kwargs.get('read_ch', [])
        if not type(self.read_ch) == list:
            self.read_ch = [self.read_ch]
        self.Nch_read = len(self.read_ch)
        # self.Npts = self.Npts/self.Nch_read
        # print("Npts= {}".format(self.Npts))
        self.read_ch = self._dev + '/' +  ',{}/'.format(self._dev).join(self.read_ch)
        Npts = self.Npts
        readtask = nidaqmx.Task()
        readtask.ai_channels.add_ai_voltage_chan(self.read_ch)
        readtask.timing.cfg_samp_clk_timing(int(self.clock),\
                                                    sample_mode=AcquisitionType.CONTINUOUS,
                                                    samps_per_chan=int(self.Npts))

        self.readtask = readtask
        return readtask

    def DoTask(self):
        # t_end = self.t_end
        # if hasattr(self, 'writetask'):
        #     self.writetask.write(write, auto_start=False)
        #     self.writetask.start()
        # if hasattr(self, 'readtask'):
        data = self.readtask.read(number_of_samples_per_channel=int(self.Npts))
        self.data = data

       
        # if hasattr(self, 'writetask'):
        #     self.writetask.close()
        # if hasattr(self, 'readtask'):
        # self.readtask.close()
        return data


if __name__ == '__main__':

    import scipy.signal as sig
    import matplotlib.pyplot as plt
    import ipdb
    import numpy as np

    def Triangle_shape(T,Vmax, Vmin, Npts):
        # here define a triangular shape function with repeat twice
        # to be sure we can read a full period with the daq
        down = lambda x : x *(Vmin-Vmax)/(T*0.5) + Vmax
        up = lambda x : x *(Vmax-Vmin)/(T*0.5)
        t = np.linspace(0, 2*T, Npts)    
        x = t[np.where(t<T/2)]
        ydown = list(down(x))
        yup = list(up(x))
        y = ydown + yup 
        to_add = int(t.size/4)
        y = list(np.zeros(to_add)) + y + list(np.zeros(to_add))

        # ipdb.set_trace()
        # assert len(y) == len(t)
        return (t, np.array(y))


    T = 0.1
    Vmax = 5   
    Vmin = 0
    daq = DAQ(t_end = 2*T, dev = 'Dev1')
    t, write = Triangle_shape(T, Vmax, Vmin, daq.Npts)
    ind_T =  np.where(t<=T)[0][-1]

    f, ax = plt.subplots()
    ax.plot(t,write)
    lines = ax.plot(t,write, '.', ms = 4)
    lines2 = ax.plot(t,write)

    ind = (np.diff(np.sign(np.diff(write))) < 0).nonzero()[0] + 1
    ind = [ind[0], ind[0] + ind_T]
    lines3 = ax.plot(t[ind], write[ind], 'v', ms = 6)
    ipdb.set_trace()
    while True:
        try:
            nt = int(daq.Npts/2)
            daq.SetupRead(read_ch = 'ai0:1')
            daq.SetupWrite(write_ch = 'ao0')
            data = daq.DoTask()

            Trans  = np.array(data[0])
            probe = np.array(data[1])
            box = np.ones(int(len(probe)/nt))/(len(probe)/nt)
            y_smooth = np.convolve(probe, box, mode='same')
            ind = (np.diff(np.sign(np.diff(y_smooth))) < 0).nonzero()[0] + 1
            ind = ind[y_smooth[ind]>Vmax/2][0]
            limd_T =  [ind,ind + ind_T]
            t_sync = t[ind]
            t_marker = t[limd_T]- t_sync
            # ipdb.set_trace()
            

            lines[0].set_data([t-t_sync,Trans])
            lines2[0].set_data([t,y_smooth])

           


            lines3[0].set_data([t_marker, Trans[limd_T]])
            f.canvas.draw()
            
            plt.pause(0.05)

        except KeyboardInterrupt:
            break