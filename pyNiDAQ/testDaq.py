
# Import PyQt wrappers
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QFontDatabase
from PyQt5 import uic
from PyQt5 import QtGui
import PyQt5


import ipdb
import os
import sys
import time
import numpy as np
import ctypes
from os.path import expanduser
import pyqtgraph as pg

from PyDAQmx import *
# nidaqmx

Ui_MainWindow, QtBaseClass = uic.loadUiType('DAQui.ui')


class DAQControl(QMainWindow):
    # changedValue = pyqtSignal(QObject)
    # buttonMoved = pyqtSignal(tuple)
    # sliderMoved = pyqtSignal(tuple)
    # sliderPiezoMoved = pyqtSignal(tuple)
    read = int32()

    def __init__(self):
        super(DAQControl, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addmpl()

        self.ui.pushButton_start.clicked.connect(self.Measure)

    def RetrieveParam(self):
        def returnValSpin(name, focus):
            spinbox = getattr(self.ui, focus + name)
            return spinbox.value()

        # ipdb.set_trace()
        param_name = ['amplitude', 'offset', 'time', 'timeres']
        focus_name = ['Ramp', 'Sine', 'Step']
        focus = focus_name[self.ui.TabProfile.currentIndex()]
        Param = {}
        for param in param_name:
            Param[param] = returnValSpin(param, focus)

        if focus == 'Sine':
            Param['frequency'] = returnValSpin('frequency', focus)

        Param['Vmin'] = self.ui.Vmin.value()
        Param['Vmax'] = self.ui.Vmax.value()

        Param['focus'] = focus

        print(Param)
        return Param

    def RetrieveDevice(self):
        device = self.ui.DevDAQ.currentText() + '/'
        Dev = {'ao': device + self.ui.ChannelOut.currentText(),
               'ai': device + self.ui.ChannelIn.currentText(),
               'ai2': device + self.ui.ChannelIn_2.currentText()}

        return Dev

    def DefSignal(self, Param):
        A = Param['amplitude']
        off = Param['offset']
        t_end = Param['time']
        dt = Param['timeres']
        x = np.arange(0, t_end+dt, dt)
        if Param['focus'] == 'Sine':
            freq = Param['frequency']

            y = 0.5*A*np.sin(2*np.pi * freq * x) + off

        elif Param['focus'] == 'Ramp':
            a = A/t_end
            b = -A/2 + off
            y = a*x+b

        # return to 0
        x2 = np.arange(t_end+dt, t_end+dt + t_end/10, dt)
        y2 = np.zeros(x2.size) + y[0]
        x = np.array(x.tolist() + x2.tolist())
        y = np.array(y.tolist() + y2.tolist())

        # add 25ms due to dealy write/read
        x = x + 0.025 + dt
        x2 = np.arange(0, 0.025+dt, dt)
        y2 = np.ones(np.size(x2)) * y[0]
        x = np.array(x2.tolist() + x.tolist() )
        y = np.array( y2.tolist() + y.tolist())

        # ipdb.set_trace()
        return x, y

    
    

    def SetupReadDAQ(self, **kwargs):
        npts = kwargs.get('npts', 1)
        freq = kwargs.get('freq', 1)
        channels = kwargs.get('channel', ['Dev1/ai0'])
        print(channels)
        data = kwargs.get('data', np.zeros((len(channels),npts),
                                           dtype=np.float64))
        print(data.shape)
        Vmax = kwargs.get('Vmax', 0)
        Vmin = kwargs.get('Vmin', 0)
        
        cnt = 0
        ch = ''
        for ii in channels:
            ch = ch + ii + ','
            cnt += 1 
        ch = ch[:-1]
        print(ch)
        taskHandle = TaskHandle()
        DAQmxCreateTask("", byref(taskHandle))
        DAQmxCreateAIVoltageChan(taskHandle, ch, "",
                                 DAQmx_Val_Cfg_Default, Vmin, Vmax,
                                 DAQmx_Val_Volts, None)
        DAQmxCfgSampClkTiming(taskHandle, "", npts*freq,
                              DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
                              npts)
        return taskHandle, data

    def SetupWriteDAQ(self, **kwargs):
        npts = kwargs.get('npts', 1)
        freq = kwargs.get('freq', 1)
        data = kwargs.get('data1period', np.array(0))
        Vmax = kwargs.get('Vmax', 0)
        Vmin = kwargs.get('Vmin', 0)
        ch = kwargs.get('channel', 'Dev1/ao0')

        taskHandle = TaskHandle()
        DAQmxCreateTask("", byref(taskHandle))
        DAQmxCreateAOVoltageChan(taskHandle,
                                 ch, "",
                                 Vmin, Vmax,
                                 DAQmx_Val_Volts,
                                 None)
        DAQmxCfgSampClkTiming(taskHandle, "", npts*freq,
                              DAQmx_Val_Rising,
                              DAQmx_Val_FiniteSamps,
                              npts)
        DAQmxWriteAnalogF64(taskHandle, npts, 0, 10,
                            DAQmx_Val_GroupByChannel, data,
                            None, None)
        return taskHandle

    def StartMeasure(self):
        DAQmxStartTask(self.taskHandle_write)
        self.twrite = time.time()
        DAQmxStartTask(self.taskHandle_read)
        self.tread = time.time()

    def ReadData(self, freq, npts, Dev):
        DAQmxReadAnalogF64(self.taskHandle_read, self.fact *npts, freq,
                           DAQmx_Val_GroupByChannel, self.data,
                          2 * self.fact *npts, byref(self.read), None)

    def PlotResults(self, t_end):
        for line in self.current_trace:
            self.my_plot.removeItem(line)

        self.current_trace = []
        
        V1 = self.data[0]
        V2 = self.data[1]
        t = np.linspace(0, t_end, len(V1))
        self.current_trace.append(self.my_plot.plot(t, V1,
                                                     pen=self.linepen))
        self.current_trace.append(self.my_plot.plot(t, V2,
                                                     pen=self.linepen2))
        # ipdb.set_trace()
    def Measure(self):
        Param = self.RetrieveParam()
        Dev = self.RetrieveDevice()
        self.fact =  10

        t_signal, signal = self.DefSignal(Param)
        npts = len(signal)
        freq = 1/Param['time']

        self.taskHandle_read, self.data = self.SetupReadDAQ(freq=freq, npts=self.fact *npts,
                                                            Vmin=Param['Vmin'],
                                                            Vmax=Param['Vmax'],
                                                            channel=[Dev['ai'], Dev['ai2']])
        self.taskHandle_write = self.SetupWriteDAQ(freq=freq, npts=npts,
                                                   data1period=signal,
                                                   Vmax=np.max(signal),
                                                   Vmin=np.min(signal),
                                                   channel=Dev['ao'])

        self.StartMeasure()
        time.sleep(1/freq + 0.1)
        cnt =0
        while cnt <10:
            # try:
            self.ReadData(freq, npts, Dev)
            break
            # except:
            #     print('Waiting a bit')
            #     time.sleep(1)
            #     cnt += 1
        DAQmxStopTask(self.taskHandle_read)
        DAQmxStopTask(self.taskHandle_write)
        DAQmxClearTask(self.taskHandle_read)
        DAQmxClearTask(self.taskHandle_write)
        self.PlotResults(Param['time'])
        print('-'*60)
        tdelay = self.tread- self.twrite
        print('Time delay (ms) {:.3f}'.format(tdelay*1e3))
        print('-'*60)


    def addmpl(self):
        labelStyle = {'color': '#000', 'font-size': '14pt'}
        axispen = pg.mkPen(color='#000', fontsize='14pt')
        axisfont = QtGui.QFont()
        axisfont.setFamily('Arial')
        axisfont.setPointSize(22)
        axisfont.setBold(True)

        self.my_plot = pg.PlotWidget()

        self.my_plot.setBackground(background=None)
        self.my_plot.showGrid(x=True, y=True, alpha=0.25)
        # self.my_plot.ViewBox()
        self.my_plot.setRange(xRange=[0, 1], yRange=[0, 1])
        self.my_plot.setLabel(
            'bottom', text='Wavelength (nm)', units=None,  **labelStyle)
        self.my_plot.setLabel('left', 'Signal', 'V', **labelStyle)

        self.my_plot.plotItem.getAxis('bottom').setPen(axispen)
        self.my_plot.plotItem.getAxis('bottom').setFont(axisfont)
        self.my_plot.plotItem.getAxis('left').setStyle(tickFont=axisfont)
        self.my_plot.plotItem.getAxis('left').setPen(axispen)

        self.my_plot.plotItem.getAxis('top').setPen(axispen)
        self.my_plot.plotItem.getAxis('right').setPen(axispen)
        self.my_plot.plotItem.getAxis('top').setTicks([])
        self.my_plot.plotItem.getAxis('right').setTicks([])

        self.my_plot.plotItem.showAxis('right', show=True)
        self.my_plot.plotItem.showAxis('left', show=True)
        self.my_plot.plotItem.showAxis('top', show=True)
        self.my_plot.plotItem.showAxis('bottom', show=True)

        self.ui.mplvl.addWidget(self.my_plot)

        x = np.linspace(0, 1, 10000)*1e-9
        sigma = 5e-9 * np.random.rand(1)
        y = np.exp(-((x-0.5)**2)/(sigma**2))

        self.linepen = pg.mkPen(color='#0072bd', width=1)
        self.linepen2 = pg.mkPen(color='#bc462b', width=1)
        self.current_trace = []
        self.current_trace.append(self.my_plot.plot(x, y,
                                                    pen=self.linepen,
                                                    name='Forward')
                                  )

#                           --  Main --
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    myappid = 'NIST.daqcontrol.ui.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication([])
    # app_icon = QtGui.QIcon()
    # icon = os.getcwd() + '/ressources/IconUI.ico'
    # app_icon.addFile(icon, QtCore.QSize(16, 16))
    # app_icon.addFile(icon, QtCore.QSize(24, 24))
    # app_icon.addFile(icon, QtCore.QSize(32, 32))
    # app_icon.addFile(icon, QtCore.QSize(48, 48))
    # app_icon.addFile(icon, QtCore.QSize(256, 256))
    # app.setWindowIcon(app_icon)
    window = DAQControl()
    window.show()
    sys.exit(app.exec_())
