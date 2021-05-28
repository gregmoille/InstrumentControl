# Import PyQt wrappers
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QFontDatabase
from PyQt5 import uic
from PyQt5 import QtGui
import PyQt5


# import utility packages
import visa
import ipdb
import os
import sys
import time
import numpy as np
import ctypes
from os.path import expanduser

import PyThorAPT
from thorlabspiezo import Piezo
from newfocusstage import NFstage
from stepthreads import StepThread, GoHomeThread
from ThreadPs4Controller import Ps4Thread

Ui_MainWindow, QtBaseClass = uic.loadUiType('StageControll.ui')


class Stage(QMainWindow):
    changedValue = pyqtSignal(QObject)
    buttonMoved = pyqtSignal(tuple)
    sliderMoved = pyqtSignal(tuple)

    def __init__(self):
        super(Stage, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connected = False

        # Set Led Pixmap
        self._ledoff = QtGui.QPixmap(os.getcwd() + '/ressources/led-off.png')
        self._ledon = QtGui.QPixmap(os.getcwd() + '/ressources/led-on.png')

        # define the different stuff from UI
        self.SetupDictUI()

        # intialize thread dic for step motor
        self.MoveThread = {xx: None for xx in self.stageList}
        self.WorkerStep = {xx: None for xx in self.stageList}
        self.HomeThread = {xx: None for xx in self.stageList}
        self.WorkerHome = {xx: None for xx in self.stageList}

        # set the led to off at first
        for kk in self.stepLed.values():
            kk.setPixmap(self._ledoff)
        self.ui.led_leftPiezo.setPixmap(self._ledoff)
        self.ui.led_rightPiezo.setPixmap(self._ledoff)
        self.ui.led_Sample.setPixmap(self._ledoff)

        # Connect the Button
        self.ConnectButton()

        # Connect the Slots
        self.ConnectQtSlot()

        # Connect the PS4 Controller
        self.SetupPs4()
        self.ListenPS4()

# -------------------------------------------------------------------------------
#                           --  Initialize --
# ------------------------------------------------------------------------------
    def SetupDictUI(self):
        self.step = np.array([0.0005, 0.001, 0.0025, 0.005,
                              0.01, 0.025, 0.05, 0.1,
                              0.25, 0.5, 1, 2.5, 5, 20])

        self.axis = ['X', 'Y', 'Z']
        self.stages = ['left', 'right']
        self.stageList1 = [yy + xx for xx in self.axis for yy in self.stages]
        self.piezo_address = {'left': 'ASRL8::INSTR',
                              'right': 'ASRL7::INSTR'
                              }
        # adding the microscope, only true for step motor
        # we keep stageList1 for the piezo though
        self.stageList = self.stageList1 + ['micX', 'micZ']

        self.SnStep = {'leftX': 90866217,
                       'leftY': 90866218,
                       'leftZ': 90866219,
                       'rightX': 90868135,
                       'rightY': 90868136,
                       'rightZ': 90868137,
                       'micZ': 27500738,
                       'micX': 27250214,
                       }

        self.frame = {'left': self.ui.frame_left,
                      'right': self.ui.frame_right,
                      'mic': self.ui.frame_mic,
                      'sample': self.ui.frame_sample, }
        self.framelabel = {'left': self.ui.label_left,
                           'right': self.ui.label_right,
                           'mic': self.ui.label_mic,
                           'sample': self.ui.label_sample, }

        self.stepLed = {xx: getattr(self.ui, 'led_' + xx)
                        for xx in self.stageList}
        self.stepSizeSlide = {xx: getattr(
            self.ui, 'step_' + xx) for xx in self.stageList}
        self.stepSizeLCD = {xx: getattr(self.ui, 'lcdstep_' + xx)
                            for xx in self.stageList}
        self.forwardbut = {xx: getattr(self.ui, 'forward_' + xx)
                           for xx in self.stageList}
        self.backwardbut = {xx: getattr(self.ui, 'back_' + xx)
                            for xx in self.stageList}
        self.homebut = {xx: getattr(self.ui, 'home_' + xx)
                        for xx in self.stageList}

        self.lcd = {xx: getattr(self.ui, 'lcd_' + xx) for xx in self.stageList}
        self.piezo = {xx: getattr(self.ui, 'piezo_' + xx)
                      for xx in self.stageList1}
        self.lcdpiezo = {xx: getattr(self.ui, 'lcdpiezo_' + xx)
                         for xx in self.stageList1}

    def ConnectButton(self):
        # connect the step sliders to only allow certain values
        for kk in self.stepSizeSlide.values():
            kk.valueChanged.connect(self.setStep)

        self.ui.pushButtonsync_left.clicked.connect(self.PiezoSync)
        self.ui.pushButtonsync_right.clicked.connect(self.PiezoSync)
        # connect the piezo sliders to only allow better control
        for kk in self.piezo.values():
            kk.valueChanged.connect(self.setPiezo)

        # Connect the button
        self.ui.pushButtonConnect.clicked.connect(self.Connect)
        self.ui.pushButtonExit.clicked.connect(self.Exit)
        for kk in self.forwardbut.keys():
            self.forwardbut[kk].clicked.connect(lambda: self.Move(1))
        for kk in self.backwardbut.keys():
            self.backwardbut[kk].clicked.connect(lambda: self.Move(-1))

        for kk in self.homebut.values():
            kk.clicked.connect(self.HomeStage)

        self.ui.sample_forward.pressed.connect(
            lambda: self.StopMoveSample(True))
        self.ui.sample_forward.released.connect(
            lambda: self.StopMoveSample(False))
        self.ui.sample_backward.pressed.connect(
            lambda: self.StopMoveSample(True))
        self.ui.sample_backward.released.connect(
            lambda: self.StopMoveSample(False))

    def ConnectQtSlot(self):
        self.buttonMoved.connect(self.MoveAxis)
        self.sliderMoved.connect(self.MoveStep)
    def SetupPs4(self):
        self._controllui = 'left'
        self._controlui_axis = 'X'
        self._oldtime_res = time.time()
        self.ArrowPs4 = {'DpadUp': 0,
                         'DpadDown': 0,
                         'DpadRight': 1,
                         'DpadLeft': -1,
                         }
        self.Ps4Axis = ['AnalogLx',
                        'AnalogLy',
                        'AnalogRx',
                        'AnalogRy', ]

        self.switchFrame = {'R2': 'right',
                            'L2': 'left',
                            'L1': 'mic',
                            'R1': 'sample'}
        self.switchAxis = {'Triangle': 'Z',
                            'Cross': 'X',
                            'Circle': 'Y'}
# -------------------------------------------------------------------------------
#                           --  Connec, Sync & Exit --
# ------------------------------------------------------------------------------

    def PiezoSync(self):
        stage = self.sender().objectName().split('_')[1]
        axis = ['X', 'Y', 'Z']
        if stage == 'left':
            kk = 'left'
            for aa in axis:
                # time.sleep(0.5)
                V = self.piezomotor[kk].GetVoltage(aa.lower())
                self.lcdpiezo[kk + aa].display(V)
                self.piezo[kk+aa].setValue(V*1e2)

        if stage == 'right':
            kk = 'right'
            for aa in axis:
                # time.sleep(0.5)
                V = self.piezomotor[kk].GetVoltage(aa.lower())
                self.lcdpiezo[kk + aa].display(V)
                self.piezo[kk+aa].setValue(V*1e2)

    def Connect(self):
        if not self._connected:
            # -- Connect the step motor --
            # ----------------------------------------------------
            self.stepmotor = {}
            self.stepstatus = {}
            self._connected = True
            self.ui.pushButtonConnect.setEnabled(False)
            self.ui.pushButtonExit.setEnabled(False)

            for kk in self.stageList:
                self.stepmotor[kk] = PyThorAPT.APTMotor(SN=self.SnStep[kk],
                                                        verbose=0)
                self.stepstatus[kk] = False
                res = self.stepmotor[kk].InitializeHardwareDevice()
                if res == 0:
                    self.stepLed[kk].setPixmap(self._ledon)
                    QApplication.processEvents()

            try:
                for kk in self.stageList:
                    pos = self.stepmotor[kk].getPos()
                    self.lcd[kk].display(pos*1e3)
            except:
                pass
            self.piezomotor = {}

            # -- Connect the piezo  --
            # ----------------------------------------------------
            _sucess = True
            for kk in self.piezo_address.keys():
                try:
                    self.piezomotor[kk] = Piezo(address=self.piezo_address[kk])
                    led = getattr(self.ui, 'led_' + kk + 'Piezo')
                    led.setPixmap(self._ledon)
                    # self.iuobutton.click()
                    syncbut = getattr(self.ui, 'pushButtonsync_' + kk)
                    syncbut.click()
                except:
                    pass

            self.ui.pushButtonConnect.setEnabled(True)
            self.ui.pushButtonExit.setEnabled(True)

            # -- connect the sample stage --
            # ----------------------------------------------------
            self.samplestage = NFstage(address='169.254.122.10')
            self.ui.led_Sample.setPixmap(self._ledon)
        else:
            self.Exit()
            self.stepmotor = {}
            self.Connect()

    def Exit(self):
        self._connected = False
        for kk in self.stageList:
            self.stepmotor[kk].cleanUpAPT()
            self.stepLed[kk].setPixmap(self._ledoff)
            QApplication.processEvents()
        for kk in self.piezomotor:
            self.piezomotor[kk].instr.close()
            led = getattr(self.ui, 'led_' + kk + 'Piezo')
            led.setPixmap(self._ledoff)

        self.samplestage.instr.close()
        self.ui.led_Sample.setPixmap(self._ledoff)

# -------------------------------------------------------------------------------
#                           --  Settings --
# ------------------------------------------------------------------------------

    def setStep(self):
        try:
            name = self.sender().objectName().split('_')[1]
            slider = self.stepSizeSlide[name]
            x = slider.value()
            self.sliderMoved.emit((name,x))
        except:
            pass

    def setPiezo(self):
        name = self.sender().objectName().split('_')[1]
        slider = self.piezo[name]
        print(name)
        lcd = self.lcdpiezo[name]
        x = slider.value()
        # print(x)
        # lcd.display(x/1e2)
        if self._connected:
            if 'left' in name:
                axis = name.split('left')[1].lower()
                self.piezomotor['left'].SetVoltage(x/1e2, axis)
                # V =  self.piezomotor['left'].GetVoltage(axis)
                lcd.display(x/1e2)

            if 'right' in name:
                axis = name.split('right')[1].lower()
                self.piezomotor['right'].SetVoltage(x/1e2, axis)
                # time.sleep(0.05)
                # V =  self.piezomotor['right'].GetVoltage(axis)
                lcd.display(x/1e2)

# -------------------------------------------------------------------------------
#                           --  Move --
# ------------------------------------------------------------------------------

    def StopMoveSample(self, move):
        if self._connected:
            if move:
                res = self.ui.stage_Resolution.currentText().lower()
                drction = self.sender().objectName().split('_')[1]
                self.samplestage.StartMotion(drction, res)
            else:
                self.samplestage.StopMotion()
                print('STOP!!!!')

    def Move(self, coef):
        butt_name = self.sender().objectName()
        print('-'*60)
        print(butt_name)
        print('-'*60)

        self.buttonMoved.emit((butt_name, coef))

    def HomeStage(self):
        name = self.sender().objectName().split('_')[1]
        print(name)
        if self._connected:
            # ipdb.set_trace()
            motor = self.stepmotor[name]
            self.HomeThread[name] = QThread(self)
            self.WorkerHome[name] = GoHomeThread(stage=motor,
                                                 name=name)
            self.WorkerHome[name].signal_done[dict].connect(self.ReleaseHome)
            self.WorkerHome[name].moveToThread(self.HomeThread[name])
            self.HomeThread[name].started.connect(self.WorkerHome[name].Home)

            self.homebut[name].setEnabled(False)

            self.HomeThread[name].start()

# -------------------------------------------------------------------------------
#                           --  Thread Moves --
# ------------------------------------------------------------------------------
    @pyqtSlot(tuple)
    def MoveAxis(self, straxis):
        name = straxis[0]
        coef = straxis[1]
        print('-'*60)
        print('Received:')
        print(name)
        print(coef)
        print('-'*60)
        print(coef)
        if self._connected:
            # ipdb.set_trace()
            motor = self.stepmotor[name]
            pos = motor.getPos()
            stepbox = self.stepSizeLCD[name]
            step = coef * stepbox.value() * 1e-3
            new_pos = pos + step

            self.MoveThread[name] = QThread(self)
            self.WorkerStep[name] = StepThread(pos=new_pos,
                                               stage=motor,
                                               name=name)
            self.WorkerStep[name].signal_done[dict].connect(self.ReleaseButton)
            self.WorkerStep[name].moveToThread(self.MoveThread[name])
            self.MoveThread[name].started.connect(self.WorkerStep[name].Move)

            self.backwardbut[name].setEnabled(False)
            self.forwardbut[name].setEnabled(False)

            self.MoveThread[name].start()

    @pyqtSlot(tuple)
    def MoveStep(self,strstep):
        name = strstep[0]
        x = strstep[1]
        print(name)
        lcd = self.stepSizeLCD[name]
        # x = slider.value()
        print(x)
        step = self.step[x]
        lcd.display(step*1e3)

    @pyqtSlot(dict)
    def ReleaseButton(self, dctMove):
        name = dctMove['name']
        done = dctMove['done']
        pos = dctMove['pos']

        lcd = self.lcd[name]
        self.backwardbut[name].setEnabled(True)
        self.forwardbut[name].setEnabled(True)

        if done:
            lcd.display(pos*1e3)

        self.WorkerStep[name].stop()
        self.MoveThread[name].quit()

    @pyqtSlot(dict)
    def ReleaseHome(self, dctHome):
        name = dctHome['name']
        done = dctHome['done']
        pos = dctHome['pos']
        lcd = self.lcd[name]
        self.homebut[name].setEnabled(True)
        if done:
            lcd.display(pos*1e3)
        self.WorkerHome[name].stop()
        self.HomeThread[name].quit()

# -------------------------------------------------------------------------------
#                           --  Ps4 Function --
# ------------------------------------------------------------------------------
    def ListenPS4(self):
        self._isConnect = True
        self.ThreadPS4 = QThread(self)
        self.WorkerPS4 = Ps4Thread()
        self.WorkerPS4.signalPs4[dict].connect(self.PrintController)
        self.WorkerPS4.moveToThread(self.ThreadPS4)
        self.ThreadPS4.started.connect(self.WorkerPS4.listen)

        # self.ui.pushButton_Connect.setText('Disconnect')
        self.ThreadPS4.start()

    def MoveJoystick(self,butt_name,butt_dir):
        self._oldtime_res = time.time()
        # retrieve direction
        if butt_dir == 'forward':
            coef = 1
        if butt_dir =='back':
            coef = -1

        but = getattr(self.ui, butt_dir + '_' + butt_name)
        # ipdb.set_trace()
        QApplication.processEvents()
        but.setDown(True)
        QApplication.processEvents()
        but.setDown(True)

        QApplication.processEvents()
        time.sleep(0.1)
        self.buttonMoved.emit((butt_name, coef))
        but.setDown(False)
        but.setDown(False)
        QApplication.processEvents()

    def ClickArrow(self,but_name,butt_dir):
        self._oldtime_res = time.time()
        slider = self.stepSizeSlide[but_name]
        val = slider.value()
        print(val)
        if butt_dir == 1:
            if val<len(self.step) -1:
                print(val+butt_dir)
                slider.setValue(val+butt_dir)
                self.sliderMoved.emit((but_name,val+butt_dir))
        if butt_dir == -1:
            if val>0:
                print(val+butt_dir)
                slider.setValue(val+butt_dir)
                self.sliderMoved.emit((but_name,val+butt_dir))
        
            

    def SetAxis(self, buttons):
        boldFont = QFont()
        boldFont.setBold(True)
        normFont = QFont()
        normFont.setBold(False)

        def SetLabel(axis):
            # put normal font on previous one
            labl = getattr(self.ui,'label_' +self._controllui + self._controlui_axis ) 
            labl.setFont(normFont)
            fr  =  getattr(self.ui,'frame_' +self._controllui + self._controlui_axis ) 
            fr.setLineWidth(0)
            fr.setMidLineWidth(0)
            # set new_axis
            self._controlui_axis = axis
            labl = getattr(self.ui,'label_' +self._controllui + self._controlui_axis ) 
            labl.setFont(boldFont)
            fr  =  getattr(self.ui,'frame_' +self._controllui + self._controlui_axis ) 
            fr.setLineWidth(1)
            fr.setMidLineWidth(1)

        if buttons:
            # X axis
            if buttons[0] == 'Cross':
                # check if not in sample stage
                if not self._controllui == 'sample':
                    SetLabel('X')
            # Y axis
            if buttons[0] == 'Circle':
                if not self._controllui == 'mic':
                    SetLabel('Y')
            #Z axis
            if buttons[0] == 'Triangle':
                if not self._controllui == 'sample':
                    SetLabel('Z')

    def SetFrame(self, buttons):
        boldFont = QFont()
        boldFont.setBold(True)
        normFont = QFont()
        normFont.setBold(False)

        def SetFrameStyle(nameframe):    
            otherframe = [xx for xx in self.frame.keys() if xx != nameframe]
            self.frame[nameframe].setLineWidth(1)
            self.frame[nameframe].setMidLineWidth(1)
            self.framelabel[nameframe].setFont(boldFont)

            for ff in otherframe:
                self.frame[ff].setLineWidth(0)
                self.frame[ff].setMidLineWidth(0)
                self.framelabel[ff].setFont(normFont)

        if buttons:
            labl = getattr(self.ui,'label_' +self._controllui + self._controlui_axis )
            labl.setFont(normFont)
            fr  =  getattr(self.ui,'frame_' +self._controllui + self._controlui_axis ) 
            fr.setLineWidth(0)
            fr.setMidLineWidth(0)
            if buttons[0] == 'R2':
                SetFrameStyle(self.switchFrame['R2'])
                self._controllui = self.switchFrame['R2']
            if buttons[0] == 'L2':
                SetFrameStyle(self.switchFrame['L2'])
                self._controllui = self.switchFrame['L2']
            if buttons[0] == 'R1':
                SetFrameStyle(self.switchFrame['R1'])
                self._controllui = self.switchFrame['R1']
            if buttons[0] == 'L1':
                SetFrameStyle(self.switchFrame['L1'])
                self._controllui = self.switchFrame['L1']


            if not buttons[0] == 'R1':
                if self._controlui_axis == 'Y':
                    if self._controllui == self.switchFrame['L1']:
                        self._controlui_axis = 'X'
                labl = getattr(self.ui,'label_' +self._controllui + self._controlui_axis )
                labl.setFont(boldFont)
                fr  =  getattr(self.ui,'frame_' +self._controllui + self._controlui_axis ) 
                fr.setLineWidth(1)
                fr.setMidLineWidth(1)
            else:
                self._controlui_axis = 'Y'
                labl = getattr(self.ui,'label_' +self._controllui + self._controlui_axis )
                labl.setFont(boldFont)
                fr  =  getattr(self.ui,'frame_' +self._controllui + self._controlui_axis ) 
                fr.setLineWidth(1)
                fr.setMidLineWidth(1)

    def RetrieveActiveButtPs4(self, ps4Buttons):
        keyTrue = [kk for kk in ps4Buttons.keys() if ps4Buttons[kk]]
        if keyTrue:
            keyTrue = keyTrue
        return keyTrue

    def RetrieveActiveAxisPs4(self,ps4Joystick):
        # retrieve the axis moving more than half of the way
        keyTrue = [kk for kk in ps4Joystick.keys() if np.abs(ps4Joystick[kk])>0.5]
        Direction = {}
        dirlist = {-1:'back', 1: 'forward'}
        if keyTrue:
            # retrieve direction
            kk = keyTrue[0]
            Direction[kk]  = np.sign(ps4Joystick[kk])

        return Direction

# -------------------------------------------------------------------------------
#                           --  PS4 Threads Slot --
# ------------------------------------------------------------------------------
    @pyqtSlot(dict)
    def PrintController(self, dic):
        self.ps4Buttons = dic['button']
        self.ps4Joystick = dic['axis']
        buttons = self.RetrieveActiveButtPs4(self.ps4Buttons)
        axis = self.RetrieveActiveAxisPs4(self.ps4Joystick)
        # Change the focus if changed
        self.SetFrame(buttons)
        
        # Change the Axis
        self.SetAxis(buttons)

        # Test if active if in the Arrows
        if buttons:
            activearrow = buttons[0]
            # test if the button exist -> handling error with mic or sample
            try:
                butt_dir = self.ArrowPs4[activearrow]
                butt_name = self._controllui + self._controlui_axis
                cur_time = time.time()
                if cur_time - self._oldtime_res > 0.3:
                    # print(cur_time - self._oldtime_res)
                    self.ClickArrow(butt_name,butt_dir)
            except:
                pass

        # Test if active if in the Joystick
        dic_dir = {-1:'back', 1: 'forward'}
        if axis:
            # only consider X axis of analog
            if self._controllui == 'sample':
                #special handling for jog
                pass
            
            else:
                if self._controlui_axis == 'X':
                    # check if right to inverse dir
                    if self._controllui == 'right':
                        coef = -1
                    else:
                        coef = 1

                    if 'AnalogLx' in axis:
                        butt_dir = dic_dir[np.sign(axis['AnalogLx'])*coef]
                        butt_name = self._controllui + self._controlui_axis
                        
                        cur_time = time.time()
                        if cur_time - self._oldtime_res > 0.3:
                            # print(cur_time - self._oldtime_res)
                            self.MoveJoystick(butt_name,butt_dir)

                # consider only Y axis of analog
                else:
                    if self._controllui == 'left' and self._controlui_axis == 'Y':
                        coef = -1
                    else:
                        coef = 1
                    if 'AnalogLy' in axis:
                        butt_dir = dic_dir[np.sign(axis['AnalogLy'])*coef]
                        butt_name = self._controllui + self._controlui_axis
               
                        cur_time = time.time()
                        if cur_time - self._oldtime_res > 0.3:
                            # print(cur_time - self._oldtime_res)
                            self.MoveJoystick(butt_name,butt_dir)


if __name__ == "__main__":
    myappid = 'NIST.stagecontrol.ui.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication([])
    app_icon = QtGui.QIcon()
    icon = os.getcwd() + '/ressources/IconUI.ico'
    app_icon.addFile(icon, QtCore.QSize(16, 16))
    app_icon.addFile(icon, QtCore.QSize(24, 24))
    app_icon.addFile(icon, QtCore.QSize(32, 32))
    app_icon.addFile(icon, QtCore.QSize(48, 48))
    app_icon.addFile(icon, QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    window = Stage()
    window.show()
    sys.exit(app.exec_())
