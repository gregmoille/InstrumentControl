idLaser = 4106
DeviceKey = '6700 SN60612'
lsr = NewFocus6700(id =idLaser, key = DeviceKey)
lsr.connected = True

daq_ch = ['ai0', 'ai23']

Piezo = Tsetup.PiezoScan(laser = lsr,daq_ch = daq_ch, daq_dev = 'Dev1',
                        daq_probe = 'ai16', daq_write = 'ao0',
                        Vmin = -3, Vmax = 3, Vcoeff = 1,
                        freq_scan = 5, pzt_center = 50)

Free = Tsetup.FreeRun(laser = lsr,daq_ch = ['ai0'], daq_dev = 'Dev1',)

DC = Tsetup.DCScan(laser = lsr, wavemeter = None,
                     daq_ch = daq_ch, daq_dev = 'Dev1',
                    Pmeter_in = None, Pmeter_out = None,
                    Pin_ratio= 10, Pout_ratio= 10)
%matplotlib notebook
