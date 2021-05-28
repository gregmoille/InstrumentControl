import numpy as np
import threading
import os
import plotly.graph_objects as go
import pandas as pd
import sys
import re
from scipy import constants as cts
from IPython.display import display, HTML
import time

work_dir = os.path.join(os.path.dirname(__file__), '../')
work_dir = os.path.abspath(work_dir)
path = os.path.abspath(work_dir + '/../')

if not work_dir in sys.path:
     sys.path.insert(0, work_dir)
from pyOSA import Yokogawa
from pyOSA import uiOSA

# if len(sys.argv)>1:
#     DEBUG = bool(re.search('true', sys.argv[0].lower()))
#     print(f'Debugging: {DEBUG}')
# else:
#     DEBUG = False
# DEBUG = False
# print(DEBUG)



class OSAjupyter(uiOSA):
    OSAmodel = {'AQ6375B': dict(span=[1200.0, 2400.0]),
               'AQ6374': dict(span=[350.0, 1750.0]),
               'AQ6370D': dict(span=[600.0, 1700.0])}


    def __init__(self, **kwargs):
        super().__init__()
        self.DEBUG = kwargs.get('DEBUG', False)
        if self.DEBUG:
            print('Debuging mode ON')
        self.createUI()
        self.connected = False
        self._id_trace = 0
        self._scan = False

        # -- connect the button --
        self._connectUI()

    def connect(self, change):
        ip = self.ui.ip.value
        if change.new:
            try_connect = 0
            while try_connect < 5:
                with Yokogawa(ip=ip) as osa:
                    # -- fetch the OSA state
                    if osa.connected:
                        try_connect += 1
                        print(try_connect)
                        identity  = osa.identity
                        if self.DEBUG:
                            print(f'Model:{identity}')
                            print(f'Model:{self.OSAmodel}')
                            print(f"Model:{self.OSAmodel[identity['model']]}")
                        if self.DEBUG:
                            print('Connected to the OSA')
                        try: 
                            para = osa.settings
                            if self.DEBUG:
                                print('Fetched parameters')
                        except Exception as err:
                            print(err)
                            
                        trace = osa.trace
                        if self.DEBUG:
                            print('Fetched traces')
                        
                        break
                    else:
                        try_connect += 1
                        print('Did not connect, retrying...')
                        time.sleep(0.5)
      
            self.figOSA.data[0].x = []
            self.figOSA.data[0].y = []
            # time.sleep(1)

            # close the socket, no need anymore
            # -- updating the UI
            if try_connect >=5:
                print("Couldn't connect to the OSA, please check the IP")
            else:
                self.connected = True
                if self.DEBUG:
                    print('Finished Connecting')

                model = identity['model']
                if self.DEBUG:
                    print(f"Model: {model}")
                self.ui.model.value =  f"Maker: {identity['maker']}\n"  + \
                                      f"Model: {model}\n" + \
                                      f"SN: {identity['SN']}\n\n" + \
                                      f"Spectral range:\n\t {self.OSAmodel[model]['span'][0]}nm - {self.OSAmodel[model]['span'][1]}nm\n"

                lbd_start = para['centwlgth'] - para['span']/2
                lbd_end = para['centwlgth'] + para['span']/2
                if self.DEBUG:
                    print(f'Start: {lbd_start}')
                    print(f'End: {lbd_end}')

                self.ui.λ.min =  self.OSAmodel[model]['span'][0]
                self.ui.λ.max =  self.OSAmodel[model]['span'][1]
                self.ui.λ.value = (1e9*lbd_start, 1e9*lbd_end)
                try:
                    self.ui.bandwidth.value = self._Bdwt_val[1e9*para['bdwdth']]
                except Exception as err:
                    if self.DEBUG:
                        print(f'Badnwidth Error: {err}')
                        print(f"Value: {1e9*para['bdwdth']}")

                try:
                    self.ui.res.index = int(para['resol'])
                except Exception as err:
                    if self.DEBUG:
                        print(f'Res Error: {err}')
                        print(f"Value: {para['resol']}")
                try:
                    self.ui.pts.value = int(para['pts'])
                except Exception as err:
                    if self.DEBUG:
                        print(f'Pts Error: {err}')
                        print(f"Value: {para['pts']}")

                self.figOSA.data[0].x = trace.lbd.values*1e9
                self.figOSA.data[0].y = trace.S.values
                self.figOSA.update_xaxes(autorange = True)
                self.figOSA.update_xaxes(autorange = False)
                self.figOSA.update_xaxes(range = [self.figOSA.layout.xaxis.range[0],
                                            self.figOSA.layout.xaxis.range[1]])

                self.figOSA.update_yaxes(autorange = True)
                time.sleep(0.2)
                self.figOSA.update_yaxes(autorange = False)
                self.figOSA.update_yaxes(range = [-59, self.figOSA.layout.yaxis.range[-1]])
                time.sleep(0.5)
                self.figOSA.update_yaxes(range = [-85, self.figOSA.layout.yaxis.range[-1]])

        else:
            self.connected = False

    def refreshTrace(self, change):
        ip = self.ui.ip.value
        if self.connected:
            with Yokogawa(ip=ip) as osa:
                if osa.connected:
                    trace = osa.trace

            x = trace.lbd*1e9
            y = trace.S
            if self.ui.freq_scale.value.lower() == 'frequency':
                x = 1e-12*cts.c/(x*1e-9)

            self.figOSA.data[0].x = x
            self.figOSA.data[0].y = trace.S


    def _stopScan(self):
        self._scan = False
        ip = self.ui.ip.value
        print(ip)
        time.sleep(0.5)
        with Yokogawa(ip=ip) as osa:
            osa.scan = 'stop'
            print('stopped')
            self._scan = False
        
    
    def _singleScan(self):
        self._scan = True
        
        ip = self.ui.ip.value
        
        with Yokogawa(ip=ip) as osa:
            
            self.figOSA.data[0].x = []
            self.figOSA.data[0].y = []
            osa.scan = 'single'
            print('Launching a single scan')
            while True: 
                print('getting traces')
                time.sleep(0.01)
                trace = osa.trace
                if trace: 
                    x = trace.lbd*1e9
                    y = trace.S
                    if self.ui.freq_scale.value.lower() == 'frequency':
                        x = 1e-12*cts.c/(x*1e-9)
                    self.figOSA.data[0].x = x
                    self.figOSA.data[0].y = trace.S
                else:
                    print(trace)
                time.sleep(0.25)
                if self._scan == False: 
                    print('!!!stop the loop!!!')
                    break

    def _repeatScan(self):
        self._scan = True
        ip = self.ui.ip.value
        with Yokogawa(ip=ip) as osa:
            print('Launching a Continuous scan')
            self.figOSA.data[0].x = []
            self.figOSA.data[0].y = []
            osa.scan = 'repeat'
            print('Launching a Continuous scan')
            while True: 
                time.sleep(0.01)
                trace = osa.trace
    
                if not(trace is None): 
                    x = trace.lbd*1e9
                    y = trace.S
                    if self.ui.freq_scale.value.lower() == 'frequency':
                        x = 1e-12*cts.c/(x*1e-9)
                    self.figOSA.data[0].x = x
                    self.figOSA.data[0].y = trace.S
                else:
                    time.sleep(0.25)
                if self._scan == False: 
                    print('!!!stop the loop!!!')
                    break
         
    def scanType(self, change):
        print(change.new.lower())
        if change.new.lower() == 'stop':
            self._stopScan()
        if not self._scan:
            if change.new.lower() == 'single':
                t = threading.Thread(target=self._singleScan)
                t.start()
            if change.new.lower() == 'repeat':
                t = threading.Thread(target=self._repeatScan)
                t.start()

    def select_trace(self, change):
        ip = self.ui.ip.value
        if self.connected:
            with Yokogawa(ip=ip) as osa:
                osa.trace = change.new.replace('Trace ', '')

    def update_λ(self, change):
        ip = self.ui.ip.value
        if self.connected:
            # print(change.new)
            centwlgth =  (change.new[1] + change.new[0])/2
            span = (change.new[1] - change.new[0])
            time.sleep(1)
            with Yokogawa(ip=ip) as osa:
                para = osa.settings
            
            if self.DEBUG:
                print(para)
            para['centwlgth'] = centwlgth*1e-9
            para['span'] = span*1e-9
            if self.DEBUG:
                print(para)
            with Yokogawa(ip=ip) as osa:
                osa.settings = para
            self.figOSA.update_xaxes(range = change.new)

    def update_res(self, change):
        ip = self.ui.ip.value
        if self.connected:
            with Yokogawa(ip=ip) as osa:
                para = osa.settings
            para['resol'] = change.new
            with Yokogawa(ip=ip) as osa:
                osa.settings = para

    def update_bdwt(self, change):
        ip = self.ui.ip.value
        if self.connected:
            with Yokogawa(ip=ip) as osa:
                para = osa.settings
            para['bdwdth'] = float(change.new.replace(' nm', ''))*1e-9
            with Yokogawa(ip=ip) as osa:
                osa.settings = para
                para = osa.settings
            self.ui.bandwidth.value = self._Bdwt_val[1e9*para['bdwdth']]

    def update_points(self, change):
        ip = self.ui.ip.value
        if self.connected:
            with Yokogawa(ip=ip) as osa:
                para = osa.settings
            para['pts'] = change.new
            with Yokogawa(ip=ip) as osa:
                osa.settings = para
                para = osa.settings
            self.ui.pts.value = int(para['pts'])

    def clear_all_trace(self, change):
        self._id_trace = 0
        self.figOSA.data = [self.figOSA.data[0]]
        self.figOSA.data[0].x = []
        self.figOSA.data[0].y = []

    def clear_keep_trace(self, change):
        self._id_trace = 0
        self.figOSA.data = [self.figOSA.data[0]]

    def keep_trace(self, change):
        self._id_trace += 1
        print('Keeping trace')
        tr = go.Scatter(x = self.figOSA.data[0].x,
                         y = self.figOSA.data[0].y)
        self.figOSA.add_trace(tr)
        print('Trace kept')

    def freq_scale(self, change):
        print(change.new.lower)

        xdata = [None]*len(self.figOSA.data)
        newx = [None]*len(self.figOSA.data)

        for ii in range(len(self.figOSA.data)):
            xdata[ii] = self.figOSA.data[ii].x

        if change.new.lower() == 'frequency':
            for ii in range(len(self.figOSA.data)):
                 newx[ii] =  1e-12 * cts.c/(xdata[ii]*1e-9)
            xlabel = 'Frequency (THz)'

        elif change.new.lower() == 'wavelength':
            for ii in range(len(self.figOSA.data)):
                 newx[ii] =  1e-12 * cts.c/(xdata[ii]*1e-9)
            xlabel = 'Wavelength (nm)'

        for ii in range(len(self.figOSA.data)):
            self.figOSA.data[ii].x = newx[ii]
        self.figOSA.update_xaxes(title = xlabel, range = [np.min(newx), np.max(newx)])

    #     print(change.new)
    #     if change.new:
    #         newx =  1e-12 * cts.c/(xdata*1e-9)
    #         xlabel = 'Frequency (THz)'
    #     else:
    #         newx =  1e9 * cts.c/(xdata*1e12)
    #         xlabel = 'Wavelength (nm)'
    #
    #     self.figOSA.data[0].x = newx
    #     # figOSA.data[0].y = ydata
    #     self.figOSA.update_xaxes(title = xlabel, range = [newx.min(), newx.max()])
    # #

    def save_data(self, change):
        ip = self.ui.ip.value
        fname = self.ui.picker.selected

        if fname:
            if not os.path.exists(self.ui.picker.selected):
                if self.ui.to_save.value.lower() == 'pc':
                    lbd = self.figOSA.data[0].x*1e-9
                    S = self.figOSA.data[0].y
                    df = pd.DataFrame(dict(lbd = lbd, S = S))

                    if len(self.figOSA.data) > 1:
                        for ii in range(1, len(self.figOSA.data)):
                            lbd = self.figOSA.data[0].x*1e-9
                            S = self.figOSA.data[0].y
                            dum = pd.DataFrame({f'lbd{ii}': lbd, f'S{ii}': S})
                            df = pd.concat([df, dum], axis = 1)
                    df.to_parquet(fname)
                else:
                    with Yokogawa(ip=ip) as osa:
                        if osa.connected:
                            trace = osa.trace
                            save_ok = True
                        else:
                            save_ok = False
                            print("Cannot coonect!!")
                    if save_ok:
                        trace.to_parquet(fname)

    def _connectUI(self):
        self.ui.cnct.observe(self.connect, 'value')
        # self.ui.scan.observe(self.scan_osa,'value')
        self.ui.refresh_trace.on_click(self.refreshTrace)
        self.ui.trace.observe(self.select_trace, 'value')
        self.ui.λ.observe(self.update_λ, 'value')
        self.ui.bandwidth.observe(self.update_bdwt, 'value')
        self.ui.pts.observe(self.update_points, 'value')
        self.ui.res.observe(self.update_res, 'index')
        self.ui.clr.on_click(self.clear_all_trace)
        self.ui.clr_keep.on_click(self.clear_keep_trace)
        self.ui.keep.on_click(self.keep_trace)
        self.ui.save.on_click(self.save_data)
        self.ui.freq_scale.observe(self.freq_scale, 'value')
        
        self.ui.scan.observe(self.scanType, 'value')


# # ----------------------------------
# # -- Worker for scanning
# # ----------------------------------
# run_thread = True
# def worker(f, instr):
#     while run_thread:
#         try:
#             #with Yokogawa(ip=ip) as instr:
#             trace = instr.trace
#     #         x = np.linspace(600, 1700, 50001)
#     #         y = np.log10(np.random.rand(50001)*(1/np.cosh((x-(700+1850)/2)/10))**2)
#             f.data[0].x = trace.lbd.values*1e9
#             f.data[0].y = trace.S.values
#         except:
#             print('Comunication error')
#             time.sleep(0.1)
#             #with Yokogawa(ip=ip) as instr:
#             trace = instr.trace
#     #       x = np.linspace(600, 1700, 50001)
#     #       y = np.log10(np.random.rand(50001)*(1/np.cosh((x-(700+1850)/2)/10))**2)
#             f.data[0].x = trace.lbd.values*1e9
#             f.data[0].y = trace.S.values
#         time.sleep(0.1)
#
#
#
# # ----------------------------------
# # -- Setup the Connectors
# # ----------------------------------
#
#
# def scan_osa(change):
#     global thread_osa
#     global run_thread
#     run_thread = False
#     ip = ui.ip.value
#     if connected:
#         # osa.scan = change.new.lower()
#         run_thread = False
#         if change.new.lower() == 'single' or change.new.lower() == 'repeat':
#             with Yokogawa(ip=ip) as osa:
#                 osa.scan = change.new.lower()
#                 run_thread = True
#                 thread_osa = threading.Thread(target=worker, args=(figOSA, osa))
#                 thread_osa.start()
#         if change.new.lower() == 'stop':
#             with Yokogawa(ip=ip) as osa:
#                 osa.scan = change.new.lower()
#             print('Trying to kill the stuff')
#             run_thread = False
#



#


# # ----------------------------------
# #  -- connect callbacks and traits
# # ----------------------------------
# ui.cnct.observe(connect, 'value')
# ui.scan.observe(scan_osa,'value')
# ui.trace.observe(select_trace, 'value')
# ui.λ.observe(update_λ, 'value')
# ui.bandwidth.observe(update_bdwt, 'value')
# ui.pts.observe(update_points, 'value')
# ui.res.observe(update_res, 'index')
# ui.clr.on_click(clear_trace)
# ui.save.on_click(save_data)
# ui.freq_scale.observe(freq_scale, 'value')
#
#
# # ----------------------------------
# #  -- Display
# # ----------------------------------
# box_layout =  wdg.Layout(display='flex',
#                     flex_flow='column',
#                     flex_wrap = 'wrap',
#                     align_content =  'stretch',
#                     justify_content =  'center',
#                     align_items='stretch',
#                     width='28%')
# outp_layout =  wdg.Layout(display='flex',
#                     flex_flow='column',
#                     flex_wrap = 'wrap',
#                     align_content =  'stretch',
#                     justify_content =  'center',
#                     align_items='stretch',
#                     width='72%')
# ui.picker.layout = wdg.Layout(display='flex',
#                     flex_flow='column',
#                     flex_wrap = 'wrap',
#                     align_content =  'stretch',
#                     justify_content =  'center',
#                     align_items='stretch',
#                     width='100%')
# cc = [ui.cnct,ui.freq_scale, ui.ip,ui.scan, ui.trace, ui.res,ui.bandwidth, ui.pts,ui.λ, ui.clr,ui.save,ui.picker]
# ctrl = wdg.Box(children = cc,layout = box_layout)
# otp = wdg.Box(children = [figOSA], layout = outp_layout)
# display(wdg.HBox([ctrl, otp]))
