# -- Import PyQt wrappers --
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QPointF
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor
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
#import pyqtgraph as pg
import scipy.io as io
import visa
from copy import copy



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
#import pyUtilities as ut
from pyPowerMeter import ThorlabsP1xx


# -- lood UI --
# -- load UI --
Ui_MainWindow, QtBaseClass = uic.loadUiType(work_dir + '/UI/RPiUI.ui')

class Pmeter(QMainWindow):
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
    

    def __init__(self,**kwargs):
        super(Pmeter, self).__init__()

        # -- setup the UI --
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # -- Define UI elements -- 
        self.address = ['']
        self.but_connect = {'in': self.ui.connect_IN, 
                            'out': self.ui.connect_OUT}
        self.list_address = {'in': self.ui.address_IN,
                            'out': self.ui.address_OUT}
        self.Pfactor = {'in': self.ui.fact_IN,
                        'out': self.ui.fact_OUT}
        self.Pdisp = {'in': self.ui.P_IN, 
                    'out': self.ui.P_OUT}
        self.Pmeter = {'in': None, 'out': None}
        self.λ = {'in': None, 'out': None}
        self._isconnected = {'in': False, 'out': False}
        self.threadread = {'in': None, 'out': None}
        self._readlopp = {'in': True, 'out': True}
        self.P = {'in': 0, 
                'out': 0}


        test = ['a', 'b', 'c']
        rm = visa.ResourceManager('@py')
        instr_add = {'P1000': '::32882::',
                    'P16-144': '::32891::'}
        try:
            dev = rm.list_resources()
            [self.list_address[kk].addItems(dev) for kk in ['in', 'out']]
        except:
            pass

        self.but_connect['in'].clicked.connect(lambda : self.Connect('in')) 
        self.but_connect['out'].clicked.connect(lambda : self.Connect('out')) 

    def Connect(self, port):
        print(port)
        if self._isconnected[port]:
            self._readlopp[port] = False
            time.sleep(0.25)
            self.Pmeter[port].close()
            self._isconnected[port] = False
            self.but_connect[port].setText('Coonnect')
        else:
            try:
                add = self.list_address[port].currentText()
                self.Pmeter[port] = ThorlabsP1xx(address = add)
                self._readlopp[port] = True
                self.ReadLoop(port, True)
                self._isconnected[port] = True
                self.Pmeter[port].lbd = float(self.λ[port])
                self.but_connect[port].setText('Disconnect')
            except:
                pass

    def ReadLoop(self,port, state):
        def Read(port):
            coef = np.array([-9, -6, -3,  1], dtype = float)
            units = ['nW', 'µW', 'mW', 'W']
            while True:
                if self._readlopp[port]:
                    break
                try: 
                    fact = float(self.Pfactor[port].text())
                except:
                    fact = 1

                data = self.Pmeter[port].read * fact
                self.P[port] = data
                ind = np.where(np.log10(data)<coef)[0][0] - 1
                Pstr = '{:.3f} {}'.format(data* 10**coef[ind], units[ind]) 
                self.Pdisp[port].setText(Pstr)

                if self._isconnected['in'] and self._isconnected['out']:
                    losses = 10*np.log10(self.P['out']/self.P["in"])
                    self.ui.losses.setText( '{:.2f} dB'.format(losses) )


        self.threadread[port] = threading.Thread(target=Read, args=(port,))
        self.threadread[port].daemon = True
        self.threadread[port].start()





if __name__ == "__main__":
    app = QApplication([])
    window = Pmeter()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    sys.exit(app.exec_())