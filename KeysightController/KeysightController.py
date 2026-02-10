#!/usr/bin/env python

# -- Import PyQt wrappers --
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QPointF
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtGui

# -- import classic package --
from functools import wraps
from datetime import datetime
import time
import sys
import numpy as np
import threading
import os
import ipdb
import pyqtgraph as pg
from copy import copy

work_dir = path = os.path.abspath(__file__ + '/..')
print(work_dir)
# -- import custom NIST-ucomb Package --
path = os.path.abspath(work_dir + '/UI/QDarkStyleSheet-master/qdarkstyle/')

if not path in sys.path:
    sys.path.insert(0, path)
path = os.path.abspath(work_dir + '/../')
if not path in sys.path:
    sys.path.insert(0, path)
    print(path)
import pyUtilities as ut
from pyLaser import Keysight8164B
from pyPowerMeter import Keysight7744A

Ui_MainWindow, QtBaseClass = uic.loadUiType(work_dir + '/UI/UIkeysight.ui')


class KeysightControll(QMainWindow):
    '''

    '''
    __author__ = "Gregory Moille"
    __copyright__ = "Copyright 2018, NIST"
    __credits__ = ["Gregory Moille",
                   "Xiyuan Lu",
                   "Kartik Srinivasan"]
    __license__ = "GPL"
    __version__ = "1.0.0"
    __maintainer__ = "Gregory Moille"
    __email__ = "gregory.moille@mist.gov"
    __status__ = "Development"

    def __init__(self, **kwargs):
        super(KeysightControll, self).__init__()

        # -- setup the UI --
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._led = {False: QPixmap(':/qss_icons/rc/radio_checked.png'),
                     True: QPixmap(':/qss_icons/rc/radio_checked_focus.png')
                     }

        # -- setup useful hidden attributes --
        self._plotting = False
        self._isRuning = False
        self._laserconnected = False
        self._detconnected = False

        # -- connect buttons --
        self.ui.butConnectLaser.clicked.connect(self.ConnectLsr)
        self.ui.butConnectDet.clicked.connect(self.ConnectDet)
        self.ui.butSet.clicked.connect(self.SetLaser)
        self.ui.butFetch.clicked.connect(self.FetchLaser)
        self.ui.butUp.clicked.connect(lambda: self.ChangeLbd('up'))
        self.ui.butDown.clicked.connect(lambda: self.ChangeLbd('down'))

        self.ui.butAcquire.clicked.connect(self.PlotPower)
        self.ui.butClear.clicked.connect(self.ClearPlot)

        self.ui.butResetLaser.clicked.connect(self.resetLaser)
        self.ui.butResetDet.clicked.connect(self.resetDet)

        # -- Create a graph --
        ut.CreatePyQtGraph(self, [0, 5], self.ui.mplvl, 
                        xlabel = 'Time', ylabel = 'Power (mW)',
                        N = 1)

    def _isConnected(attr):
        def check(fun):
            @wraps(fun)
            def wrapp(*args, **kwargs):
                app = args[0]
                val = getattr(app, attr)
                if val:
                    out = fun(*args, **kwargs)
                else:
                    out = None
                    print('Not connected!!!')
            return wrapp
        return check 

    def ConnectLsr(self):
        if not self._laserconnected:
            addrs = self.ui.lsrAdd.currentText()
            self._lsr = Keysight8164B(addres = addrs)
            self._lsr.connected = True
            print(self._lsr.connected)
            if self._lsr.connected:
                self.ui.ledLsr.setPixmap(self._led[True])
                self._laserconnected = True
            else:
                self.ui.butConnectLaser.setChecked(False)
        else:
            self._lsr.connected = False
            self.ui.ledLsr.setPixmap(self._led[False])

    def ConnectDet(self):
        if not self._detconnected:
            addrs = self.ui.lsrAdd.currentText()
            self._det = Keysight7744A(addres = addrs)
            self._det.connected = True
            print(self._det.connected)
            if self._det.connected:
                self.ui.ledDet.setPixmap(self._led[True])
                self._detconnected = True
            else:
                self.ui.butConnectDet.setChecked(False)
        else:
            self._det.connected = False
            self.ui.ledDet.setPixmap(self._led[False])


    @_isConnected('_laserconnected')
    def SetLaser(self,val):
        self._lsr.lbd = self.ui.spinLaserLbd.value()
        self._lsr.power = self.ui.spinLaserPow.value()
        self._lsr.attenuation = self.ui.spinAtt.value()
        self._lsr.attenuation_lbd = self.ui.spinAttLbd.value()

    @_isConnected('_laserconnected')
    def FetchLaser(self,val):
        self.ui.spinLaserLbd.setValue(self._lsr.lbd)
        self.ui.spinLaserPow.setValue(self._lsr.power)
        self.ui.spinAtt.setValue(self._lsr.attenuation)
        self.ui.spinAttLbd.setValue(self._lsr.attenuation_lbd)
        self.ui.lblWlgth.setText('{:.3f}'.format(self._lsr.lbd))

    @_isConnected('_laserconnected')
    def ChangeLbd(self,dir):
        const = 1
        if dir == 'down':
            const = -1

        step = self.ui.spinRes.value()*1e-3
        self.ui.butUp.setEnabled(False)
        self.ui.butDown.setEnabled(False)
        self.ui.sliderStep.setEnabled(False)
        self.ui.spinRes.setEnabled(False)
        QApplication.processEvents()
        λnow = self._lsr.lbd
        time.sleep(0.01)
        self._lsr.lbd  = λnow + const* step
        time.sleep(0.01)
        lbd = self._lsr.lbd
        self.ui.lblWlgth.setText('{:.3f}'.format(lbd))

        self.ui.butUp.setEnabled(True)
        self.ui.butDown.setEnabled(True)
        self.ui.sliderStep.setEnabled(True)
        self.ui.spinRes.setEnabled(True)
        QApplication.processEvents()

    @_isConnected('_laserconnected')
    def resetLaser(self, val):
        self._lsr.reset = True

    @_isConnected('_detconnected')
    def resetDet(self, val):
        self._det.reset = True

    @_isConnected('_detconnected')
    def PlotPower(self, val):
        if self._plotting:
            self._plotting = False
            self.threadPlot.stop()
            self.ui.butAcquire.setText('Acquire')
        else:


            self._tscan = self.ui.spinTime.value()
            self.my_plot.setRange(xRange=[0, self._tscan])
            self._plotting = True
            self.ui.butAcquire.setText('Stop')

            self._det.lbd = self.ui.spinLaserLbd.value()
            self._det.reset = True

            class UpdateData(QThread):
                data = pyqtSignal(tuple)

                def __init__(self, **kwargs):
                    self._t = []
                    self.tscan = kwargs.get('tscan', 1)
                    self._det = kwargs.get('det', 1)
                    self._Pdet = []
                    self._P0 = 0
                    self._t0 = time.time()
                    self._isRuning = True
                    QThread.__init__(self)

                def run(self):
                    while self._isRuning:
                        t = time.time() - self._t0
                        P = self._det.power
                        if t > self.tscan:
                            self._t0 = time.time()
                            t = time.time() - self._t0
                            self._t = []
                            self._Pdet = []

                        self._t.append(t)
                        self._Pdet.append(P)
                        time.sleep(0.01)
                        self.data.emit((self._t,self._Pdet))
                
                def stop(self):
                    self._isRuning = False

            @pyqtSlot(tuple)
            def UpdatePlot(tpl):
                t = tpl[0]
                P = tpl[1]
                self.ui.lblPower.setText('{:.5f}'.format(P[-1]))
                for line in self.current_trace:
                    self.my_plot.removeItem(line)
                try:
                    self.current_trace = [pg.PlotDataItem(x = t, y = P,
                                                pen=self.linepen[0],color = self._clr[0])]
                except:
                    self.current_trace = []
                for c in self.current_trace:
                    self.my_plot.addItem(c)



            self.threadPlot = UpdateData(tscan = self._tscan, det = self._det)
            self.threadPlot.data[tuple].connect(UpdatePlot)
            self.threadPlot.start()


    def ClearPlot(self, val):
        for line in self.current_trace:
                self.my_plot.removeItem(line)



    # -----------------------------------------------------------------------------
    # -- Graph Interaction --
    # -----------------------------------------------------------------------------



if __name__ == "__main__":
    app = QApplication([])
    window = KeysightControll()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    sys.exit(app.exec_())
