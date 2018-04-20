#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QSlider
# Import PyQt wrappers
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot, pyqtSignal
# from PyQt5 import QtCore
# from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QFontDatabase
from PyQt5 import uic
from PyQt5 import QtGui
import PyQt5
from functools import wraps
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
        self._cst_slide = 100

        self.ui.slide_pzt.valueChanged[int].connect(lambda x: self.ui.spnbx_pzt.setValue(x/self._cst_slide))
        self.ui.spnbx_pzt.valueChanged[float].connect(self.Pzt_Value)
        self.ui.spnbx_lbd.valueChanged[float].connect(self.SetWavelength)
        self.ui.spnbx_lbd_start.valueChanged[float].connect(self.ScanLim)
        self.ui.spnbx_lbd_stop.valueChanged[float].connect(self.ScanLim)
        self.ui.spnbx_speed.valueChanged[float].connect(self.ScanSpeed)

        self.ui.but_connect.clicked.connect(self.Connect)
        self._connected = False
        self.ui.wdgt_param.setEnabled(False)
        self.ui.wdgt_plot.setEnabled(False)
        ut.CreatePyQtGraph(self, [1500, 1600], self.ui.mplvl)

        self.dev = DevWind(parent = self)
        self.ui.actionGet_Errors.triggered.connect(self.dev.show)

    # -- Some Decorators --
    # -----------------------------------------------------------------------------
    def Blinking(condition):
        def decorator(fun):
            @wraps(fun)
            def wrapper(*args,**kwargs):
                laser = args[0].laser
                self_app = args[0]
                def blink():
                    self_app.ui.but_dcscan.setEnabled(False)
                    print("Lbd changing {}".format(getattr(laser, condition)))
                    while getattr(laser, condition):
                        self_app._blink = not(self_app._blink)
                        self_app.ui.led_SetWavelength.setPixmap(self_app._led[self_app._blink])
                        time.sleep(0.1)
                    self_app.ui.led_SetWavelength.setPixmap(self_app._led[False])
                    self_app.ui.but_dcscan.setEnabled(True)

                out = fun(*args,**kwargs)
                time.sleep(0.1)
                print(args[0].laser._is_changing_lbd)
                self_app.threadscan = threading.Thread(target=blink, args=())
                self_app.threadscan.daemon = True
                self_app.threadscan.start()

                return out
            return wrapper
        return decorator

    def isConnected(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            self_app = args[0]
            if self_app._connected:
                out = fun(*args, **kwargs)
            else:
                out = None
                self_app.dev.ui.text_lastError.setText('Laser is not connected')
            return out
        return wrapper

    def BlockSignals(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            self_app = args[0]
            #block all signals
            attr = ['spnbx_lbd', 'slide_pzt','spnbx_pzt',
            'spnbx_lbd_start','spnbx_lbd_start','spnbx_lbd_stop','spnbx_speed']

            for a in attr:
                print(a)
                setattr(self_app.ui, a + '.blockSignals' , True)

            out = fun(*args, **kwargs)

            #enable back the signals
            for a in attr:
                setattr(self_app.ui, a + '.blockSignals', False)

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
                print('Connection')
                self.laser.connected = True
                # ipdb.set_trace()
                print('Connected... fetching Wavelength')
                self.ui.but_connect.setText('Disconnect')
                self._connected = True
                self.RetrieveLaser()
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
        print(self.laser._is_changing_lbd)

    @isConnected
    def Pzt_Value(self,val):
        print('Setting pzt')
        self.ui.slide_pzt.setValue(val*self._cst_slide)
        self.laser.pzt = val

    @isConnected
    def ScanLim(self,val):
        print('Setting limits')
        self.laser.scan_limit = [self.ui.spnbx_lbd_start.value(),
                                self.ui.spnbx_lbd_stop.value()]
    @isConnected
    def ScanSpeed(self,val):
        print('Setting speed')
        self.laser.scan_speed = self.ui.spnbx_speed.value()

    @isConnected
    def Scan(self, value):
        pass


    # -- Utilities --
    # -----------------------------------------------------------------------------
    def FetchDaqParam(self):
        pass

    @BlockSignals
    def RetrieveLaser(self):
        print("retrieving data")

        #for some reasom there is a bug disable the signal with this guy
        self.ui.spnbx_lbd_start.blockSignals(True)

        lbd = self.laser.lbd
        pzt = self.laser.pzt
        scan_lim = self.laser.scan_limit
        scan_speed = self.laser.scan_speed


        print('-'*30)
        print("Fetching error {}".format(self.laser.error))
        print('-'*30)
        
        print(pzt)
        print(scan_lim)
        self.ui.spnbx_lbd.setValue(lbd)
        self.ui.slide_pzt.setValue(pzt * 100)
        self.ui.spnbx_pzt.setValue(pzt)
        self.ui.spnbx_lbd_start.setValue(scan_lim[0])
        self.ui.spnbx_lbd_stop.setValue(scan_lim[1])
        self.ui.spnbx_speed.setValue(scan_speed)
        


        #patch for this signal
        self.ui.spnbx_lbd_start.blockSignals(False)

    
if __name__ == "__main__":
    app = QApplication([])
    window = Transmission()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    sys.exit(app.exec_())



