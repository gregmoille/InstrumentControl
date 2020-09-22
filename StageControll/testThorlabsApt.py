import PyThorAPT
import numpy as np






SnX_left = 90866217
SnY_left = 90866218
SnZ_left = 90866219
SnX_right = 90868135
SnY_right = 90868136
SnZ_right = 90868137
SNX_micro = 27250214
SNZ_micro = 27500738

Xleft = PyThorAPT.APTMotor(SN=SnX_left)
Yleft = PyThorAPT.APTMotor(SN=SnY_left)
Zleft = PyThorAPT.APTMotor(SN=SnZ_left)
Xright = PyThorAPT.APTMotor(SN=SnX_right)
Yright = PyThorAPT.APTMotor(SN=SnY_right)
Zright = PyThorAPT.APTMotor(SN=SnZ_right)
Xmicro = PyThorAPT.APTMotor(SN=SNX_micro)
Zmicro = PyThorAPT.APTMotor(SN=SNZ_micro)


Xleft.InitializeHardwareDevice()
Yleft.InitializeHardwareDevice()
Zleft.InitializeHardwareDevice()
Xright.InitializeHardwareDevice()
Yright.InitializeHardwareDevice()
Zright.InitializeHardwareDevice()
Xmicro.InitializeHardwareDevice()
Zmicro.InitializeHardwareDevice()


Xleft.go_home()
Yleft.go_home()
Zleft.go_home()
Xright.go_home()
Yright.go_home()
Zright.go_home()
Xmicro.go_home()
Zmicro.go_home()


Xleft.cleanUpAPT()
Yleft.cleanUpAPT()
Zleft.cleanUpAPT()
Xright.cleanUpAPT()
Yright.cleanUpAPT()
Zright.cleanUpAPT()
Xmicro.cleanUpAPT()
Zmicro.cleanUpAPT()