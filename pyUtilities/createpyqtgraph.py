import pyqtgraph as pg
import numpy as np
from PyQt5 import QtGui
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

    app.linepen = []

    app.linepen += [pg.mkPen(color='#81caf9', width=1)]
    app.linepen += [pg.mkPen(color='#ffa691', width=1)]
    app.linepen += [pg.mkPen(color='#cfffaf', width=1)]
    app.linepenMZ_frwrd = pg.mkPen(color=color, width=1)
    app.linepenMZ_bckwrd = pg.mkPen(color=color, width=1)

    app.current_trace = []
    app.current_trace.append(app.my_plot.plot(x, y,
                                                pen=app.linepen[0],
                                                name='Forward')
                              )
    # for ii in range(app.ui.comboBox_SelectLine.count()):
    #     app.ui.comboBox_SelectLine.removeItem(0)
    # for ii in range(len(app.current_trace)):
    #     app.ui.comboBox_SelectLine.addItem('Line ' + str(ii+1))

def ReplaceData(app, x, y):
    # ipdb.set_trace()
    for line in app.current_trace:
                    app.my_plot.removeItem(line)
    app.current_trace = []
    try:
        for ii in range(x.shape[1]):
            app.app.current_trace += [app.my_plot.plot(x[ii], y[ii],
                                                pen=app.linepen[ii],
                                                name='line{}'.format(ii))]
    except:
        app.current_trace += [app.my_plot.plot(x, y,
                                                pen=app.linepen[0],
                                                name='line{}'.format(0))]