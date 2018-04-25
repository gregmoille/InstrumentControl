import sys
import time
import ipdb
import numpy as np

import os
try:
    import clr
    clr.AddReference(r'mscorlib')
    from System.Text import StringBuilder
    from System import Int32
    from System.Reflection import Assembly
except:
    pass
import ipdb

path = os.path.realpath('../')
if not path in sys.path:
    sys.path.insert(0, path)
from pyDecorators import InOut, ChangeState, Catch


class Toptica1050()

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
        super(Toptica1050, self).__init__()
        # some misc
        self._set = "param-set!"
        self._get = "param-ref"
        self._lsr = "'laser1:"
        self._exec = 'exec '


    # -- Methods -- 
    # ---------------------------------------------------------
    def Querry(self, word):
        pass

    # -- Decorators --
    # ---------------------------------------------------------
    @property
    def connected(): 
        pass

    @property
    @InOut.output(bool)
    def lbd(self):
        word = '({} {}ctl:wavelength-act)'.format(self._set, self._lsr)
        self._lbd = self.Querry(word)
        return self._lbd

    @lbd.setter
    @Catch.error
    @InOut.accepts(float)
    def lbd(self, value):
        word = '({} {}ctl:wavelength-set {:.3f})'.format(self._set, 
                                                        self._lsr,
                                                        val)
        self.Querry(word)

    
