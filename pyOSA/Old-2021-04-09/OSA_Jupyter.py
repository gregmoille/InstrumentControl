import numpy as np
from ipywidgets import widgets as wdg
import matplotlib.pyplot as plt
import threading
from ipyfilechooser import FileChooser
from matplotlib.animation import FuncAnimation
import os
import plotly.graph_objects as go
import pandas as pd
import sys
import re
from scipy import constants as cts
from IPython.display import display, HTML
import time
from IPython.display import clear_output
# print('*'*60)
# print()

work_dir = os.path.join(os.path.dirname(__file__), '../')
work_dir = os.path.abspath(work_dir)
path = os.path.abspath(work_dir + '/../')
# print(work_dir)

if not work_dir in sys.path:
     sys.path.insert(0, work_dir)
     # print(work_dir)
from pyOSA import Yokogawa



print(sys.argv)
xlim = [ float(re.findall("\d+",sys.argv[1])[0]),
        float(re.findall("\d+",sys.argv[2])[0])]
print(xlim)


if len(sys.argv)>3:
    print(sys.argv[3])
    DEBUG = True
else:
    DEBUG = False





# ----------------------------------
# -- Setup the plot
# ----------------------------------
height = 1000
x = np.linspace(xlim[0], xlim[1], 100000)
y = np.log10((1/np.cosh((x-(700+1850)/2)/10))**2)
tr = go.Scatter(x =x, y =y)
figOSA = go.FigureWidget(data=tr)
figOSA.update_xaxes(title = 'Wavelength (nm)', range = [xlim[0], xlim[1]],
                showspikes = True, spikethickness= 1)
figOSA.update_yaxes(title = 'Power (dBm)', range = [-90, 20],
                showspikes = True, spikethickness= 1)
figOSA.update_layout(height = height)

# ----------------------------------
# -- Setup the UI
# ----------------------------------
class _dic2struct():
    def __init__(self, d, which='sim', do_tr=True):
        self._dic = d
        for a, b in d.items():
           setattr(self, a, _dic2struct(b) if isinstance(b, dict) else b)
    def __repr__(self):
        return str(list(self._dic.keys()))
dd = {}
dd['cnct'] =  wdg.Checkbox(value = False, description = "Connected")
dd['freq_scale'] =  wdg.Checkbox(value = False, description = "Frequency ?")
dd['ip'] =  wdg.Text(value = '10.0.0.11', description = 'IP:')
dd['λ'] = wdg.IntRangeSlider(value = (xlim[0], xlim[1]),
                                min =xlim[0], max = xlim[1], step = 5,
                                description = 'λ',
                            continuous_update=False)
dd['pts'] = wdg.IntSlider(value = 50000,
                                min =10, max = 100000, step = 100,
                                description = 'Points:',
                            continuous_update=False)
dd['pts'].add_class("osa_wavelength")
dd['scan'] = wdg.ToggleButtons(options=['Single', 'Repeat', 'Stop'],
                               value = 'Stop',
                               description='Scan:',disabled=False,
                               button_style = 'info')
dd['scan'].add_class("osa_scan_button")

dd['trace'] = wdg.Dropdown(options=['Trace A', 'Trace B', 'Trace C', 'Trace D'],
                               value = 'Trace A',
                           description='Trace:')

dd['res'] = wdg.Dropdown(options=['Norm/Hold', 'Norm/Auto', 'Mid', 'High 1', 'High 2', 'High 3'],
                           description='Resolution:')


Bdwt_val = {0.02: '0.02 nm',
            0.05: '0.05 nm',
            0.1: '0.1 nm',
            0.2: '0.2 nm',
            0.5: '0.5 nm',
            1: '1 nm',
            2: '2 nm'}

dd['bandwidth'] = wdg.SelectionSlider(description='Bandwidth:',
                                          options=Bdwt_val.values(),
                                         continuous_update=False)

dd['bandwidth'].add_class("osa_bandwidth")
dd['clr'] = wdg.Button(description = 'Clear Trace',button_style = 'info',tooltip='Click me',)
dd['clr'].add_class("osa_clear")
dd['save'] = wdg.Button(description = 'Save Spectra',button_style = 'info')
dd['save'].add_class("osa_save")
dd['picker'] = FileChooser('./../')
dd['picker'].use_dir_icons = True
dd['picker'].rows = 5
dd['picker'].width = 200
ui = _dic2struct(dd)

# ----------------------------------
# -- Worker for scanning
# ----------------------------------
run_thread = True
def worker(f, instr):
    while run_thread:
        try:
            #with Yokogawa(ip=ip) as instr:
            trace = instr.trace
    #         x = np.linspace(600, 1700, 50001)
    #         y = np.log10(np.random.rand(50001)*(1/np.cosh((x-(700+1850)/2)/10))**2)
            f.data[0].x = trace.lbd.values*1e9
            f.data[0].y = trace.S.values
        except:
            print('Comunication error')
            time.sleep(0.1)
            #with Yokogawa(ip=ip) as instr:
            trace = instr.trace
    #       x = np.linspace(600, 1700, 50001)
    #       y = np.log10(np.random.rand(50001)*(1/np.cosh((x-(700+1850)/2)/10))**2)
            f.data[0].x = trace.lbd.values*1e9
            f.data[0].y = trace.S.values
        time.sleep(0.1)

# ----------------------------------
# -- Setup the Connectors
# ----------------------------------
connected = False
def connect(change):
    global connected
    global osa
    ip = ui.ip.value
    if change.new:
        connected = True
        with Yokogawa(ip=ip) as osa:
            try:
                para = osa.settings
            except Exception as err:
                if DEBUG:
                    print(f'Param fetching: {err}')
            try:
                trace = osa.trace
            except Exception as err:
                if DEBUG:
                    print(f'Trace fetching: {err}')

            lbd_start = para['centwlgth'] - para['span']/2
            lbd_end = para['centwlgth'] + para['span']/2
            # print((1e9*lbd_start, 1e9*lbd_end))
            #ax.set_xlim([1e9*lbd_start, 1e9*lbd_end])

            figOSA.update_xaxes(range = [1e9*lbd_start, 1e9*lbd_end])
            ui.λ.value = (1e9*lbd_start, 1e9*lbd_end)
            ui.bandwidth.value = Bdwt_val[1e9*para['bdwdth']]
            try:
                ui.res.index = int(para['resol'])
            except:
                pass
            try:
                ui.pts.value = int(para['pts'])
            except:
                pass

            # time.sleep(0.5)
        print(traces)
        figOSA.data[0].x = trace.lbd.values*1e9
        figOSA.data[0].y = trace.S.values
        printt('Finished Connecting')
    else:
        connected = False


def scan_osa(change):
    global thread_osa
    global run_thread
    run_thread = False
    ip = ui.ip.value
    if connected:
        # osa.scan = change.new.lower()
        run_thread = False
        if change.new.lower() == 'single' or change.new.lower() == 'repeat':
            with Yokogawa(ip=ip) as osa:
                osa.scan = change.new.lower()
                run_thread = True
                thread_osa = threading.Thread(target=worker, args=(figOSA, osa))
                thread_osa.start()
        if change.new.lower() == 'stop':
            with Yokogawa(ip=ip) as osa:
                osa.scan = change.new.lower()
            print('Trying to kill the stuff')
            run_thread = False


def select_trace(change):
    ip = ui.ip.value
    if connected:
        with Yokogawa(ip=ip) as osa:
            osa.trace = change.new.replace('Trace ', '')

def update_λ(change):
    ip = ui.ip.value
    if connected:
        # print(change.new)
        centwlgth =  (change.new[1] + change.new[0])/2
        span = (change.new[1] - change.new[0])
        with Yokogawa(ip=ip) as osa:
            para = osa.settings
            para['centwlgth'] = centwlgth*1e-9
            para['span'] = span*1e-9
            print(para)
            osa.settings = para

        figOSA.update_xaxes(range = change.new)

def update_res(change):
    ip = ui.ip.value
    if connected:
        para = osa.settings
        para['resol'] = change.new
        with Yokogawa(ip=ip) as osa:
            osa.settings = para

def update_bdwt(change):
    ip = ui.ip.value
    if connected:
        para = osa.settings
        para['bdwdth'] = float(change.new.replace(' nm', ''))*1e-9
        with Yokogawa(ip=ip) as osa:
            osa.settings = para
            para = osa.settings
        ui.bandwidth.value = Bdwt_val[1e9*para['bdwdth']]

def update_points(change):
    ip = ui.ip.value
    if connected:
        para = osa.settings
        para['pts'] = change.new
        with Yokogawa(ip=ip) as osa:
            osa.settings = para
            para = osa.settings
        ui.pts.value = int(para['pts'])

def clear_trace(change):
    figOSA.data[0].x = []
    figOSA.data[0].y = []

def freq_scale(change):
    xdata = figOSA.data[0].x
    # ydata = figOSA.data[0].y
    print(change.new)
    if change.new:
        newx =  1e-12 * cts.c/(xdata*1e-9)
        xlabel = 'Frequency (THz)'
    else:
        newx =  1e9 * cts.c/(xdata*1e12)
        xlabel = 'Wavelength (nm)'

    figOSA.data[0].x = newx
    # figOSA.data[0].y = ydata
    figOSA.update_xaxes(title = xlabel, range = [newx.min(), newx.max()])


def save_data(change):
    ip = ui.ip.value
    fname = ui.picker.selected
    if fname:
        if not os.path.exists(ui.picker.selected):
            with Yokogawa(ip=ip) as osa:
                trace = osa.trace
            trace.to_parquet(fname)

# ----------------------------------
#  -- connect callbacks and traits
# ----------------------------------
ui.cnct.observe(connect, 'value')
ui.scan.observe(scan_osa,'value')
ui.trace.observe(select_trace, 'value')
ui.λ.observe(update_λ, 'value')
ui.bandwidth.observe(update_bdwt, 'value')
ui.pts.observe(update_points, 'value')
ui.res.observe(update_res, 'index')
ui.clr.on_click(clear_trace)
ui.save.on_click(save_data)
ui.freq_scale.observe(freq_scale, 'value')


# ----------------------------------
#  -- Display
# ----------------------------------
box_layout =  wdg.Layout(display='flex',
                    flex_flow='column',
                    flex_wrap = 'wrap',
                    align_content =  'stretch',
                    justify_content =  'center',
                    align_items='stretch',
                    width='28%')
outp_layout =  wdg.Layout(display='flex',
                    flex_flow='column',
                    flex_wrap = 'wrap',
                    align_content =  'stretch',
                    justify_content =  'center',
                    align_items='stretch',
                    width='72%')
ui.picker.layout = wdg.Layout(display='flex',
                    flex_flow='column',
                    flex_wrap = 'wrap',
                    align_content =  'stretch',
                    justify_content =  'center',
                    align_items='stretch',
                    width='100%')
cc = [ui.cnct,ui.freq_scale, ui.ip,ui.scan, ui.trace, ui.res,ui.bandwidth, ui.pts,ui.λ, ui.clr,ui.save,ui.picker]
ctrl = wdg.Box(children = cc,layout = box_layout)
otp = wdg.Box(children = [figOSA], layout = outp_layout)
display(wdg.HBox([ctrl, otp]))
