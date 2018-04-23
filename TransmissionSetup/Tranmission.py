#!/usr/bin/env python

# -- Import PyQt wrappers -- 
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

# -- import classic package --
from functools import wraps
import time
import sys
import numpy as np
import threading
import os
import ipdb

# -- import custom NIST-ucomb Package --
path = os.path.realpath('./UI/QDarkStyleSheet-master/qdarkstyle/')
if not path in sys.path:
    sys.path.insert(0, path)
path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)
import pyUtilities as ut
from pyNFLaser import NewFocus6700
from pyWavemeter import Wavemeter
from workers import DcScan

# -- load UI --
Ui_MainWindow, QtBaseClass = uic.loadUiType('./UI/UITranmission.ui')
Ui_DevWindow, QtBaseClass = uic.loadUiType('./UI/DevWindow.ui')

class ErrorHandling(QThread):
    err_msg = pyqtSignal(str)

    def __init__(self, main_app):
        QThread.__init__(self)
        ipdb.set_trace()
        self.main_app = main_app
        self._isRunning = True

    def run(self):
        self._isRunning = True
        print('Doing First stuff!!!!')
        while self._isRunning:
            print('Doing stuff!!!!')
            if self.main_app._connected:
                old_err = self.main_app._olderr.split('\n')[-1]
                new_err = self.main_app.laser._err_msg.split('\n')[-1]
                if not old_err ==  new_err:
                    self.main_app._olderr +=  '\n' + new_err
                    self.err_msg.emit(str(self.main_app._olderr))
            time.sleep(1)
    def stop(self):
        self._isRunning = False

class DevWind(QMainWindow):
    def __init__(self, parent=None):
        super(DevWind, self).__init__(parent)
        self.ui = Ui_DevWindow()
        self.ui.setupUi(self)
        self.ui.butt_clearError.clicked.connect(lambda:
                                                self.ui.text_lastError.setText(''))

        self.parent = parent
        self.old_err = ''
        self.ui.text_lastError.setText('')
        # self.GetLaserErr()
        # self.ui.butt_getLaserErr.clicked.connect(self.GetLaserErr)

    def GetLaserErr(self):
        @pyqtSlot(str)
        def _updateErr(val):
            self.ui.text_lastError.setText(val)

        self.threadErr = ErrorHandling(main_app=self.parent)
        self.threadErr.err_msg[str].connect(_updateErr)
        self.threadErr.start()
        
    def StopErr(self):
        self.threadErr.stop()

class Transmission(QMainWindow):
    '''
    --------------------------------------------------------
    Main Window for the transmission UI software
    It is long, but it is mostly connection of the buttons,
    a bit of postprocessing and so on. The work is done 
    under the hood, through the workers, and through the 
    different homemande python package to controll the 
    equipement (see pyNFLaser, pyWavemeter,...)
    
    ------------------------------------------------------
    G. Moille - NIST - 2018
    ------------------------------------------------------
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
        super(Transmission, self).__init__()

        # -- setup the UI --
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # -- setup main attributes --
        self.laser = None
        self.wavemeter = None
        
        # -- setup useful hidden attributes --
        self._connected = False
        self._led = {False: QPixmap(':/qss_icons/rc/radio_checked.png'),
                     True: QPixmap(':/qss_icons/rc/radio_checked_focus.png')
                     }
        self._blink = False
        self._cst_slide = 100

        # -- connect buttons --
        self.ui.but_connect.clicked.connect(self.Connect)
        self.ui.but_laserOut.clicked.connect(self.LaserOut)
        self.ui.but_dcscan.clicked.connect(self.Scan)

        # -- connect spin boxes --
        self.ui.spnbx_pzt.valueChanged[float].connect(self.Pzt_Value)
        self.ui.spnbx_lbd.valueChanged[float].connect(self.SetWavelength)
        self.ui.spnbx_lbd_start.valueChanged[float].connect(self.ScanLim)
        self.ui.spnbx_lbd_stop.valueChanged[float].connect(self.ScanLim)
        self.ui.spnbx_speed.valueChanged[float].connect(self.ScanSpeed)

        # -- connect sliders --
        self.ui.slide_pzt.valueChanged[int].connect(
            lambda x: self.ui.spnbx_pzt.setValue(x/self._cst_slide))

        # -- Create a graph --
        ut.CreatePyQtGraph(self, [1500, 1600], self.ui.mplvl)

        # -- Setup apparence at launch --
        self.ui.wdgt_param.setEnabled(False)
        self.ui.wdgt_plot.setEnabled(False)

        # -- Misc --
        self._do_blink = False
        self.wlm = None
        self.laser = None
        self._olderr = ''
        self._param = {}
        # self.dev = DevWind(parent=self)
        # self.ui.actionGet_Errors.triggered.connect(self.dev.show)

    # -----------------------------------------------------------------------------
    # -- Some Decorators --
    # -----------------------------------------------------------------------------
    def Blinking(cdt_word):
        '''
        Blinking decorator when changing wavelength
        '''
        def decorator(fun):
            @wraps(fun)
            def wrapper(*args, **kwargs):
                self_app = args[0]

                def blink():
                    cdt = True
                    self_app.ui.but_dcscan.setEnabled(False)
                    while cdt:
                        self_app._blink = not(self_app._blink)
                        self_app.ui.led_SetWavelength.setPixmap(
                            self_app._led[self_app._blink])
                        time.sleep(0.1)
                        cdt = eval(cdt_word)

                    self_app.ui.led_SetWavelength.setPixmap(
                        self_app._led[False])
                    self_app.ui.but_dcscan.setEnabled(True)

                out = fun(*args, **kwargs)
                self_app.threadscan = threading.Thread(target=blink, args=())
                self_app.threadscan.daemon = True
                self_app.ui.but_dcscan.setEnabled(False)
                self_app.threadscan.start()

                return out
            return wrapper
        return decorator

    def isConnected(fun):
        '''
        Decorator checking of laser connected to perform or no 
        the operation
        '''
        @wraps(fun)
        def wrapper(*args, **kwargs):
            self_app = args[0]
            if self_app._connected:
                out = fun(*args, **kwargs)
            else:
                out = None
                self_app.dev.ui.text_lastError.setText(
                    'Laser is not connected')
            return out
        return wrapper

    def blockSignals(val):
        '''
        Block the signal if spinboxes or other need to be set to a value
        without sending a command to the instrument
        '''
        def dec(fun):
            @wraps(fun)
            def wrapper(*args, **kwargs):
                self_app = args[0]
                # block all signals
                attr = ['spnbx_lbd', 'slide_pzt', 'spnbx_pzt',
                        'spnbx_lbd_start', 'spnbx_lbd_start', 'spnbx_lbd_stop', 'spnbx_speed']

                if not val:
                    out = fun(*args, **kwargs)

                for a in attr:
                    print(a)
                    setattr(self_app.ui, a + '.blockSignals', True)
                time.sleep(0.2)
                QApplication.processEvents()

                if val:
                    out = fun(*args, **kwargs)

                return out
            return wrapper
        return dec

    # -----------------------------------------------------------------------------
    # -- Methods --
    # -----------------------------------------------------------------------------
    def Connect(self):
        if not self._connected:
            try:
                idLaser = 4106
                DeviceKey = '6700 SN10027'
                self.laser = NewFocus6700(id=idLaser, key=DeviceKey)
                print('Connection')
                self.laser.connected = True
                # ipdb.set_trace()
                print('Connected... fetching Wavelength')
                self.ui.but_connect.setText('Disconnect')
                self._connected = True
                self.RetrieveLaser()
                # self.dev.GetLaserErr()

            except Exception as err:
                err = str(err) + \
                    '\nLaser is not connected, please try to connect it.'
                self.dev.ui.text_lastError.setText(err)
        else:
            try:
                self.laser.connected = False
                self.ui.but_connect.setText('Connect')
                self._connected = False
                # self.dev.StopErr()
            except Exception as err:
                err = str(err) + '\nCannot disconnect the laser.'
                self.dev.ui.text_lastError.setText(str(err))

        self.ui.wdgt_param.setEnabled(self._connected)
        self.ui.wdgt_plot.setEnabled(self._connected)
        self.ui.led_connected.setPixmap(self._led[self._connected])


    @isConnected
    def LaserOut(self,val):
        out = self.laser.output
        if out:
            self.laser.output = False
            self.ui.led_laserOut.setPixmap(self._led[False])
        else:
            self.laser.output = True
            self.ui.led_laserOut.setPixmap(self._led[True])

    @isConnected
    @Blinking('self_app.laser._is_changing_lbd')
    def SetWavelength(self, value):
        self.laser.lbd = value

    @isConnected
    def Pzt_Value(self, val):
        print('Setting pzt')
        self.ui.slide_pzt.setValue(val*self._cst_slide)
        self.laser.pzt = val

    @isConnected
    def ScanLim(self, val):
        print('Setting limits')
        self.laser.scan_limit = [self.ui.spnbx_lbd_start.value(),
                                 self.ui.spnbx_lbd_stop.value()]

    @isConnected
    def ScanSpeed(self, val):
        print('Setting speed')
        self.laser.scan_speed = self.ui.spnbx_speed.value()

    @isConnected
    def Scan(self, value):
        self._do_blink = True
        def EnableUIscan(val):
            self.ui.groupBox_DCscan.setEnabled(val)
            self.ui.spnbx_I.setEnabled(val)
            self.ui.spnbx_pzt.setEnabled(val)
            self.ui.spnbx_lbd.setEnabled(val)
            self.ui.slide_pzt.setEnabled(val)
            self.ui.groupBox_Power.setEnabled(val)
            self.ui.groupBox_DAQ.setEnabled(val)
            self.ui.groupBox_6.setEnabled(val)
            self.ui.groupBox_PZT.setEnabled(val)
        EnableUIscan(False)
        self.SetWavelength(self.laser.scan_limit[0])

        # -- define the thread worker -- 
        @pyqtSlot(tuple)
        def _doScan(signal):
            # [0] Code for where the  program is in
            # the algorithm:
            #     -1 : no scan / end of scan
            #     0 : setting up the start of scan
            #     1 : scanning
            #     2: return wavemeter of begining of scan
            #     3: return wavemeter at end of scan
            # [1] Laser current wavelength
            # [2] Progress bar current %
            # [3] Blinking State
            state = signal[0]
            lbd = signal[1]
            prgrs = signal[2]
            data = signal[3]
            self.ui.progressBar.setValue(prgrs)
            if state == 2:
                self._lbd_start = lbd
                self.ui.line_wlmLbd.setText("{:.3f}".format(lbd))
            if state == 3:
                self._lbd_stop = lbd
                self.ui.line_wlmLbd.setText("{:.3f}".format(lbd))
            if state == -1:
                self._dcData = data
                self._do_blink = False
                self.ui.spnbx_lbd.blockSignals(True)
                self.ui.spnbx_lbd.setValue(self.laser.lbd)
                self.ui.spnbx_lbd.blockSignals(False)

                ut.ReplaceData(self, self._dcData[1], self._dcData[0])
                EnableUIscan(True)


        # -- retrieve params --
        if self.ui.check_calib_lbd.isChecked():
            self.wavemeter = Wavemeter()
            self._param['wlmParam'] = {'channel': int(self.ui.combo_vlmChan.currentText()),
                                      'exposure': 'auto'}
        self._param['daqParam'] = {'read_ch': [self.ui.combo_daqRead.currentText(),
                                            self.ui.combo_daqMZ.currentText()],
                                    'dev': self.ui.combo_daqDev.currentText(),
                                    'write_ch': None}
        
        # -- Set to the start wavelength -- 
        if not np.abs(self.laser.lbd - self.laser.scan_limit[0]) < 0.02:
            self.laser.lbd = self.laser.scan_limit[0]


        self.threadDcWorker = DcScan(laser= self.laser,
                                    wavemeter= self.wavemeter,
                                    param=self._param)
        self.threadDcWorker._DCscan[tuple].connect(_doScan)
        self.threadDcWorker.start()



    # -- Utilities --
    # -----------------------------------------------------------------------------
    def FetchDaqParam(self):
        pass

    @blockSignals(True)
    @blockSignals(False)
    def RetrieveLaser(self):
        print("retrieving data")

        # for some reasom there is a bug disable the signal with this guy
        self.ui.spnbx_lbd_start.blockSignals(True)

        lbd = self.laser.lbd
        pzt = self.laser.pzt
        scan_lim = self.laser.scan_limit
        scan_speed = self.laser.scan_speed
        output = self.laser.output
        print('-'*30)
        print("Fetching error {}".format(self.laser.error))
        print("Laser output: {}".format(output))
        print('-'*30)

        self.ui.spnbx_lbd.setValue(lbd)
        self.ui.slide_pzt.setValue(pzt * 100)
        self.ui.spnbx_pzt.setValue(pzt)
        self.ui.spnbx_lbd_start.setValue(scan_lim[0])
        self.ui.spnbx_lbd_stop.setValue(scan_lim[1])
        self.ui.spnbx_speed.setValue(scan_speed)

       
        if output:
            self.ui.led_laserOut.setPixmap(self._led[True])
        else:
            self.ui.led_laserOut.setPixmap(self._led[False])

        # patch for this signal
        self.ui.spnbx_lbd_start.blockSignals(False)


if __name__ == "__main__":
    app = QApplication([])
    window = Transmission()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    sys.exit(app.exec_())
