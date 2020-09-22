# -- Import PyQt wrappers --
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QSizePolicy
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QPointF, Qt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtGui
import PyQt5
import sip
# -- import classic package --
from functools import wraps
from datetime import datetime
import time
import sys
import numpy as np
import threading
import os
import ipdb
#import pyqtgraph as pg
import scipy.io as io
import visa
from copy import copy



work_dir = path = os.path.abspath(__file__ + '/..')
# -- import custom NIST-ucomb Package --
path = os.path.abspath(work_dir + '/UI/QDarkStyleSheet-master/qdarkstyle/')
if not path in sys.path:
    sys.path.insert(0, path)
path = os.path.abspath(work_dir + '/../')
if not path in sys.path:
    sys.path.insert(0, path)
    print(path)
#import pyUtilities as ut
from pyPowerMeter import ThorlabsP1xx


# -- lood UI --
# Ui_MainWindow, QtBaseClass = uic.loadUiType(work_dir + '/UI/RPiUI.ui')
from UI import Ui_MainWindow



class myQLabel(QLabel):
    def __init__(self, *args, **kargs):
        super(myQLabel, self).__init__(*args, **kargs)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored,
                                      QSizePolicy.Ignored))

        self.setMinSize(10)


    def setMinSize(self, minfs):

        f = self.font()
        f.setPixelSize(minfs)
        br = QtGui.QFontMetrics(f).boundingRect(self.text())

        self.setMinimumSize(br.width(), br.height())

    def resizeEvent(self, event):
        super(myQLabel, self).resizeEvent(event)

        if not self.text():
            return

        #--- fetch current parameters ----

        f = self.font()
        cr = self.contentsRect()

        #--- iterate to find the font size that fits the contentsRect ---

        dw = event.size().width() - event.oldSize().width()   # width change
        dh = event.size().height() - event.oldSize().height() # height change

        fs = max(f.pixelSize(), 1)
        while True:

            f.setPixelSize(fs)
            br =  QtGui.QFontMetrics(f).boundingRect(self.text())

            if dw >= 0 and dh >= 0: # label is expanding

                if br.height() <= cr.height() and br.width() <= cr.width():
                    fs += 1
                else:
                    f.setPixelSize(max(fs - 1, 1)) # backtrack
                    break

            else: # label is shrinking

                if br.height() > cr.height() or br.width() > cr.width():
                    fs -= 1
                else:
                    break

            if fs < 1: break

        #--- update font size ---

        self.setFont(f)

class Pmeter(QMainWindow):
    __author__ = "Gregory Moille"
    __copyright__ = "Copyright 2018, NIST"
    __credits__ = ["Gregory Moille",
                   "Xiyuan Lu",
                   "Kartik Srinivasan"]
    __license__ = "GPL"
    __version__ = "2.0.0"
    __maintainer__ = "Gregory Moille"
    __email__ = "gmoille@umd.edu"
    __status__ = "Development"


    def __init__(self,**kwargs):
        super(Pmeter, self).__init__()
        # -- setup the UI --
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.P_IN = myQLabel('In. Pwr')
        self.ui.P_IN.setObjectName("P_IN")
        self.ui.P_IN.setAlignment(Qt.AlignCenter)
        self.ui.pin_frame.addWidget(self.ui.P_IN)

        self.ui.P_OUT = myQLabel('Outp. Pwr')
        self.ui.P_OUT.setObjectName("P_OUT")
        self.ui.P_OUT.setAlignment(Qt.AlignCenter)
        self.ui.pout_frame.addWidget(self.ui.P_OUT)

        self.SetupDict()
        self.GetConnectedRessources()

        self.but_connect['in'].clicked.connect(lambda : self.Connect('in'))
        self.but_connect['out'].clicked.connect(lambda : self.Connect('out'))

    def SetupDict(self):
        # -- Define UI elements --
        self.address = ['']
        self.but_connect = {'in': self.ui.connect_IN,
                            'out': self.ui.connect_OUT}
        self.list_address = {'in': self.ui.address_IN,
                            'out': self.ui.address_OUT}
        self.connected_instr = {}
        self.Pfactor = {'in': lambda: float(self.ui.fact_IN.text()),
                        'out': lambda: float(self.ui.fact_OUT.text())}
        self.Pdisp = {'in': self.ui.P_IN,
                    'out': self.ui.P_OUT}
        self.Pmeter = {'in': None,
                       'out': None}
        self.λ = {'in': lambda: float(self.ui.wavelength_IN.currentText()),
                  'out': lambda: float(self.ui.wavelength_OUT.currentText())}
        self._isconnected = {'in': False, 'out': False}
        self.threadread = {'in': None, 'out': None}
        self._readlopp = {'in': True, 'out': True}
        self.P = {'in': 0,
                'out': 0}

    def GetConnectedRessources(self):
        try:
            rm = visa.ResourceManager()
            try:
                dev = rm.list_resources()
                # get the names of the instruments:
                names = []
                for dd in dev:
                    try:
                        instr = rm.open_resource(dd, timeout=0.5)
                        print('-'*60)
                        n = instr.query('*IDN?').strip().replace('Thorlabs,','').replace('1.3.0','').replace(',', ', ')
                        names += [n]
                        self.connected_instr[n] = dd
                    except Exception as err:
                        print(err)

                [self.list_address[kk].addItems(names) for kk in ['in', 'out']]
            except Exception as err:
                print('Listing ressources Error')
                print(err)
                pass
        except:
            try:
                dev = rm.list_resources()
                for dd in dev:
                    try:
                        instr = rm.open_resource(dd, timeout=0.5)
                        print('-'*60)
                        instr.write('*RST')
                        instr.write('*CLS')
                        n = instr.query('*IDN?').strip()
                        names += [n]
                        self.list_address['in'].addItems(n)
                        self.list_address['in'].addItems(n)
                        self.connected_instr[n] = dd
                    except Exception as err:
                        print(err)
            except Exception as err:
                print('Listing ressources @py Error')
                print(err)
                pass

    def Connect(self, port):
        print(port)
        if self._isconnected[port]:
            self.ReadLoop(port, False)
            time.sleep(0.25)
            self.Pmeter[port].connected = False
            self._isconnected[port] = False
            self.but_connect[port].setText('Connect')
        else:
            try:
                instr = self.list_address[port].currentText()
                add = self.connected_instr[instr]
                self.Pmeter[port] = ThorlabsP1xx(address = add)
                self.Pmeter[port].connected = True
                self._isconnected[port] = True

                self.SetupPmeter(port)

                time.sleep(0.25)
                self.but_connect[port].setText('Disconnect')
                self._readlopp[port] = True
                self.ReadLoop(port, True)
            except Exception as err:
                print('Connection to device error')
                print(err)
                pass

    def SetupPmeter(self, port):
        self.Pmeter[port].lbd = self.λ[port]()
        print(self.Pmeter[port].lbd)

    def ReadLoop(self, port, state):
        class PowerMonitor(QThread):
            pwr = pyqtSignal(tuple)

            def __init__(self, **kwargs):
                self.pmeter = kwargs.get('pmeter', None)
                self.port = kwargs.get('port', None)
                self._isRuning = True
                QThread.__init__(self)

            def run(self):
                while self._isRuning:
                    try:
                        p = self.pmeter.power
                        to_emit = (p, self.port)
                        self.pwr.emit(to_emit)
                    except Exception as err:
                        self.pmeter._instr.write('*RST')
                        self.pmeter._instr.write('*CLS')
                        self.pmeter.connected = False
                        time.sleep(1)
                        self.pmeter.connected = True
                        # self.pmeter._instr.write('*RST')
                        # self.pmeter._instr.write('*CLS')


            def stop(self):
                self._isRuning = False

        @pyqtSlot(tuple)
        def UpdatePower(tpl):
            # ipdb.set_trace()
            pwr = tpl[0]
            port = tpl[1]
            coef = np.array([-9, -6, -3,  1], dtype = float)
            units = ['nW', 'µW', 'mW', 'W']

            try:
                fact = self.Pfactor[port]()
            except Exception as err:
                print(err)
                fact = 1

            data = pwr * fact
            self.P[port] = data
            print(self.P[port])
            if self.P[port]<=0:
                Pstr = '-Inf'
            else:
                ind = np.where(np.log10(self.P[port])<coef)[0][0] - 1
                print(ind)
                print(self.P[port]*10**(-1*coef[ind]))
                Pstr = '{:.3f} {}'.format(self.P[port]*10**(-1*coef[ind]), units[ind])
                # Pstr = '{:.3f}'.format(data* 1e6)
            self.Pdisp[port].setText(Pstr)

            if self._isconnected['in'] and self._isconnected['out']:
                losses = 10*np.log10(self.P['out']/self.P["in"])
                self.ui.losses.setText( '{:.2f} dB'.format(losses) )

        if state:
            self.threadread[port] = PowerMonitor(pmeter = self.Pmeter[port], port = port)
            self.threadread[port].pwr[tuple].connect(UpdatePower)
            self.threadread[port].start()
        else:
            self.threadread[port].stop()




if __name__ == "__main__":
    app = QApplication([])
    window = Pmeter()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    sys.exit(app.exec_())
