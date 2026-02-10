from ipywidgets import widgets as wdg
from .ipyfilechooser import FileChooser
import plotly.graph_objects as go
import plotly.io as pio
import os
import numpy as np
pio.templates.default = "plotly_white"

class _dic2struct():
    def __init__(self, d, which='sim', do_tr=True):
        self._dic = d
        for a, b in d.items():
           setattr(self, a, _dic2struct(b) if isinstance(b, dict) else b)
    def __repr__(self):
        return str(list(self._dic.keys()))


class uiOSA():
    def __init__(self):
        # ----------------------------------
        # -- Setup the plot
        # ----------------------------------
        height = 800
        xlim = [1300, 1700]
        x = np.linspace(xlim[0], xlim[1], 100000)
        y = np.log10((1/np.cosh((x-(700+1850)/2)/10))**2)
        tr = go.Scatter(x =x, y =y)
        self.figOSA = go.FigureWidget(data=tr)
        self.figOSA.update_xaxes(title = 'Wavelength (nm)', range = [xlim[0], xlim[1]],
                        showspikes = True, spikethickness= 1)
        self.figOSA.update_yaxes(title = 'Power (dBm)', range = [-90, 20],
                                 showspikes = True, spikethickness= 1)
        self.figOSA.update_layout(height = height)


    def createUI(self):
        dd = {}

        # === Connection ===
        # ==============================
        # connection button
        dd['cnct'] =  wdg.Checkbox(value = False, description = "Connected")
        # IP Address
        dd['ip'] =  wdg.Text(value = '10.0.0.11', description = 'IP:')
        # Model connected
        dd['model'] =  wdg.Textarea(
                                value='',
                                rows=9,
                                placeholder='',
                                description='Model',
                                disabled=True
                            )

        # === Scan ===
        # ==============================
        # Scan type
        dd['refresh_trace'] = wdg.Button(description = 'Refresh Trace',
                                   button_style = 'info',
                                   tooltip='Fetch the current trace on the instrument',
                                   display='flex',
                                   flex_flow='row',
                                   justify_content='space-between',
                                    align_items='stretch',)
        # dd['refresh'].add_class("osa_scan_button")

        dd['scan'] = wdg.ToggleButtons(options=['Single', 'Repeat', 'Stop'],
                                       value = 'Stop',
                                       display='flex',
                                        flex_flow='row',
                                        justify_content='space-between',
                                        align_items='stretch',
                                       description='Scan:',
                                       button_style = 'info')
        # dd['scan'].add_class("osa_scan_button")

        # === Setup ===
        # ==============================
        # Wavelength range

        dd['refresh_setup'] = wdg.Button(description = 'Refresh Setup',
                                       button_style = 'info',
                                       tooltip='Fetch the current setup of the instrument',
                                       display='flex',
                                       flex_flow='row',
                                       justify_content='space-between',
                                        align_items='stretch',)

        dd['λ'] = wdg.IntRangeSlider(value = (0, 2000),
                                        min = 0, max = 2000, step = 5,
                                        description = 'λ',
                                    continuous_update=False)

        # Number of pts
        dd['pts'] = wdg.IntSlider(value = 50000,
                                        min =1, max = 100000, step = 100,
                                        description = 'Points:',
                                        continuous_update=False)
        # dd['pts'].add_class("osa_wavelength")
        # Resolution
        dd['res'] = wdg.Dropdown(options=['Norm/Hold', 'Norm/Auto', 'Mid', 'High 1', 'High 2', 'High 3'],
                                   description='Resolution:')

        # Bandiwth
        self._Bdwt_val = {0.02: '0.02 nm',
                    0.05: '0.05 nm',
                    0.1: '0.1 nm',
                    0.2: '0.2 nm',
                    0.5: '0.5 nm',
                    1: '1 nm',
                    2: '2 nm'}
        dd['bandwidth'] = wdg.SelectionSlider(description='Bandwidth:',
                                                  options=self._Bdwt_val.values(),
                                                 continuous_update=False)

        # dd['bandwidth'].add_class("osa_bandwidth")
        # === Trace ===
        # ==============================
        # freq/wavelength swith
        dd['freq_scale'] =  wdg.ToggleButtons(options=['Wavelength', 'Frequency'],
                                               value = 'Wavelength',
                                               description='X scale',disabled=False,
                                               button_style = '')
        # Trace selection
        dd['trace'] = wdg.Dropdown(options=['Trace A', 'Trace B', 'Trace C', 'Trace D'],
                                   value = 'Trace A',
                                   description='Trace:')

        # clear traces
        dd['clr'] = wdg.Button(description = 'Clear Traces',button_style = 'danger',tooltip='',)
        # delete saved trace
        # clear traces
        dd['clr_keep'] = wdg.Button(description = 'Clear Saved' ,button_style = 'warning',tooltip='',)
        # keep current
        dd['keep'] = wdg.Button(description = 'Keep Trace',
                                button_style = 'success',tooltip='Click me',)
        # === Save ===
        # ==============================
        # save
        # freq/wavelength swith
        dd['to_save'] =  wdg.ToggleButtons(options=['PC', 'OSA'],
                                               value = 'PC',
                                               description='Data',disabled=False,
                                               button_style = '')
        dd['save'] = wdg.Button(description = 'Save Spectra',button_style = 'info')
        dd['picker'] = FileChooser(os.path.abspath('./../'), width = 300)
        dd['picker'].use_dir_icons = True
        dd['picker'].rows = 8
        dd['picker'].width = 200

        self.ui = _dic2struct(dd)




        # -- setup the style of the UI --
        # --------------------------------
        self.ui.trace.layout = {'width': '285px', 'margin': '20px 7px 20px 0px'}
        self.ui.trace.style={"description_width": "45px"}

        self.ui.keep.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}
        self.ui.clr_keep.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}
        self.ui.clr.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}

        self.ui.freq_scale.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}
        self.ui.freq_scale.style={"button_width": "95px", "description_width": "45px"}


        self.ui.refresh_trace.layout = {'width': '300px', 'margin': '40px 0px 20px 0px'}
        self.ui.refresh_trace.style={"button_width": "55px"}

        self.ui.scan.layout = {'width': '300px', 'margin': '20px 0px 20px 0px'}
        self.ui.scan.style={"button_width": "55px", "description_width": "45px"}


        self.ui.ip.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}
        self.ui.ip.style={"description_width": "45px"}

        self.ui.model.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}
        self.ui.model.style={"description_width": "45px"}

        self.ui.cnct.layout = {'width': '300px', 'margin': '20px 0px 20px 0px'}
        self.ui.cnct.style={"description_width": "45px"}


        self.ui.refresh_setup.layout = {'width': '300px', 'margin': '20px 0px 20px 0px'}
        self.ui.res.layout = {'width': '300px', 'margin': '20px 0px 20px 0px'}
        self.ui.res.style={"description_width": "70px"}
        self.ui.bandwidth.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}
        self.ui.bandwidth.style={"description_width": "70px"}
        self.ui.pts.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}
        self.ui.pts.style={"description_width": "70px"}

        self.ui.λ.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}
        self.ui.λ.style={"description_width": "70px"}


        self.ui.to_save.layout = {'width': '300px', 'margin': '20px 0px 20px 0px'}
        self.ui.to_save.style={"button_width": "90px", "description_width": "45px"}
        self.ui.save.layout = {'width': '300px', 'margin': '0px 0px 20px 0px'}
        self.ui.picker.layout = wdg.Layout(display='inline',
                            flex_flow='column',
                            flex_wrap = 'wrap',
                            align_content =  'stretch',
                            justify_content =  'center',
                            align_items='stretch',
                            width='300px')
        self.ui.picker.width = 200
        self.ui.picker.rows =8



        # -- diplaying with style --

        box_layout =  wdg.Layout(display='flex',
                            flex_flow='column',
                            flex_wrap = 'wrap',
                            align_content =  'stretch',
                            justify_content =  'center',
                            align_items='stretch',
                            width='28%',
                            height = '500px')
        outp_layout =  wdg.Layout(display='flex',
                            flex_flow='column',
                            flex_wrap = 'wrap',
                            align_content =  'stretch',
                            justify_content =  'center',
                            align_items='stretch',
                            width='72%')


        figure = wdg.Box(children = [self.figOSA], layout = outp_layout)

        v_layout = wdg.Layout(display='flex',
                         flex_flow='column',
                         align_items='center',
                         align_content='center',
                         width='100%')

        items = [wdg.Label('') for i in range(4)]
        left_box = wdg.VBox([items[0], items[1]])
        right_box = wdg.VBox([items[2], items[3]])
        spacer = wdg.HBox([left_box, right_box])

        Connection = wdg.VBox([self.ui.cnct, self.ui.ip,  self.ui.model], layout = v_layout)
        Scan = wdg.VBox([self.ui.refresh_trace, self.ui.scan], layout = v_layout)
        Setup = wdg.VBox([self.ui.refresh_setup, self.ui.res,self.ui.bandwidth, self.ui.pts,self.ui.λ], layout = v_layout)
        Trace = wdg.VBox([self.ui.trace,self.ui.freq_scale, self.ui.keep, self.ui.clr_keep, self.ui.clr], layout = v_layout)
        Save = wdg.VBox([self.ui.to_save, self.ui.save,self.ui.picker], layout = v_layout)
        children = [Connection, Scan, Setup, Trace, Save]



        tab = wdg.Tab(layout = box_layout)
        tab.children = children
        titles = ['Connection', 'Scan', 'Setup', 'Trace', 'Save']
        for it, tt in enumerate(titles):
            tab.set_title(it, tt)
        end_layout = wdg.Layout(display='flex',
                         flex_flow='row',
                         align_items='center',
                         align_content='center',
                         width='100%')
        endUI = wdg.HBox([tab, figure], layout = end_layout)



        # -- Dispaying --
        display(endUI)
