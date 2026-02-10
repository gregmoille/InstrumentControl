import os
import sys
path = os.path.realpath(r'Y:\PythonSoftware\NewInstrumentControl')
if not path in sys.path:
    sys.path.insert(0, path)
from pyLaser import NewFocus6700
import TransmissionSetup as Tsetup
