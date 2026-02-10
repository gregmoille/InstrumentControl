import os
import sys
work_dir = os.path.abspath('N:/Experiments/InstrumentControl/')
if not work_dir in sys.path:
    sys.path.insert(0, work_dir)
from pyOSA import Yokogawa
import plotly.graph_objects as go
import pandas as pd
# OSAjupyter(DEBUG = True)

def SetFigure():
    
    df = pd.DataFrame(dict(freq = [0,1], S = [0,1]))
    fig = go.FigureWidget()
    fig.add_trace(go.Scatter(x = df.freq*1e-9,
                             y = df.S, line_color = 'steelblue'))
    fig.update_layout(height = 500)
    return fig

def ScanOSA(fig,stop_scan=True, ip = '10.0.0.20' ):
    import os
    import sys
    import time
    import threading
    from scipy import constants as cts
    import plotly.graph_objects as go
    import ipywidgets as widgets

    class TraceOSA(threading.Thread):
        def __init__(self,**kwargs):
            threading.Thread.__init__(self)
            self._running = False
            self.ip = kwargs.get('ip', '10.0.0.20')
            self.fig = kwargs.get('fig', None)
            self.stop_scan = kwargs.get('stop_scan', True)
        def run(self):
            self._running = True
            with Yokogawa(ip = self.ip) as osa: 
                while self._running:
                    print('Running', end = '\r')
                    self.trace = osa.trace
                    if self.fig:
                        figdata = self.fig.data[0] 
                        figdata.x = 1e-12*cts.c/self.trace.lbd
                        figdata.y = self.trace.S

        def stop(self, *args):
            self._running = False
            if self.stop_scan:
                time.sleep(0.1)
                with Yokogawa(ip = self.ip) as osa: 
                    osa.scan = 'stop'
            



    osa = TraceOSA(ip = ip, fig = fig, stop_scan = stop_scan)
    button = widgets.Button(description="Click To Stop Scan!")
    button.on_click(osa.stop)
    display(button)
    osa.start()
    return osa

