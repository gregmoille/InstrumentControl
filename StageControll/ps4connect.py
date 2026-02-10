from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QFontDatabase
from PyQt5 import uic
from PyQt5 import QtGui
import PyQt5

import sys
import os
import time
import ipdb
import numpy as np
import ctypes
from os.path import expanduser

from ThreadPs4Controller import Ps4Thread

class PS4Connect(QObject):
    changedValue = pyqtSignal(QObject)

    def __init__(self, **kwargs):
        self.ui = kwargs.get('ui',None)
        self._isConnect = False
        self._controllui = 'left'
        self._value = 0
        self._oldtime_res = time.time()
    
        # self.ui.pushButton_Connect.clicked.connect(self.ListenPS4)
        # self.ui.forward_left.clicked.connect(lambda: self.ChangeVal(1))
        # self.ui.back_left.clicked.connect(lambda: self.ChangeVal(-1))

        

        # self.buttons = {'forward_left': self.ui.forward_left,
        #                 'forward_right': self.ui.forward_right,
        #                 'back_left': self.ui.back_left,
        #                 'back_right': self.ui.back_right, }

        self.ArrowPs4 = {'DpadUp': 'forward',
                         'DpadDown': 'back',
                         'DpadRight': 'forward',
                         'DpadLeft': 'back',
                         }
        self.Ps4Axis = ['AnalogLx',
                        'AnalogLy',
                        'AnalogRx',
                        'AnalogRy',]

        self.switchFrame = {'R2': 'right',
                            'L2': 'left'}


    def ChangeVal(self, val):
        cur_time = time.time()
        if cur_time - self._oldtime_res > 0.25:
            self._value += val
            self.ui.label_test.setText(str(self._value))
            self._oldtime_res = cur_time

    def ListenPS4(self):
        if not self._isConnect:
            self._isConnect = True
            self.Thread = QThread(self)
            self.Worker = Ps4Thread()
            self.Worker.signalPs4[dict].connect(self.PrintController)
            self.Worker.moveToThread(self.Thread)
            self.Thread.started.connect(self.Worker.listen)

            # self.ui.pushButton_Connect.setText('Disconnect')
            self.Thread.start()
        else:
            self.Worker.stop()
            print('stop')
            self.Thread.quit()
            # self.ui.pushButton_Connect.setText('Connect')
            self._isConnect = False

    def ClickBut(self, but):
        but.setDown(True)
        QApplication.processEvents()
        time.sleep(0.0125)
        but.click()
        time.sleep(0.0125)
        but.setDown(False)
        QApplication.processEvents()

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
            Direction[kk]  = dirlist[np.sign(ps4Joystick[kk])]

        return Direction


    @pyqtSlot(dict)
    def PrintController(self, dic):
        self.ps4Buttons = dic['button']
        self.ps4Joystick = dic['axis']
        buttons = self.RetrieveActiveButtPs4(self.ps4Buttons)

        # Change the focus if changed
        self.SetFrame(buttons)

        # Test if active if in the Arrows
        activearrow = [xx for xx in self.ArrowPs4.keys() if xx in buttons]
        if activearrow:
            activearrow = activearrow[0]
            butt_name = self.ArrowPs4[activearrow] + '_' + self._controllui
            self.ClickBut(getattr(self.ui, butt_name))


        # Test the Joysticks
        axis = self.RetrieveActiveAxisPs4(self.ps4Joystick)
        if axis:
            k = list(axis.keys())[0]
            butt_name = axis[k] + '_' + self._controllui
            self.ClickBut(getattr(self.ui, butt_name))


    def SetFrame(self, buttons):
        def SetFrameStyle(nameframe):
            boldFont = QFont()
            boldFont.setBold(True)
            normFont = QFont()
            normFont.setBold(False)
            otherframe = [xx for xx in self.frame.keys() if xx != nameframe]
            self.frame[nameframe].setLineWidth(1)
            self.frame[nameframe].setMidLineWidth(1)
            self.framelabel[nameframe].setFont(boldFont)

            for ff in otherframe:
                self.frame[ff].setLineWidth(0)
                self.frame[ff].setMidLineWidth(0)
                self.framelabel[ff].setFont(normFont)

        if buttons:
            if buttons[0] == 'R2':
                SetFrameStyle(self.switchFrame['R2'])
                self._controllui = self.switchFrame['R2']
            if buttons[0] == 'L2':
                SetFrameStyle(self.switchFrame['L2'])
                self._controllui = self.switchFrame['L2']

