#!/usr/bin/env python

import sys
# Import PyQt wrappers
from PyQt5.QtWidgets import QMainWindow, QApplication
# from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
# from PyQt5.QtCore import pyqtSlot
# from PyQt5 import QtCore
# from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QFontDatabase
from PyQt5 import uic
from PyQt5 import QtGui
import PyQt5

import time

import threading

import os
path = os.path.realpath('./UI/QDarkStyleSheet-master/qdarkstyle/')
if not path in sys.path:
    sys.path.insert(0, path)
path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)

Ui_MainWindow, QtBaseClass = uic.loadUiType('./UI/UITranmission.ui')
Ui_DevWindow, QtBaseClass = uic.loadUiType('./UI/DevWindow.ui')
# from UITranmission import Ui_MainWindow as Ui_MainWindow
import pyUtilities as ut
from pyNFLaser import NewFocus6700
from pyWavemeter import Wavemeter
import ipdb

class DevWind(QMainWindow):
    def __init__(self, parent = None):
        super(DevWind, self).__init__(parent)
        self.ui = Ui_DevWindow()
        self.ui.setupUi(self)
        self.ui.butt_clearError.clicked.connect(lambda:
                                self.ui.text_lastError.setText(''))

        self.parent = parent
        self.ui.butt_getLaserErr.clicked.connect(self.GetLaserErr)

    def GetLaserErr(self):
        try: 
            err = self.parent.laser.error
            self.ui.text_lastError.setText(str(err))
        except Exception as err:
            self.ui.text_lastError.setText(str(err))


class Transmission(QMainWindow):
    def __init__(self, **kwargs):
        super(Transmission, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._led = {False: QtGui.QPixmap(':/qss_icons/rc/radio_checked.png'),
                    True: QtGui.QPixmap(':/qss_icons/rc/radio_checked_focus.png')
                    }
        self._blink = False
        self.ui.slide_pzt.valueChanged[int].connect(lambda x: self.ui.spnbx_pzt.setValue(x/100))
        self.ui.spnbx_pzt.valueChanged[float].connect(self.Pzt_Value)
        # self.ui.slide_test.valueChanged[int].connect(self.Scan)
        self.ui.spnbx_lbd.valueChanged[float].connect(self.SetWavelength)
        self.ui.but_connect.clicked.connect(self.Connect)


        # self.ui.but_connect.clicked[bool].connect(self.EnableDCscan)

        self._connected = False
        self.ui.wdgt_param.setEnabled(False)
        self.ui.wdgt_plot.setEnabled(False)
        ut.CreatePyQtGraph(self, [1500, 1600], self.ui.mplvl)

        self.dev = DevWind(parent = self)
        # ipdb.set_trace()
        self.ui.actionGet_Errors.triggered.connect(self.dev.show)
    # -- Some Decorators --
    # -----------------------------------------------------------------------------
    def Blinking(condition):
        def decorator(fun):
            def wrapper(*args,**kwargs):
                self_app = args[0]
                def blink():
                    self.ui.groupBox_DCscan.setEnabled(False)
                    while self_app._test_blink:
                        self_app._blink = not(self_app._blink)
                        self_app.ui.led_SetWavelength.setPixmap(self_app._led[self_app._blink])
                        time.sleep(0.1)
                    self_app.ui.led_SetWavelength.setPixmap(self_app._led[False])
                    self.ui.groupBox_DCscan.setEnabled(True)

                
                self_app._test_blink = getattr(self_app, condition)
                out = fun(*args,**kwargs)
                self_app.threadscan = threading.Thread(target=blink, args=())
                self_app.threadscan.daemon = True
                self_app.threadscan.start()
                return out
            return wrapper
        return decorator

    def isConnected(fun):
        def wrapper(*args, **kwargs):
            self_app = args[0]
            if self_app._connected:
                out = fun(*args, **kwargs)
            else:
                out = None
                self.dev.ui.text_lastError.setText('Laser is not connected')
            return out
        return wrapper


    # -- Methods --
    # -----------------------------------------------------------------------------

    def Connect(self):
        if not self._connected:
            try: 
                idLaser = 4106
                DeviceKey = '6700 SN10027'
                self.laser = NewFocus6700(id =idLaser, key = DeviceKey)
                self.laser.beep = False
                self.laser.connected = True
                self.ui.but_connect.setText('Disconnect')
                self._connected = True
            except Exception as err:
                err = str(err) + '\nLaser is not connected, please try to connect it.'
                self.dev.ui.text_lastError.setText(err)
        else:
            try:
                self.laser.connected = False
                self.ui.but_connect.setText('Connect')
                self._connected = False
            except Exception as err:
                err = str(err) + '\nCannot disconnect the laser.'
                self.dev.ui.text_lastError.setText(str(err))

        self.ui.wdgt_param.setEnabled(self._connected)
        self.ui.wdgt_plot.setEnabled(self._connected)
        self.ui.led_connected.setPixmap(self._led[self._connected])

    @isConnected
    @Blinking('_is_changing_lbd')
    def SetWavelength(self,value):
        self.laser.lbd = value

    @isConnected
    def Pzt_Value(self,val):
        self.ui.slide_pzt.setValue(val*100)
        lbd.pzt = val
        
    @isConnected
    def Scan(self, value):
        self.ui.spnbx_lbd.blockSignals(True)
        
        self.ui.spnbx_lbd.blockSignals(False)



    # -- Utilities --
    # -----------------------------------------------------------------------------
    def FetchDaqParam(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    window = Transmission()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    sys.exit(app.exec_())



