#!/usr/bin/env python

# -- Import PyQt wrappers --
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QPointF
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
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
from pyLaser import NewFocus6700
from pyWavemeter import Wavemeter
from workers import DcScan, FreeScan

# -- load UI --
print('-'*30)
print(work_dir)
print('-'*30)
Ui_MainWindow, QtBaseClass = uic.loadUiType(work_dir + '/UI/UITranmission.ui')
Ui_DevWindow, QtBaseClass = uic.loadUiType(work_dir + '/UI/DevWindow.ui')
Ui_InstrWindow, QtBaseClass = uic.loadUiType(
    work_dir + '/UI/InstrumentAddress.ui')


class ErrorHandling(QThread):
    err_msg = pyqtSignal(str)

    def __init__(self, main_app):
        QThread.__init__(self)
        self.main_app = main_app
        self._probe = 0
        self._isRunning = True
        self.old_err = ''

    def run(self):
        self._isRunning = True
        print('Doing First stuff!!!!')
        while self._isRunning:
            if not self.old_err == str(self.main_app.laser._err_msg):
                self.old_err = str(self.main_app.laser._err_msg)
                self.main_app._has_err = True
                self.err_msg.emit(self.old_err)
                print('doing stuff')

    def stop(self):
        self._isRunning = False


class DevWind(QMainWindow):
    def __init__(self, parent=None):
        super(DevWind, self).__init__(parent)
        self.ui = Ui_DevWindow()
        self.ui.setupUi(self)
        self.ui.butt_clearError.clicked.connect(lambda: self.ClearError(True))

        self.parent = parent
        self.ui.text_lastError.setText('')
        # self.GetLaserErr()
        # self.ui.butt_getLaserErr.clicked.connect(self.GetLaserErr)

    def ClearError(self, val):

        self.parent._has_err = False
        self.parent._has_checked_err = False
        print('Puting back everything')
        self.parent.ui.wdgt_param.setEnabled(val)
        self.parent.ui.wdgt_plot.setEnabled(val)
        if val:
            self.parent.laser._err_msg = '\n'
            dumm = self.parent.laser.error

    def GetLaserErr(self):
        @pyqtSlot(str)
        def _updateErr(val):

            self.parent._do_blink = False
            # self.parent.ui.wdgt_param.setEnabled(False)
            # self.parent.ui.wdgt_plot.setEnabled(False)
            ts = time.time()
            timestamp = datetime.fromtimestamp(
                ts).strftime('%Y-%m-%d %H:%M:%S')
            self.ui.text_lastError.setText(timestamp + ' -- ' + val)

        self.old_err = self.parent.laser._err_msg
        self.threadErr = ErrorHandling(main_app=self.parent)
        self.threadErr.err_msg[str].connect(_updateErr)
        self.threadErr.start()

    def StopErr(self):
        self.threadErr.stop()
        self.ClearError(False)
        self.threadErr.quit()
        self.threadErr.wait()


class InstrAddr(QMainWindow):
    def __init__(self, parent=None):
        super(InstrAddr, self).__init__(parent)
        self.ui = Ui_InstrWindow()
        self.ui.setupUi(self)


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
        self._showhline = False

        # -- connect buttons --
        self.ui.but_connect.clicked.connect(self.Connect)
        self.ui.but_laserOut.clicked.connect(self.LaserOut)
        self.ui.but_dcscan.clicked.connect(self.Scan)
        self.ui.but_freeScan.clicked.connect(self.FreeScan)
        self.ui.but_DownS.clicked.connect(self.DownSampleTrace)
        self.ui.but_setdir.clicked.connect(self.ChosePath)
        self.ui.but_savedata.clicked.connect(self.SaveData)
        self.ui.but_DataTip.clicked.connect(lambda: ut.ShowDataTip(self))
        self.ui.but_ClearPlot.clicked.connect(self.ClearDiaplayPlot)

        # -- connect spin boxes --
        self.ui.spnbx_pzt.valueChanged[float].connect(self.Pzt_Value)
        self.ui.spnbx_lbd.valueChanged[float].connect(self.SetWavelength)
        self.ui.spnbx_lbd_start.valueChanged[float].connect(self.ScanLim)
        self.ui.spnbx_lbd_stop.valueChanged[float].connect(self.ScanLim)
        self.ui.spnbx_speed.valueChanged[float].connect(self.ScanSpeed)

        # -- connect sliders --
        self.ui.slide_pzt.valueChanged[int].connect(
            lambda x: self.ui.spnbx_pzt.setValue(x/self._cst_slide))

        # -- connect checkBoxes --
        # ipdb.set_trace()
        self.ui.check_lbdMZ.stateChanged.connect(self.PlotCalibrated)

        # -- Create a graph --
        ut.CreatePyQtGraph(self, [1500, 1600], self.ui.mplvl)
        self.my_plot.scene().sigMouseMoved.connect(self.onMove)
        # -- Setup apparence at launch --
        # self.ui.wdgt_param.setEnabled(False)
        # self.ui.wdgt_plot.setEnabled(False)
        self.ui.group_PostProc.setEnabled(False)
        # -- Misc --
        self._do_blink = False
        self.wlm = None
        self.laser = None
        self._olderr = ''
        self._has_err = False
        self._has_checked_err = False
        self._doClear = True
        self._param = {}
        self._postproc = False
        self.dev = DevWind(parent=self)
        self.ui.actionGet_Errors.triggered.connect(self.dev.show)

        self.instrWin = InstrAddr(parent=self)
        self.ui.actionSet_Instrument_Address.triggered.connect(
            self.instrWin.show)

    # -----------------------------------------------------------------------------
    # -- Some Decorators --
    # -----------------------------------------------------------------------------
    def Blinking(fun):
        '''
        Blinking decorator when changing wavelength
        '''
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
                    time.sleep(0.6)
                    cdt = self_app.laser._is_changing_lbd

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

    def isConnected(fun):
        '''
        Decorator checking of laser connected to perform or no 
        the operation
        '''
        @wraps(fun)
        def wrapper(*args, **kwargs):
            print('Check if Connected')
            self_app = args[0]
            if self_app._connected:
                out = fun(*args, **kwargs)
            else:
                out = None
                self_app.dev.ui.text_lastError.setText(
                    'Laser is not connected')
            return out
        return wrapper

    def hasError(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            print('Check if has error')
            self_app = args[0]
            # old = self_app.RetrieveLaser()
            out = fun(*args, **kwargs)
            if self_app._has_err and not self_app._has_checked_err:
                self_app.ui.wdgt_param.setEnabled(False)
                self_app.ui.wdgt_plot.setEnabled(False)
                self_app._do_blink = False
                self_app.RetrieveLaser()
                self_app._has_checked_err = True
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
                        'spnbx_lbd_start', 'spnbx_lbd_start',
                        'spnbx_lbd_stop', 'spnbx_speed']

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
                print('Connected... fetching Wavelength')
                self.ui.but_connect.setText('Disconnect')
                self._connected = True
                self.RetrieveLaser()
                self.dev.GetLaserErr()

            except Exception as err:
                err = str(err) + \
                    '\nLaser is not connected, please try to connect it.'
                self.dev.ui.text_lastError.setText(err)
        else:
            try:
                print('-'*30)
                print('Disconnecting')
                print('-'*30)
                self.dev.StopErr()
                time.sleep(0.2)
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
    def LaserOut(self, val):
        out = self.laser.output
        if out:
            self.laser.output = False
            self.ui.led_laserOut.setPixmap(self._led[False])
        else:
            self.laser.output = True
            self.ui.led_laserOut.setPixmap(self._led[True])

    @hasError
    @isConnected
    @Blinking
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

    # -----------------------------------------------------------------------------
    # -- DC Scan --
    # -----------------------------------------------------------------------------
    @isConnected
    def Scan(self, value):
        self._do_blink = True
        self._postproc = True

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
                # data returned
                # (tdaq, time_probe,lbd_probe,, lbd_daq [T, MZ])
                self._data = {'tdaq': data[0],
                              't_laser': data[2],
                              'lbd_Laser': data[3],
                              'lbd_daq': data[4],
                              'T': data[5][0],
                              'MZ': data[5][1]}
                self._toPlot = [self._data['lbd_daq'], self._data['T']]
                self._do_blink = False
                self.ui.spnbx_lbd.blockSignals(True)
                self.ui.spnbx_lbd.setValue(self.laser.lbd)
                self.ui.spnbx_lbd.blockSignals(False)
                ut.ReplaceData(self, self._toPlot[0], self._toPlot[1])
                EnableUIscan(True)
                self.threadDcWorker.stop()
                self.threadDcWorker.quit()
                self.threadDcWorker.wait()
                self.ui.group_PostProc.setEnabled(self._postproc)
        # -- retrieve params --
        if self.ui.check_calib_lbd.isChecked():
            self.wavemeter = Wavemeter()
            ch = int(self.ui.combo_vlmChan.currentText())
            self._param['wlmParam'] = {'channel': ch,
                                       'exposure': 'auto'}
        daqDev = self.instrWin.ui.combo_daqDev.currentText()
        daqTch = self.ui.combo_daqRead.currentText()
        daqMZch = self.ui.combo_daqMZ.currentText()
        self._param['daqParam'] = {'read_ch': [daqTch, daqMZch],
                                   'dev': daqDev,
                                   'write_ch': None}

        # -- Set to the start wavelength --
        if not np.abs(self.laser.lbd - self.laser.scan_limit[0]) < 0.02:
            self.SetWavelength(self.laser.scan_limit[0])
            time.sleep(0.15)

        self.threadDcWorker = DcScan(laser=self.laser,
                                     wavemeter=self.wavemeter,
                                     param=self._param,
                                     debug=True)
        self.threadDcWorker._DCscan[tuple].connect(_doScan)
        self.threadDcWorker.start()

    def PlotCalibrated(self, val):
        if val is 2:
            print('plotting calibrated stuff')
        if val is 0:
            print('plotting normal stuff')

    # -----------------------------------------------------------------------------
    # -- Free Scan --
    # -----------------------------------------------------------------------------
    # @isConnected
    def FreeScan(self, val):
        self._postproc = False

        def _enable(val):
            self.ui.but_dcscan.setEnabled(val)
            self.ui.but_pztscan.setEnabled(val)
            self.ui.group_plotSetting.setEnabled(val)
            self.ui.but_savedata.setEnabled(val)
            if val:
                self.ui.group_PostProc.setEnabled(self._postproc)

        @pyqtSlot(list)
        def _doFreeScan(l):
            data = np.array(l)
            x = np.linspace(0, 100, data.size)
            self._toPlot = [x, data]
            ut.ReplaceData(self, self._toPlot[0], self._toPlot[1])

        if val:
            self.ui.but_freeScan.setText('Stop Scan')
            _enable(False)
            daqTch = self.ui.combo_daqRead.currentText()
            daqDev = self.instrWin.ui.combo_daqDev.currentText()
            self._param['daqParam'] = {'read_ch': [daqTch],
                                       'dev': daqDev,
                                       'write_ch': None}

            self.threadFreeWorker = FreeScan(laser=self.laser,
                                             param=self._param,
                                             debug=True)
            self.threadFreeWorker._Freescan[tuple].connect(_doFreeScan)
            self.threadFreeWorker.start()

        else:
            self.ui.but_freeScan.setText('Free Scan')
            _enable(True)
            self.threadFreeWorker.stop()
            self.threadFreeWorker.quit()
            self.threadFreeWorker.wait()

    # -----------------------------------------------------------------------------
    # -- Saving and stuff --
    # -----------------------------------------------------------------------------
    def ChosePath(self):
        # Open the popup window to pick a directory
        dir_ = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Select Directory", os.path.expanduser("Z:\\"),
            QtGui.QFileDialog.ShowDirsOnly))
        self.ui.text_Dir.setText(dir_.strip())
        # self.UpdateDir()

    def SaveData(self):
        _save = True

        # Check that directory was picked
        drcty = self.ui.text_Dir.text().strip()
        fname = self.ui.text_File.text().strip()
        ext = self.ui.comboBox_Extension.currentText()
        if drcty == '':
            _save = False
            self.ui.text_Dir.setText('Chose a directory!')
        if fname == '':
            _save = False
            self.ui.text_File.setText('Chose a File Name!')
        if _save:
            if ext == '.mat':
                filename = drcty + '\\' + fname + '.mat'
                io.savemat(filename, self._data)
            if ext == '.dill':
                filename = drcty + '\\' + fname + '.dill'
                with open(filename, 'bw') as fn:
                    dill.dump(self._data, fn)
            if ext == 'all':
                filename = drcty + '\\' + fname
                io.savemat(filenamem + '.mat', self._data)
                with open(filename + '.dill', 'bw') as fn:
                    dill.dump(self._data, fn)

    # -----------------------------------------------------------------------------
    # -- Utilities --
    # -----------------------------------------------------------------------------
    def RetrieveLaser(self, old=None):
        # for some reasom there is a bug disable the signal with this guy
        self.ui.spnbx_lbd_start.blockSignals(True)
        self.ui.spnbx_lbd.blockSignals(True)
        self.ui.slide_pzt.blockSignals(True)
        self.ui.spnbx_pzt.blockSignals(True)
        self.ui.spnbx_lbd_start.blockSignals(True)
        self.ui.spnbx_lbd_start.blockSignals(True)
        self.ui.spnbx_lbd_stop.blockSignals(True)
        self.ui.spnbx_speed.blockSignals(True)
        print("retrieving data")

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
        self.ui.spnbx_lbd.blockSignals(False)
        self.ui.slide_pzt.blockSignals(False)
        self.ui.spnbx_pzt.blockSignals(False)
        self.ui.spnbx_lbd_start.blockSignals(False)
        self.ui.spnbx_lbd_start.blockSignals(False)
        self.ui.spnbx_lbd_stop.blockSignals(False)
        self.ui.spnbx_speed.blockSignals(False)
        self._do_blink = False
        self.laser.lbd = lbd

        return {'lbd': lbd,
                'pzt': pzt,
                'scan_lim': scan_lim,
                'scan_speed': scan_speed,
                'output': output, }

    # -----------------------------------------------------------------------------
    # -- Graph Interaction --
    # -----------------------------------------------------------------------------
    def ClearDiaplayPlot(self):
        if self._doClear:
            for line in self.current_trace:
                self.my_plot.removeItem(line)
            self.current_trace = []
            self.ui.but_ClearPlot.setText('Display Plot')
            self._doClear = False
            if self._showhline:
                self.ui.but_DataTip.click()
        else:
            ut.ReplaceData(self, self._toPlot[0], self._toPlot[1])
            self.ui.but_ClearPlot.setText('Clear Plot')
            self._doClear = True

    def DownSampleTrace(self):
        step = self.ui.spnbx_downsample.value()
        if not self._toPlot == []:
            ut.PlotDownSampleTrace(
                self, self._toPlot[0], self._toPlot[1], step)

    def onMove(self, pos):
        if self._showhline:
            if self.vLine.isUnderMouse():
                pen = ut.SetPen(self._clr[self._ind_curve])
                self.hLine.setPen(pen)
                self.vLine.setPen(pen)
                xline = self.vLine.getXPos()
                x = self.current_trace[self._ind_curve].getData()[0]
                y = self.current_trace[self._ind_curve].getData()[1]
                ind = np.abs(x-xline).argmin()
                xcur = x[ind]
                ycur = y[ind]
                # xlim = self.my_plot.getXRange()
                # ylim = self.my_plot.getYRange()
                # ipdb.set_trace()
                xlim = self.my_plot.getPlotItem().getAxis('bottom').range
                ylim = self.my_plot.getPlotItem().getAxis('left').range
                xpos = xlim[0] + 0.025*np.diff(xlim)[0]
                ypos = ylim[0] + 0.025*np.diff(ylim)[0]
                self.txt.setPos(QPointF(xpos, ypos))
                self.txt.setText(
                    "lbd = {:.3f} nm – {:.3f} V".format(xcur, ycur))
                # self.ui.xPos.setText("{:.3f}".format(xcur) + 'nm')
                # self.ui.yPos.setText("{:.3f}".format(ycur) + 'V')
                self.vLine.setPos([xcur, 0])
                self.hLine.setPos([0, ycur])

    # -----------------------------------------------------------------------------
    # -- Help and About --
    # -----------------------------------------------------------------------------
    def Help(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setTextFormat(QtCore.Qt.RichText)
        txt = 'OK Go see the GitHub Page'
        # ipdb.set_trace()
        msgBox.setWindowTitle(self.tr("Help"))
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setText(txt)
        msgBox.exec_()

    def About(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setTextFormat(QtCore.Qt.RichText)
        urlLink = '<a href="mailto:gregory.moille@nist.gov' + \
            '?Subject=Bug%20With%20Transmission%20UI%20Software">' + \
            'this link</a>'
        urlRequest = '<a href="mailto:gregory.moille@nist.gov' + \
            '?Subject=Request%20For%Transmission%20UI%20Software">' + \
            'this link</a>'
        txt = '<b>Topica UI - v2.0</b><br><br>Developed by G. Moille<br>' +\
            'National Institute of Standards And Technology<br>' +\
            '2019br><br>' +\
            'Please report through ' + urlLink + \
            '<br>Please report any request though ' + urlRequest
        # ipdb.set_trace()
        msgBox.setWindowTitle(self.tr("About"))
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setText(txt)
        msgBox.exec_()


if __name__ == "__main__":
    app = QApplication([])
    window = Transmission()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    sys.exit(app.exec_())
