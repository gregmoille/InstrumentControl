import pyqtgraph as pg
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import ipdb




def CreatePyQtGraph(app, xrange, plot_widget, color='#eff0f1'):
    labelStyle = {'color': color, 'font-size': '14pt'}
    axispen = pg.mkPen(color=color, fontsize='14pt')
    axisfont = QtGui.QFont()
    axisfont.setFamily('Arial')
    axisfont.setPointSize(22)
    axisfont.setBold(True)
    app.my_plot = pg.PlotWidget()


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

    plot_widget.addWidget(app.my_plot)

    x = np.linspace(xrange[0], xrange[1], 10000)
    span = xrange[1] - xrange[0]
    sigma = span/10 * np.random.rand(1)
    y = np.exp(-((x-(xrange[0]+span/2))**2)/(sigma**2))
    sigma = span/5 * np.random.rand(1)
    y2 = np.exp(-((x-(xrange[0]+span/2))**2)/(sigma**2))
    app._clr = ['#81caf9', '#ffa691', '#cfffaf']
    app.linepen = []
    app.linepen += [pg.mkPen(color=(129, 202, 249), width=1)]
    app.linepen += [pg.mkPen(color=(255, 166, 145), width=1)]
    app.linepen += [pg.mkPen(color='#cfffaf', width=1)]
    app.linepenMZ_frwrd = pg.mkPen(color=color, width=1)
    app.linepenMZ_bckwrd = pg.mkPen(color=color, width=1)

    app.current_trace = [pg.PlotCurveItem(x = x, y = y, pen=app.linepen[0],color = app._clr[0], clickable=True),
                        pg.PlotCurveItem(x = x, y = y2, pen=app.linepen[1], color = app._clr[1], clickable=True),]
    
    app.current_trace[0].setPen(width=2, color = app._clr[0])
    app._ind_curve = 0
    def SelectCurve(curve):
        # print('ehehehehehhe')
        for i,c in enumerate(app.current_trace):
            if c is curve:
                # print('ehehe')
                # c.setPen(pen=app.linepen[i])
                c.setPen(width=3,color = app._clr[i])
                # c.setPen(pen=app.linepen[i])
                app._ind_curve = i
                print(app._ind_curve)
            else:
                c.setPen(width=2,color = app._clr[i])

    for c in app.current_trace:
        app.my_plot.addItem(c)
        c.sigClicked.connect(SelectCurve)
def ReplaceData(app, x, y):
    # ipdb.set_trace()
    for line in app.current_trace:
                    app.my_plot.removeItem(line)
    app.current_trace = []
    app._ind_curve = 0
    try:
        for ii in range(x.shape[1]):
            app.app.current_trace += [pg.PlotCurveItem(x = x[ii], y = y[ii], 
                                    pen=app.linepen[ii],color = app._clr[ii], clickable=True)]
    except:
        app.current_trace += [pg.PlotCurveItem(x = x, y = y, 
                                    pen=app.linepen[0],color = app._clr[0], clickable=True)]
    app.current_trace[0].setPen(width=2, color = app._clr[0])
    def SelectCurve(curve):
        # print('ehehehehehhe')
        for i,c in enumerate(app.current_trace):
            if c is curve:
                # print('ehehe')
                # c.setPen(pen=app.linepen[i])
                c.setPen(width=3,color = app._clr[i])
                # c.setPen(pen=app.linepen[i])
                app._ind_curve = i
                print(app._ind_curve)
            else:
                c.setPen(width=2,color = app._clr[i])

    for c in app.current_trace:
        app.my_plot.addItem(c)
        c.sigClicked.connect(SelectCurve)


def SetPen(clr):
    return pg.mkPen(width=1, style=Qt.DashLine, color=clr)

def ShowDataTip(app):
    clr = '#FFFFFF'
    app.mrkrpen = SetPen(clr)
    app.txt = pg.TextItem('',color=(255, 255, 255),anchor=(0, 1), border = app.mrkrpen)
    if not app._showhline:
        ind_line = - app.ui.comboBox_SelectLine.currentIndex()
        
        
        x = app.current_trace[0].getData()[0]
        y = app.current_trace[0].getData()[1]

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
        app.ui.but_DataTip.setText('Show Data Tip')
        app._showhline = False



def PlotDownSampleTrace(app, x, y, step):
    for line in app.current_trace:
                    app.my_plot.removeItem(line)
    app.current_trace = []
    try:
        for ii in range(x.shape[1]):
            app.app.current_trace += [app.my_plot.plot(x[ii][::step], y[ii][::step],
                                                pen=app.linepen[ii],
                                                name='line{}'.format(ii))]
    except:
        app.current_trace += [app.my_plot.plot(x, y,
                                                pen=app.linepen[0],
                                                name='line{}'.format(0))]