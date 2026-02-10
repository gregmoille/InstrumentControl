# Import PyQt wrappers
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QFontDatabase
from PyQt5 import uic
from PyQt5 import QtGui
# from analyzedisp import AnalyzeDisp
import PyQt5

# import utility packages
import ipdb
import os
import sys
import time
import dill
import pyqtgraph as pg
import numpy as np
import scipy.interpolate as intpl
import scipy.io as io
import scipy.signal as sig
import ctypes
from os.path import expanduser

from yokogawa import Yokogawa

Ui_MainWindow, QtBaseClass = uic.loadUiType('OsaUI.ui')

class WorkerScan(QObject):
    data = pyqtSignal(tuple)
    def __init__(self, osa):
        super().__init__()
        self._isRunning = True
        self.osa = osa
        # ipdb.set_trace()
        self.osa.EmptyBuffer()

    def Update(self):
        while True:
            if self._isRunning:
                # time.sleep(1)
                self.N = self.osa.QuerryData(":TRACe:SNUMber? TRA\n", 1)
                X = self.osa.QuerryData(":TRACe:X? TRA\n" , int(self.N)*100000)
                Y = self.osa.QuerryData(":TRACe:Y? TRA\n" , int(self.N)*100000)
                X = np.array([float(xx) for xx in X.split(',')])
                Y = np.array([float(xx) for xx in Y.split(',')])
                self.data.emit((X,Y, 0))
            else:
                break

    def UpdateSingle(self):
        self.osa.socket.send(b":TRACe:SNUMber? TRA\n")
        while True:
            try:
                self.N = self.osa.socket.recvfrom(256)[0]
                break
            except:
                pass
        print('Single Scan Done')
        X = self.osa.QuerryData(":TRACe:X? TRA\n" , int(self.N)*100000)
        Y = self.osa.QuerryData(":TRACe:Y? TRA\n" , int(self.N)*100000)
        X = np.array([float(xx) for xx in X.split(',')])
        Y = np.array([float(xx) for xx in Y.split(',')])
        self.data.emit((X,Y,1))


    def stop(self):
        self._isRunning = False



class OSA(QMainWindow):

    """
    To Do:
        - 
    """

    def __init__(self):
        super(OSA, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # misc
        self._isScanning = False
        self._isConnected = False
        self._res = ['Normal Hold',
                    'Normal Auto',
                    'Mid',
                    'High1',
                    'High2',
                    'High3',
                    'Normal',]
        self.Param = {}
        # create the plot window
        self.addmpl()
        # ipdb.set_trace()
       

        # Connect Connect button
        self.ui.pushButton_Connect.clicked.connect(self.Connect)

        # Connect the Set Param Button
        self.ui.pushButton_SetParam.clicked.connect(self.SetParam)
        self.ui.pushButton_Save.clicked.connect(self.Save)
        # Connect the saving buttons
        self.ui.pushButton_Path.clicked.connect(self.ChosePath)

        # Connect Scan Boutons
        self.ui.button_Single.clicked.connect(lambda: self.Scan('Single'))
        self.ui.button_Repeat.clicked.connect(lambda: self.Scan('Repeat'))
        # self.ui.button_Stop.clicked.connect(lambda: self.Scan('Stop'))

    def Connect(self):
        self.ui.button_Single.setEnabled(True)
        self.ui.button_Repeat.setEnabled(True)
        if not self._isConnected:
            self.osa = Yokogawa()
            self.GetParam()
            self.ui.led_Connect.setPixmap(QtGui.QPixmap(os.getcwd() + '/resources/led-on.png'))
            self._isConnected = True
            self._isScanning = False
            
        else:
            try:
                self.osa.QuerryData(":SENSe:WAVelength:CENTer?\n", 256)
                _pass = True
            except:
                self.osa.socket.close()
                self.ui.led_Connect.setPixmap(QtGui.QPixmap(os.getcwd() + '/resources/led-off.png'))
                self.osa = Yokogawa()
                self.GetParam()
                self.ui.led_Connect.setPixmap(QtGui.QPixmap(os.getcwd() + '/resources/led-on.png'))
                self._isConnected = True
                self._isScanning = False
                _pass = False
            if _pass:
                self.GetParam()



    def GetParam(self):
        # ipdb.set_trace()
        cnt = 0
        while cnt <100:
            try:
                centwlgth = self.osa.QuerryData(":SENSe:WAVelength:CENTer?\n", 256)
                span = self.osa.QuerryData(":SENSe:WAVelength:SPAN?\n", 256)
                resol = self.osa.QuerryData(":SENSe:SENSe?\n", 256)
                pts = self.osa.QuerryData(":SENSe:SWEep:POINts?\n", 256)
                pts_auto = self.osa.QuerryData(":SENSe:SWEep:POINts:AUTO?\n", 256)
                bdwdth = self.osa.QuerryData(":SENSe:BANDwidth?\n", 256)
                _pass = True
                break
            except:
                cnt += 1 
                time.sleep(0.1)
                _pass = False

        if _pass:
            self.ui.doubleSpinBox_BandWidth.setValue(float(bdwdth)*1e12)
            self.ui.doubleSpinBox_CentWavelength.setValue(float(centwlgth)*1e9)
            self.ui.doubleSpinBox_Span.setValue(float(span)*1e9)
            self.ui.comboBox_Resol.setCurrentIndex(int(resol))
            self.ui.spinBox_Points.setValue(int(pts))
            self.ui.radioButton_Points.setChecked(bool(pts_auto))

            self.Param['span'] = float(span)
            self.Param['resol'] = self._res[int(resol)]
            self.Param['pts'] = int(pts)
            self.Param['pts_auto'] = int(pts_auto)
            self.Param['centwlgth'] = float(centwlgth)
            self.Param['bdwdth'] = float(bdwdth)

        # print(self.Param)

    def SetParam(self):
        if self._isConnected:
            bdwdth = self.ui.doubleSpinBox_BandWidth.value()
            centwlgth = self.ui.doubleSpinBox_CentWavelength.value()
            span = self.ui.doubleSpinBox_Span.value()
            resol = self.ui.comboBox_Resol.currentIndex()
            pts = self.ui.spinBox_Points.value()
            pts_auto = self.ui.radioButton_Points.isChecked()


            self.osa.Write_OSA(":SENSe:WAVelength:CENTer " + str(centwlgth) + 'nm\n')
            self.osa.Write_OSA(":SENSe:BANDwidth " + str(bdwdth*1e-3) + 'nm\n')
            self.osa.Write_OSA(":SENSe:SENSe "+ str(resol) + '\n')
            self.osa.Write_OSA(":SENSe:WAVelength:SPAN "+ str(span) + 'nm\n')
            
            if pts_auto:
                self.osa.Write_OSA(":SENSe:SWEep:POINts:AUTO "+ str(int(pts_auto)))
            else:
                self.osa.Write_OSA(":SENSe:SWEep:POINts "+ str(pts))


            time.sleep(0.5)
            self.GetParam()

    def Scan(self, ScanType):
        if self._isConnected:
            if not self._isScanning:
                self.ThreadScan = QThread()
                self.WorkerFetch = WorkerScan(self.osa)
                self.WorkerFetch.data[tuple].connect(self.UpdateGraph)
                self.WorkerFetch.moveToThread(self.ThreadScan)
                if ScanType == 'Repeat' :
                    self.ui.button_Single.setEnabled(False)
                    self.ThreadScan.started.connect(self.WorkerFetch.Update)
                    self.ThreadScan.start()
                    self.ui.button_Repeat.setText('Stop')
                    self._isScanning = True
                    self.osa.Scan(ScanType)
                    
                else:
                    self.ui.button_Single.setEnabled(False)
                    self.ui.button_Repeat.setEnabled(False)
                    self.ThreadScan.started.connect(self.WorkerFetch.UpdateSingle)
                    self.ThreadScan.start()
                    self._isScanning = True
                    self.osa.Scan(ScanType)

            else:
                if ScanType == 'Repeat' :
                    self.WorkerFetch.stop()
                    self.ThreadScan.quit()
                    self.ThreadScan.wait()
                    self.ui.button_Single.setEnabled(True)
                    self.ui.button_Repeat.setText('Repeat')
                    self.osa.Scan('Stop')
                    self._isScanning = False
                else:
                    pass

    def ChosePath(self):
        # Open the popup window to pick a directory
        dir_ = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Select Directory", expanduser("Z:\\"),
            QtGui.QFileDialog.ShowDirsOnly))
        self.ui.lineEdit_Path.setText(dir_.strip())


    def Save(self):
        _save = True
        d_save = {}
        d_save['Wavelength'] = self.current_trace.getData()[0]*1e-9
        d_save['Signal'] = self.current_trace.getData()[1]
        d_save['Param'] = self.Param

        drcty = self.ui.lineEdit_Path.text().strip()
        fname = self.ui.lineEdit_FileName.text().strip()
        ext = '.mat'

        if drcty == '':
            _save = False
            self.ui.lineEdit_Path.setText('Chose a directory!')
        if fname == '':
            _save = False
            self.ui.lineEdit_FileName.setText('Chose a File Name!')

        if _save:
            filename = drcty + '\\' + fname + '.mat'
            io.savemat(filename, d_save)


    @pyqtSlot(tuple)
    def UpdateGraph(self, t):
        lbd = t[0]*1e9
        S = t[1]
        test = t[2]
        self.my_plot.removeItem(self.current_trace)
        self.current_trace = self.my_plot.plot(lbd, S,
                                                    pen=self.linepen)

        if test:
            self.WorkerFetch.stop()
            self.ThreadScan.quit()
            self.ThreadScan.wait()
            self._isScanning = False
            self.osa.Scan('Stop')
            self.ui.button_Single.setEnabled(True)
            self.ui.button_Repeat.setEnabled(True)


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
        self.my_plot.setRange(xRange=[1015, 1075], yRange=[0, 1])
        self.my_plot.setLabel(
            'bottom', text='Wavelength (nm)', units=None,  **labelStyle)
        self.my_plot.setLabel('left', 'Signal', 'dBm', **labelStyle)

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

        x = np.linspace(1015, 1075, 10000)*1e-9
        sigma = 5e-9 * np.random.rand(1)
        y = np.exp(-((x-1045e-9)**2)/(sigma**2))

        self.linepen = pg.mkPen(color='#0072bd', width=1)
        self.linepen2 = pg.mkPen(color='#bc462b', width=1)
        self.linepen3 = pg.mkPen(color='#b8bcc1', width=1)
        self.linepenMZ_frwrd = pg.mkPen(color='#abc5d6', width=1)
        self.linepenMZ_bckwrd = pg.mkPen(color='#cca096', width=1)

        # self.current_trace = []
        self.current_trace= self.my_plot.plot(x*1e9, y,
                                                    pen=self.linepen,
                                                    name='Forward'
                                  )


if __name__ == "__main__":
    myappid = 'NIST.osa.ui.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication([])
    app_icon = QtGui.QIcon()
    icon = os.getcwd() + '/resources/AQ6370V.ico'
    app_icon.addFile(icon, QtCore.QSize(16, 16))
    app_icon.addFile(icon, QtCore.QSize(24, 24))
    app_icon.addFile(icon, QtCore.QSize(32, 32))
    app_icon.addFile(icon, QtCore.QSize(48, 48))
    app_icon.addFile(icon, QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    window = OSA()
    window.show()
    sys.exit(app.exec_())
