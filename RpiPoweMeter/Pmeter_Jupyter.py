import ipywidgets as widgets
from ipywidgets import HBox, VBox, AppLayout, Layout,GridspecLayout
from threading import Thread
import threading
import time
import numpy as np
import logging
from IPython.display import display, HTML
import visa
import os 
import sys 


work_dir =  os.path.abspath(__file__ + '/..')
path = os.path.abspath(work_dir + '/../')
if not path in sys.path:
    sys.path.insert(0, path)
    print(path)
    
    
from pyPowerMeter import ThorlabsP1xx


# ------------------------------------
# -- Get the detectors
# ------------------------------------
rm = visa.ResourceManager()
rm = visa.ResourceManager()
connected_instr = {}
try:
    dev = rm.list_resources()
    names = []
    for dd in dev:
        try:
            instr = rm.open_resource(dd, timeout=0.5)
            # print('-'*60)
            n = instr.query('*IDN?').strip().replace('Thorlabs,','').replace('1.3.0','').replace(',', ', ')
            names += [n]
            connected_instr[n] = dd
        except Exception as err:
            pass
except Exception as err:
    pass


# ------------------------------------
# -- Create the UI
# ------------------------------------
class _dic2struct():
    def __init__(self, d, which='sim', do_tr=True):
        self._dic = d
        for a, b in d.items():
           setattr(self, a, _dic2struct(b) if isinstance(b, dict) else b)
    def __repr__(self):
        return str(list(self._dic.keys()))
dd = {'IN':{}, 'OUT':{}}
for ii in [dd['IN'], dd['OUT']]:
    ii['P'] = widgets.Text(value='0 mW', disabled=False)
    ii['P'].add_class("ui_power")
    ii['λ']= widgets.IntSlider(description = 'λ (nm)',value=1550,min=700, max=1800,step=50,
                                     orientation = 'vertical',readout=True, layout=Layout(height='180px'))
    ii['λ'].add_class("ui_wlgth")
    ii['fact']= widgets.IntSlider(description = 'Factor',value=9,min=1, max=100,step=1,
                                     orientation = 'vertical',readout=True, layout=Layout(height='180px'))
    ii['fact'].add_class("ui_wlgth")
    ii['Prgs'] = widgets.FloatProgress(value=0.0, min=0.0, max=1.0, bar_style='info')
    ii['Prgs'].add_class("ui_prgs")
    ii['Cnct'] = widgets.ToggleButton(value=False,description='Connect', layout=Layout(width='100%'))
    ii['Cnct'].add_class("ui_cnct")
    ii['Det'] = widgets.Select(options=connected_instr.keys(),
                                     disabled=False)
    _ = ii['Det'].add_class("ui_det")
dd['IN']['label'] = widgets.Label(value="Input:")
dd['IN']['label'].add_class("ui_label_title")



dd['OUT']['label'] = widgets.Label(value="Output:")
dd['OUT']['label'].add_class("ui_label_title")

dd['Losses'] = {}
dd['Losses']['loss'] = widgets.Text(value='-Inf dB', disabled=False)
dd['Losses']['loss'].add_class("ui_power")
dd['Losses']['label_top'] = widgets.Label(value="Losses:")
dd['Losses']['label_top'].add_class("ui_label_losses")
dd['Losses']['label_bottom'] = widgets.Label(value="")
dd['Losses']['label_bottom'].add_class("ui_label_losses")


dd['running'] = widgets.Checkbox(value = True, description = "Running")
dd['running'].add_class("ui_running")
ui = _dic2struct(dd)


IN = HBox([ui.IN.λ,ui.IN.fact,
            VBox([ui.IN.Det,ui.IN.Cnct]),
            VBox([ui.IN.P,
            ui.IN.Prgs]) ])

OUT = HBox([ui.OUT.λ,ui.OUT.fact,
            VBox([ui.OUT.Det,ui.OUT.Cnct]),
            VBox([ui.OUT.P,
            ui.OUT.Prgs])])
LOSS = VBox([ui.Losses.label_top,
            ui.Losses.loss,
            ui.Losses.label_bottom])


grid = VBox([ui.running,
             HBox([VBox([ui.IN.label,
                   IN,
                   ui.OUT.label,
                   OUT]), LOSS])
            ])


stop_threads = False
output = widgets.Output

# ------------------------------------
# -- Create the Worker
# ------------------------------------

Pmeter = {'IN':None, 'OUT':None}
def work(running, ui_slot, P, Loss, in_out):
    total = 100
    maxi = 0
    need_connect = True
    while True:
       
        if ui_slot.Cnct.value:
            if need_connect:
                instr = connected_instr[ui_slot.Det.value]
                Pmeter[in_out] = ThorlabsP1xx(address = instr)   
                Pmeter[in_out].connected = True
                Pmeter[in_out].lbd = float(ui_slot.λ.value)
                need_connect = False
            
            val = Pmeter[in_out].power*1e3 * ui_slot.fact.value

            if val>10:
                ui_slot.P.value = '{:.1f}'.format(val) + ' mW'
            else:
                ui_slot.P.value = '{:.3f}'.format(val) + ' mW'

            ui_slot.Prgs.value = val
            if val>maxi:
                maxi = val
                ui_slot.Prgs.max= maxi
                ui_slot.Prgs.value = val
            if in_out == 'IN':
                outP = float(P.value.replace(' mW', ''))
                inP = float(ui_slot.P.value.replace(' mW', ''))

                if outP>0:
                    Loss.value = '{:.3f} dB'.format(10*np.log10(outP/inP))
                else:
                    Loss.value = '-Inf dB'
        else:
            if not need_connect:
                Pmeter[in_out].connected = False
                need_connect = True
        if not ui.running.value:
            logging.debug('thread stop')
            break
        time.sleep(0.1)


display(HTML("<style>div.balanced-text .widget-label {max-width:200px; width:200px}"))

thread_in = threading.Thread(target=work, args=(ui.running, ui.IN, ui.OUT.P,ui.Losses.loss,  'IN'))
thread_out = threading.Thread(target=work, args=(ui.running, ui.OUT,None ,None, 'OUT'))
display(grid)

thread_in.start()
thread_out.start()

