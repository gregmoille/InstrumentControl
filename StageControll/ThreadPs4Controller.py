# Import PyQt wrappers
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5 import QtGui
import pygame
import os
import time
import ipdb
import pprint


class Ps4Thread(QObject):
    signalPs4 = pyqtSignal(dict)

    def __init__(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.axis_data = {}
        self.button_data = {}
        self.hat_data = {}

        self.dicemit = {'axis': None,
                        'button': None,
                        'hat_data': None, }

        self.Ps4Button = {'DpadUp': False,
                          'DpadDown': False,
                          'DpadRight': False,
                          'DpadLeft': False,
                          'Square': False,
                          'Cross': False,
                          'Circle': False,
                          'Triangle': False,
                          'L1': False,
                          'R1': False,
                          'L2': False,
                          'R2': False,
                          'Share': False,
                          'Options': False,
                          'LeftAnalog': False,
                          'RightAnalog': False,
                          'Ps': False,
                          'Touchpad': False
                          }

        self.Ps4Joystick = {'AnalogLx': 0,
                            'AnalogLy': 0,
                            'AnalogRx': 0,
                            'AnalogRy': 0}

        for i in range(self.controller.get_numbuttons()):
            self.button_data[i] = False

        self.hat_data = {}
        for i in range(self.controller.get_numhats()):
            self.hat_data[i] = (0, 0)

        self._isrunning = True
        super().__init__()

    def listen(self):
        while True:
            if self._isrunning:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis_data[event.axis] = round(event.value, 2)
                    elif event.type == pygame.JOYBUTTONDOWN:
                        self.button_data[event.button] = True
                    elif event.type == pygame.JOYBUTTONUP:
                        self.button_data[event.button] = False
                    elif event.type == pygame.JOYHATMOTION:
                        self.hat_data[event.hat] = event.value

                # ipdb.set_trace()
                arrow = self.hat_data[0]
                button = self.button_data
                axis = self.axis_data

                self.Ps4Button = {'DpadUp': arrow[1] == 1,
                                  'DpadDown': arrow[1] == -1,
                                  'DpadRight': arrow[0] == 1,
                                  'DpadLeft': arrow[0] == -1,
                                  'Square': button[0],
                                  'Cross': button[1],
                                  'Circle': button[2],
                                  'Triangle': button[3],
                                  'L1': button[4],
                                  'R1': button[5],
                                  'L2': button[6],
                                  'R2': button[7],
                                  'Share': button[8],
                                  'Options': button[9],
                                  'LeftAnalog': button[10],
                                  'RightAnalog': button[11],
                                  'Ps': button[12],
                                  'Touchpad': button[13]
                                  }

                Lx = axis.get(0, 0)
                Ly = -axis.get(1, 0)
                Rx = axis.get(2, 0)
                Ry = -axis.get(3, 0)

                self.Ps4Joystick = {'AnalogLx': Lx,
                                    'AnalogLy': Ly,
                                    'AnalogRx': Rx,
                                    'AnalogRy': Ry, }

                self.dicemit = {'axis': self.Ps4Joystick,
                                'button': self.Ps4Button, }

                self.signalPs4.emit(self.dicemit)
                time.sleep(0.05)
                # os.system('cls')
                # pprint.pprint('axis Data:')
                # # pprint.pprint(axis)
                # for kk in self.Ps4Joystick.keys():
                #     print(kk + ':' + str(self.Ps4Joystick[kk]))
                # pprint.pprint('button:')
                # for kk in self.Ps4Button.keys():
                #     print(kk + ':' + str(self.Ps4Button[kk]))
                # print(self.Ps4Button)

            else:
                break

    def stop(self):
        # ipdb.set_trace()
        self._isrunning = False
        self.dicemit = {'axis': None,
                        'button': None,
                        'hat_data': None}
        # self.signalPs4.emit(self.dicemit)
