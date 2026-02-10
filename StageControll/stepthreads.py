# Import PyQt wrappers
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5 import QtGui
import time

class StepThread(QObject):
    signal_done = pyqtSignal(dict)

    def __init__(self,**kwargs):
        self._isRunning = True
        self.position = kwargs.get('pos', 0)
        self.stage = kwargs.get('stage', None)
        self.name = kwargs.get('name', None)
        super().__init__()


    def Move(self):
        dic_emit = {'done': True,
                    'name': self.name,
                    'pos': self.position}
        cnt = 0
        while cnt <10:
            try:
                self.stage.mAbs(self.position)
                break
            except:
                print('error')
                time.sleep(0.05)
                cnt +=1
        self.signal_done.emit(dic_emit)
        self.stop()

    def stop(self):
        self._isRunning = False


class GoHomeThread(QObject):
    signal_done = pyqtSignal(dict)

    def __init__(self,**kwargs):
        self._isRunning = True
        self.stage = kwargs.get('stage', None)
        self.name = kwargs.get('name', None)
        super().__init__()


    def Home(self):
        dic_emit = {'done': True,
                    'name': self.name,
                    'pos': None}
        cnt = 0
        while cnt <10:
            try:
                self.stage.go_home()
                break
            except:
                print('error')
                time.sleep(0.05)
                cnt +=1
        try:
            pos = self.stage.getPos()
        except:
            pos = 0

        dic_emit['pos'] = pos

        self.signal_done.emit(dic_emit)
        self.stop()

    def stop(self):
        self._isRunning = False
