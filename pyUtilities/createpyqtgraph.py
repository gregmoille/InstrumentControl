import pyqtgraph as pg
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, Signal
import ipdb

class CustomPlotItem(pg.PlotDataItem):
    sigClicked = Signal(object)
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        # Need to switch off the "has no contents" flag
        # self.setFlags(self.flags() & ~self.ItemHasNoContents)

    def mouseDragEvent(self, ev):
        print(self.clickable)
        self.sigClicked.emit(self)
        print('Yep you clicked')


def CreatePyQtGraph(app, xrange, plot_widget, color='#eff0f1'):
    for ii in range(app.ui.combo_line.count()):
        app.ui.combo_line.removeItem(0)
    labelStyle = {'color': color, 'font-size': '14pt'}
    axispen = pg.mkPen(color=color, fontsize='14pt')
    axisfont = QtGui.QFont()
    axisfont.setFamily('Arial')
    axisfont.setPointSize(22)
    axisfont.setBold(True)
    app.my_plot = pg.PlotWidget()
    # ipdb.set_trace()

    app.my_plot.setBackground(background=None)
    app.my_plot.showGrid(x=True, y=True, alpha=0.25)
    # app.my_plot.ViewBox()
    app.my_plot.setRange(xRange=xrange, yRange=[0, 1])
    app.my_plot.setLabel(
        'bottom', text='Wavelength (nm)', units=None,  **labelStyle)
    app.my_plot.setLabel('left', 'Signal', 'V', **labelStyle)

    app.my_plot.plotItem.getAxis('bottom').setPen(axispen)
    app.my_plot.plotItem.getAxis('bottom').setFont(axisfont)
    app.my_plot.plotItem.getAxis('left').setStyle(tickFont=axisfont)
    app.my_plot.plotItem.getAxis('left').setPen(axispen)

    app.my_plot.plotItem.getAxis('top').setPen(axispen)
    app.my_plot.plotItem.getAxis('right').setPen(axispen)
    app.my_plot.plotItem.getAxis('top').setTicks([])
    app.my_plot.plotItem.getAxis('right').setTicks([])

    app.my_plot.plotItem.showAxis('right', show=True)
    app.my_plot.plotItem.showAxis('left', show=True)
    app.my_plot.plotItem.showAxis('top', show=True)
    app.my_plot.plotItem.showAxis('bottom', show=True)

    app.my_plot.plotItem.setDownsampling(auto=True, mode="subsample")

    plot_widget.addWidget(app.my_plot)

    x = np.linspace(xrange[0], xrange[1], 1e7)
    span = xrange[1] - xrange[0]
    sigma = span/10 * np.random.rand(1)
    y = np.sin(1e6*sigma*x/span)
    sigma = span/5 * np.random.rand(1)
    y2 = np.exp(-((x-(xrange[0]+span/2))**2)/(sigma**2))
    app._clr = ['#81caf9', '#ffa691', '#cfffaf']
    app._clr_deact = ['#5788a8', '#a06759', '#7b9968']
    app.linepen = []
    app.linepen += [pg.mkPen(color=(129, 202, 249), width=2)]
    app.linepen += [pg.mkPen(color=(255, 166, 145), width=2)]
    app.linepen += [pg.mkPen(color='#cfffaf', width= 1)]
    app.linepenMZ_frwrd = pg.mkPen(color=color, width=1)
    app.linepenMZ_bckwrd = pg.mkPen(color=color, width=1)

    app.current_trace = [pg.PlotDataItem(x = x, y = y, pen=app.linepen[0],color = app._clr_deact[0], clickable=True),
                        pg.PlotDataItem(x = x, y = y2, pen=app.linepen[1], color = app._clr_deact[1], clickable=True),]
    
    app.current_trace[0].setPen(width=1, color = app._clr[0])
    app._ind_curve = 0
    # def SelectCurve(curve):
    #     print('ehehehehehhe')
    #     for i,c in enumerate(app.current_trace):
    #         if c is curve:
    #             # print('ehehe')
    #             # c.setPen(pen=app.linepen[i])
    #             c.setPen(width=1,color = app._clr[i])
    #             # c.setPen(pen=app.linepen[i])
    #             app._ind_curve = i
    #         else:
    #             c.setPen(width=1,color = app._clr_deact[i])
    #     app.mrkrpen = SetPen(app._clr[app._ind_curve])
    #     print(app._clr[app._ind_curve])
    #     app.txt.setColor(app._clr[app._ind_curve])
    
    cnt = 0
    for c in app.current_trace:
        app.my_plot.addItem(c)
        app.ui.combo_line.addItem('Trace {}'.format(cnt))
        cnt += 1
        # c.setDownsampling(auto=True, method="subsample")

    app._toPlot = [np.array([x,x]), np.array([y,y2])]

def ReplaceData(app, x, y):
    # ipdb.set_trace()
    for ii in range(app.ui.combo_line.count()):
        app.ui.combo_line.removeItem(0)
    for line in app.current_trace:
        app.my_plot.removeItem(line)
    app.current_trace = []
    try:
        for ii in range(x.shape[0]):
            app.current_trace += [pg.PlotDataItem(x = x[ii], y = y[ii], 
                                    pen=app.linepen[ii],color = app._clr[ii], clickable=True)]
    except:
        app.current_trace += [pg.PlotDataItem(x = x, y = y, 
                                    pen=app.linepen[0],color = app._clr[0], clickable=True)]
    app.current_trace[0].setPen(width=2, color = app._clr[0])
    cnt = 0
    for c in app.current_trace:
        app.my_plot.addItem(c)
        app.ui.combo_line.addItem('Trace {}'.format(cnt))
        cnt += 1
    print('Done replacing')


def SetPen(clr):
    return pg.mkPen(width=1, style=Qt.DashLine, color=clr)

def ShowDataTip(app):
    clr = '#FFFFFF'
    app.mrkrpen = SetPen(app._clr[app._ind_curve])
    txtpen = SetPen(clr)
    if not app._showhline:        
        app.txt = pg.TextItem('',color=app._clr[app._ind_curve],anchor=(0, 1), border = txtpen)    
        x = app.current_trace[app._ind_curve].getData()[0]
        y = app.current_trace[app._ind_curve].getData()[1]

        xlim = app.my_plot.plotItem.getAxis('bottom').range

        xmean = (xlim[0] + xlim[1])/2
        ind = np.abs(xmean-x).argmin()
        xline = x[ind]
        yline = y[ind]

        app.vLine = pg.InfiniteLine(
            pos=[xline, 0], angle=90, movable=True, pen=app.mrkrpen)
        app.hLine = pg.InfiniteLine(
            pos=[0, yline], angle=0, movable=True, pen=app.mrkrpen)

        app.my_plot.addItem(app.vLine, ignoreBounds=True)
        app.my_plot.addItem(app.hLine, ignoreBounds=True)
        app.my_plot.addItem(app.txt, ignoreBounds=True)
        app._showhline = True
        app.ui.but_DataTip.setText('Hide Data Tip')
    else:
        app.my_plot.removeItem(app.vLine)
        app.my_plot.removeItem(app.hLine)
        app.my_plot.removeItem(app.txt)
        app.ui.but_DataTip.setText('Show Data Tip')
        app._showhline = False



def PlotDownSampleTrace(app, x, y, step):
    for line in app.current_trace:
                    app.my_plot.removeItem(line)
    app.current_trace = []
    try:
        for ii in range(x.shape[0]):
            app.current_trace += [pg.PlotDataItem(x = x[ii][::step], y = y[ii][::step], 
                                    pen=app.linepen[ii],color = app._clr_deact[ii], clickable=True)]
    except:
        app.current_trace += [pg.PlotDataItem(x = x[::step], y = y[::step], 
                                    pen=app.linepen[0],color = app._clr_deact[0], clickable=True)]

    app.current_trace[0].setPen(width=1, color = app._clr[0])
    def SelectCurve(curve):
        # print('ehehehehehhe')
        for i,c in enumerate(app.current_trace):
            if c is curve:
                # print('ehehe')
                # c.setPen(pen=app.linepen[i])
                c.setPen(width=1,color = app._clr[i])
                # c.setPen(pen=app.linepen[i])
                app._ind_curve = i
            else:
                c.setPen(width=1,color = app._clr_deact[i])
        app.mrkrpen = SetPen(app._clr[app._ind_curve])
        print(app._clr[app._ind_curve])
        app.txt.setColor(app._clr[app._ind_curve])
    for c in app.current_trace:
        app.my_plot.addItem(c)
        c.sigClicked.connect(SelectCurve)
        c.setDownsampling(auto=True, method="subsample")
