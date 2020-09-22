# Import PyQt wrappers
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QFontDatabase
from PyQt5 import uic
from PyQt5 import QtGui
import PyQt5

# import utility packages
# import visa
import ipdb
import os
import sys
import re
import time
import numpy as np
# import ctypes
from os.path import expanduser

from thorlabspiezo import Piezo
# from ThreadPs4Controller import Ps4Thread
work_dir = path = os.path.abspath(__file__ + '/..')
print(work_dir)
# -- import custom NIST-ucomb Package --
path = os.path.abspath(work_dir + '/UI/QDarkStyleSheet-master/qdarkstyle/')

if not path in sys.path:
    sys.path.insert(0, path)
path = os.path.abspath(work_dir + '/../')

Ui_MainWindow, QtBaseClass = uic.loadUiType(work_dir + '/UI/PiezoControl.ui')
Ui_InstrWindow, QtBaseClass = uic.loadUiType(work_dir + '/UI/InstrumentAddress.ui')




class InstrAddr(QMainWindow):
    def __init__(self, parent=None):
        super(InstrAddr, self).__init__(parent)
        self.ui = Ui_InstrWindow()
        self.ui.setupUi(self)



class Stage(QMainWindow):
    changedValue = pyqtSignal(QObject)
    sliderPiezoMoved = pyqtSignal(tuple)


    def __init__(self):
        super(Stage, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connected = False
        self._slidefact = 1e3
        # Set Led Pixmap
        self._ledoff = QtGui.QPixmap(':/qss_icons/rc/radio_checked.png')
        self._ledon = QtGui.QPixmap(':/qss_icons/rc/radio_checked_focus.png')

        # set the led to off at first
        self.ui.led_leftPiezo.setPixmap(self._ledoff)
        self.ui.led_rightPiezo.setPixmap(self._ledoff)


        self.ui.actionAbout.triggered.connect(self.About)
        # self.ui.actionPS4ControllerHelp.triggered.connect(self.HelpController)

        # Connect the Slots
        self.sliderPiezoMoved.connect(self.ConnectMovePiezo)


        self.instrWin = InstrAddr(parent=self)
        self.ui.actionInstrument_Address.triggered.connect(self.instrWin.show)

        # define the different stuff from UI
        self.SetupDictUI()
        # Connect the Button
        self.ConnectButton()

        # Connect the PS4 Controller
        # try:
        #     self.SetupPs4()
        #     self.ListenPS4()
        # except:
        #     print('NO PS4 CONTROLLER CONNECTED. Restart the software after connecting one.')
# -------------------------------------------------------------------------------
#                           --  Initialize --
# ------------------------------------------------------------------------------
    def SetupDictUI(self):
        self.axis = ['X', 'Y', 'Z']
        self.stages = ['left', 'right']
        self.stageList = [yy + xx for xx in self.axis for yy in self.stages]
        self.piezo_address = {'left': self.instrWin.ui.line_left.text,
                              'right': self.instrWin.ui.line_right.text
                              }
        self.frame = {'left': self.ui.frame_left,
                      'right': self.ui.frame_right, }
        self.framelabel = {'left': self.ui.label_left,
                           'right': self.ui.label_right,}

        self.piezo = {xx: getattr(self.ui, 'piezo_' + xx)
                      for xx in self.stageList}
        self.lcdpiezo = {xx: getattr(self.ui, 'lcdpiezo_' + xx)
                         for xx in self.stageList}

    def ConnectButton(self):
        # connect the step sliders to only allow certain values

        self.ui.pushButtonsync_left.clicked.connect(self.PiezoSync)
        self.ui.pushButtonsync_right.clicked.connect(self.PiezoSync)
        # connect the piezo sliders to only allow better control
        for kk in self.piezo.values():
            kk.valueChanged.connect(self.setPiezo)

        # Connect the button
        self.ui.pushButtonConnect.clicked.connect(self.Connect)
        self.ui.pushButtonExit.clicked.connect(self.Exit)
       

    def About(self):
        msgBox = QMessageBox()
        msgBox.setTextFormat(QtCore.Qt.RichText)
        urlLink = '<a href="mailto:gregory.moille@nist.gov' + \
            '?Subject=Bug%20With%20Toptica%20UI%20Software">' + \
            'this link</a>'
        urlRequest = '<a href="mailto:gregory.moille@nist.gov' + \
            '?Subject=Request%20For%20Toptica%20UI%20Software">' + \
            'this link</a>'
        txt = '<b>Piezo Stage Controller Microcomb Setup - v2.0</b><br><br>Developed by G. Moille<br>' +\
            'National Institute of Standard And Technology<br>' +\
            '20178br><br>' +\
            'Please report through ' + urlLink + \
            '<br>Please report any request though ' + urlRequest
        # ipdb.set_trace()
        msgBox.setWindowTitle(self.tr("About"))
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setText(txt)
        msgBox.exec_()

# -------------------------------------------------------------------------------
#                           --  Connect, Sync & Exit --
# ------------------------------------------------------------------------------
    def PiezoSync(self):
        stage = self.sender().objectName().split('_')[1]
        pzt = self.piezomotor[stage]
        axis = ['X', 'Y', 'Z']
        for aa in axis:
            # time.sleep(0.5)

            pzt.axis = aa
            self.lcdpiezo[stage + aa].display(pzt.V)
            self.piezo[stage+aa].setValue(pzt.V*self._slidefact)

    def Connect(self):
        if not self._connected:
            # -- Connect the step motor --
            # ----------------------------------------------------
            self._connected = True
            self.ui.pushButtonConnect.setEnabled(False)
            self.ui.pushButtonExit.setEnabled(False)

          
            self.piezomotor = {}

            # -- Connect the piezo  --
            # ----------------------------------------------------
            _sucess = True
            for kk in self.piezo_address.keys():
                try:
                    self.piezomotor[kk] = Piezo(address=self.piezo_address[kk]())
                    led = getattr(self.ui, 'led_' + kk + 'Piezo')
                    led.setPixmap(self._ledon)
                    # self.iuobutton.click()
                    syncbut = getattr(self.ui, 'pushButtonsync_' + kk)
                    syncbut.click()
                except Exception as e:
                        print('\033[93m' + '-'*10 + 'EXCEPTION:')
                        print(e)
                        print('-'*10 + 'end exception' + '\033[0m')


                

            self.ui.pushButtonConnect.setEnabled(True)
            self.ui.pushButtonExit.setEnabled(True)

            
        else:
            self.Exit()
            self.stepmotor = {}
            self.piezomotor = {}
            self.Connect()

    def Exit(self):
        self._connected = False
        
        for kk in self.piezomotor:
            self.piezomotor[kk].instr.close()
            led = getattr(self.ui, 'led_' + kk + 'Piezo')
            led.setPixmap(self._ledoff)

# -------------------------------------------------------------------------------
#                           --  Thread Moves --
# ------------------------------------------------------------------------------
    def setPiezo(self):
        try:
            name = self.sender().objectName().split('_')[1]
            slider = self.piezo[name]
            x = slider.value()
            self.sliderPiezoMoved.emit((name,x))
        except:
            pass

    @pyqtSlot(tuple)
    def ConnectMovePiezo(self,strstep):
        name = strstep[0]
        x = strstep[1]
        lcdpiezo = self.lcdpiezo[name]
        lcdpiezo.display(x/self._slidefact)

        # retrieve axis and name
        axis = re.split('left|right', name)[1]
        stage = name.split(axis)[0]

        pzt = self.piezomotor[stage]
        if self._connected:
            pzt.axis = axis
            pzt.V = x/self._slidefact
            lcdpiezo.display(x/self._slidefact)

# -------------------------------------------------------------------------------
#                           --  Main --
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    myappid = 'NIST.stagecontrol.ui.1'  # arbitrary string
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication([])
    app_icon = QtGui.QIcon()
    # icon = os.getcwd() + '/ressources/IconUI.ico'
    # app_icon.addFile(icon, QtCore.QSize(16, 16))
    # app_icon.addFile(icon, QtCore.QSize(24, 24))
    # app_icon.addFile(icon, QtCore.QSize(32, 32))
    # app_icon.addFile(icon, QtCore.QSize(48, 48))
    # app_icon.addFile(icon, QtCore.QSize(256, 256))
    # app.setWindowIcon(app_icon)
    window = Stage()
    window.show()
    sys.exit(app.exec_())
