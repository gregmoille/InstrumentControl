# -*- coding: utf-8 -*-
"""
APT Motor Controller for Thorlabs
Adopted from
https://github.com/mcleung/PyAPT/blob/master/PyAPT.py
Using the dll provided by Thorlas. 
The dll need to be in the local folder (most of the time C:\Anaconda3\Dlls)
"""

from ctypes import c_long, c_buffer, c_float, windll, pointer, cdll
import os
import time

dllpath = "C:\\Anaconda3\\DLLs\\"
dll = 'APT.dll'


class APTMotor():
    def __init__(self, SN = 90866219 ,verbose =0, **kwargs):
        self.verbose = verbose
        self.SerialNum = c_long(SN)

        # Open the dll

        self.aptdll = cdll.LoadLibrary(dllpath + dll)
        self.aptdll.EnableEventDlg(True)
        self.aptdll.APTInit()
        self.blCorr = 0.000
        time.sleep(1)
        
        
    def InitializeHardwareDevice(self):
        results = self.aptdll.InitHWDevice(self.SerialNum)
        if results == 0:
            if self.verbose:
                print('Connected')
            self.Connected = True

            # blash = c_float()
            # self.aptdll.MOT_GetBLashDist(self.SerialNum, blash)
            # print(blash.value)

            self.aptdll.MOT_SetBLashDist(self.SerialNum, c_float(0.000))
        else:
            print('Cannot Connected')
        return results

    def getHardwareInformation(self):
            model = c_buffer(255)
            hardwareNotes = c_buffer(255)
            softwareVersion = c_buffer(255)
            self.aptdll.GetHWInfo(self.SerialNum, model, 255, softwareVersion, 255, hardwareNotes, 255)
            hwinfo = [model.value, softwareVersion.value, hardwareNotes.value]
            return hwinfo

    def getStageAxisInformation(self):
        minimumPosition = c_float()
        maximumPosition = c_float()
        units = c_long()
        pitch = c_float()
        self.aptdll.MOT_GetStageAxisInfo(self.SerialNum, pointer(minimumPosition), pointer(maximumPosition), pointer(units), pointer(pitch))
        stageAxisInformation = [minimumPosition.value, maximumPosition.value, units.value, pitch.value]
        return stageAxisInformation

    def setStageAxisInformation(self, minimumPosition, maximumPosition):
        minimumPosition = c_float(minimumPosition)
        maximumPosition = c_float(maximumPosition)
        units = c_long(1) #units of mm
        # Get different pitches of lead screw for moving stages for different stages.
        pitch = c_float(self.config.get_pitch())
        self.aptdll.MOT_SetStageAxisInfo(self.SerialNum, minimumPosition, maximumPosition, units, pitch)
        return True

    def getHardwareLimitSwitches(self):
        reverseLimitSwitch = c_long()
        forwardLimitSwitch = c_long()
        self.aptdll.MOT_GetHWLimSwitches(self.SerialNum, pointer(reverseLimitSwitch), pointer(forwardLimitSwitch))
        hardwareLimitSwitches = [reverseLimitSwitch.value, forwardLimitSwitch.value]
        return hardwareLimitSwitches

    def getVelocityParameters(self):
        minimumVelocity = c_float()
        acceleration = c_float()
        maximumVelocity = c_float()
        self.aptdll.MOT_GetVelParams(self.SerialNum, pointer(minimumVelocity), pointer(acceleration), pointer(maximumVelocity))
        velocityParameters = [minimumVelocity.value, acceleration.value, maximumVelocity.value]
        return velocityParameters

    def getVel(self):
        if self.verbose: print('getVel probing...')
        minVel, acc, maxVel = self.getVelocityParameters()
        if self.verbose: print('getVel maxVel')
        return maxVel


    def setVelocityParameters(self, minVel, acc, maxVel):
        minimumVelocity = c_float(minVel)
        acceleration = c_float(acc)
        maximumVelocity = c_float(maxVel)
        self.aptdll.MOT_SetVelParams(self.SerialNum, minimumVelocity, acceleration, maximumVelocity)
        return True

    def setVel(self, maxVel):
        if self.verbose: print('setVel', maxVel)
        minVel, acc, oldVel = self.getVelocityParameters()
        self.setVelocityParameters(minVel, acc, maxVel)
        return True

    def getVelocityParameterLimits(self):
        maximumAcceleration = c_float()
        maximumVelocity = c_float()
        self.aptdll.MOT_GetVelParamLimits(self.SerialNum, pointer(maximumAcceleration), pointer(maximumVelocity))
        velocityParameterLimits = [maximumAcceleration.value, maximumVelocity.value]
        return velocityParameterLimits

        '''
        Controlling the motors
        m = move
        c = controlled velocity
        b = backlash correction

        Rel = relative distance from current position.
        Abs = absolute position
        '''
    def getPos(self):
        '''
        Obtain the current absolute position of the stage
        '''
        if self.verbose: print('getPos probing...')
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')

        position = c_float()
        self.aptdll.MOT_GetPosition(self.SerialNum, pointer(position))
        if self.verbose: print('getPos ', position.value)
        return position.value

    def mRel(self, relDistance):
        '''
        Moves the motor a relative distance specified
        relDistance    float     Relative position desired
        '''
        if self.verbose: print('mRel ', relDistance, c_float(relDistance))
        if not self.Connected:
            print('Please connect first! Use initializeHardwareDevice')
            #raise Exception('Please connect first! Use initializeHardwareDevice')
        relativeDistance = c_float(relDistance)

        self.aptdll.MOT_MoveRelativeEx(self.SerialNum, relativeDistance, True)
        if self.verbose: print('mRel SUCESS')
        return True

    def mAbs(self, absPosition):
        '''
        Moves the motor to the Absolute position specified
        absPosition    float     Position desired
        '''
        if self.verbose: print('mAbs ', absPosition, c_float(absPosition))
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        absolutePosition = c_float(absPosition)
        self.aptdll.MOT_MoveAbsoluteEx(self.SerialNum, absolutePosition, True)
        if self.verbose: print('mAbs SUCESS')
        return True

    def mcRel(self, relDistance, moveVel=0.5):
        '''
        Moves the motor a relative distance specified at a controlled velocity
        relDistance    float     Relative position desired
        moveVel        float     Motor velocity, mm/sec
        '''
        if self.verbose: print('mcRel ', relDistance, c_float(relDistance), 'mVel', moveVel)
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        # Save velocities to reset after move
        maxVel = self.getVelocityParameterLimits()[1]
        # Set new desired max velocity
        self.setVel(moveVel)
        self.mRel(relDistance)
        self.setVel(maxVel)
        if self.verbose: print('mcRel SUCESS')
        return True

    def mcAbs(self, absPosition, moveVel=0.5):
        '''
        Moves the motor to the Absolute position specified at a controlled velocity
        absPosition    float     Position desired
        moveVel        float     Motor velocity, mm/sec
        '''
        if self.verbose: print('mcAbs ', absPosition, c_float(absPosition), 'mVel', moveVel)
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        # Save velocities to reset after move
        minVel, acc, maxVel = self.getVelocityParameters()
        # Set new desired max velocity
        self.setVel(moveVel)
        self.mAbs(absPosition)
        self.setVel(maxVel)
        if self.verbose: print('mcAbs SUCESS')
        return True

    def mbRel(self, relDistance):
        '''
        Moves the motor a relative distance specified
        relDistance    float     Relative position desired
        '''
        if self.verbose: print('mbRel ', relDistance, c_float(relDistance))
        if not self.Connected:
            print('Please connect first! Use initializeHardwareDevice')
            #raise Exception('Please connect first! Use initializeHardwareDevice')
        self.mRel(relDistance-self.blCorr)
        self.mRel(self.blCorr)
        if self.verbose: print('mbRel SUCESS')
        return True

    def mbAbs(self, absPosition):
        '''
        Moves the motor to the Absolute position specified
        absPosition    float     Position desired
        '''
        if self.verbose: print('mbAbs ', absPosition, c_float(absPosition))
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        if (absPosition < self.getPos()):
            if self.verbose: print('backlash mAbs', absPosition - self.blCorr)
            self.mAbs(absPosition-self.blCorr)
        self.mAbs(absPosition)
        if self.verbose: print('mbAbs SUCESS')
        return True

        
    def go_home(self):
        '''
        Move the stage to home position and reset position entry
        '''
        if self.verbose: print('Going home')
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        if self.verbose: print('go_home SUCESS')
        self.aptdll.MOT_MoveHome(self.SerialNum)    
        return True
        
        
        ''' Miscelaneous '''
    def identify(self):
        '''
        Causes the motor to blink the Active LED
        '''
        self.aptdll.MOT_Identify(self.SerialNum)
        return True

    def cleanUpAPT(self):
        '''
        Releases the APT object
        Use when exiting the program
        '''
        self.aptdll.APTCleanUp()
        if self.verbose: print('APT cleaned up')
        self.Connected = False