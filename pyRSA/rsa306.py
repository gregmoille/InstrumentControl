from ctypes import *
from os import chdir
import numpy as np
import pandas as pd
from .RSA_API import *

class RSA306(object):
    def __init__(self, **kwargs):
        chdir("C:\\Tektronix\\RSA_API\\lib\\x64")
        self.rsa = cdll.LoadLibrary("C:\\Tektronix\\RSA_API\\lib\\x64\\RSA_API.dll")
        self._run = False

    def __enter__(self):
        self.searchConnect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.run = False
        self.disconnect()
        return self

    
    def err_check(self, rs):
        if ReturnStatus(rs) != ReturnStatus.noError:
            raise RSAError(ReturnStatus(rs).name)

    def searchConnect(self):
        numFound = c_int(0)
        intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
        deviceIDs = intArray()
        deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
        deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)
        apiVersion = create_string_buffer(DEVINFO_MAX_STRLEN)

        self.rsa.DEVICE_GetAPIVersion(apiVersion)
        # print('API Version {}'.format(apiVersion.value.decode()))

        self.err_check(self.rsa.DEVICE_Search(byref(numFound), deviceIDs,
                                    deviceSerial, deviceType))

        if numFound.value < 1:
            # self.rsa.DEVICE_Reset(c_int(0))
            print('No instruments found. Exiting script.')
            exit()
        elif numFound.value == 1:
            # print('One device found.')
            # print('Device type: {}'.format(deviceType.value.decode()))
            # print('Device serial number: {}'.format(deviceSerial.value.decode()))
            self.err_check(self.rsa.DEVICE_Connect(deviceIDs[0]))
        else:
            # corner case
            print('2 or more instruments found. Enumerating instruments, please wait.')
            for inst in deviceIDs:
                self.rsa.DEVICE_Connect(inst)
                self.rsa.DEVICE_GetSerialNumber(deviceSerial)
                self.rsa.DEVICE_GetNomenclature(deviceType)
                print('Device {}'.format(inst))
                print('Device Type: {}'.format(deviceType.value))
                print('Device serial number: {}'.format(deviceSerial.value))
                self.rsa.DEVICE_Disconnect()
            # note: the API can only currently access one at a time
            selection = 1024
            while (selection > numFound.value - 1) or (selection < 0):
                selection = int(raw_input('Select device between 0 and {}\n> '.format(numFound.value - 1)))
            self.err_check(self.rsa.DEVICE_Connect(deviceIDs[selection]))
        self.rsa.CONFIG_Preset()
        self.specSet = Spectrum_Settings()
        self.rsa.SPECTRUM_GetSettings(byref(self.specSet))
    
    def disconnect(self):
        self.rsa.DEVICE_Disconnect()

    def configSpectrum(self, cf=1e9, refLevel=0, span=40e6, rbw=300e3):
        self.rsa.SPECTRUM_SetEnable(c_bool(True))
        self.rsa.CONFIG_SetCenterFreq(c_double(cf))
        self.rsa.CONFIG_SetReferenceLevel(c_double(refLevel))

        # self.rsa.SPECTRUM_SetDefault()
        
        self.specSet.window = SpectrumWindows.SpectrumWindow_Hann
        self.specSet.verticalUnit = SpectrumVerticalUnits.SpectrumVerticalUnit_dBm
        self.specSet.span = span
        self.specSet.rbw = rbw
        self.rsa.SPECTRUM_SetSettings(self.specSet)
        self.rsa.SPECTRUM_GetSettings(byref(self.specSet))
        # return self.specSet

    def create_frequency_array(self):
        # Create array of frequency data for plotting the spectrum.
        freq = np.arange(self.specSet.actualStartFreq, self.specSet.actualStartFreq
                        + self.specSet.actualFreqStepSize * self.specSet.traceLength,
                        self.specSet.actualFreqStepSize)
        return freq

    @property
    def run(self):
        return self.run

    @run.setter
    def run(self, val):
        if val:
            self.rsa.DEVICE_Run()
            self._run = True
        else:
            self.rsa.DEVICE_Stop()
            self._run = False

    def getSpectrum(self):
        ready = c_bool(False)
        traceArray = c_float * self.specSet.traceLength
        traceData = traceArray()
        outTracePoints = c_int(0)
        traceSelector = SpectrumTraces.SpectrumTrace1
        self.rsa.SPECTRUM_AcquireTrace()
        # while not ready.value:
        #     self.rsa.SPECTRUM_WaitForDataReady(c_int(100), byref(ready))
        self.rsa.SPECTRUM_GetTrace(traceSelector, self.specSet.traceLength, byref(traceData),
                            byref(outTracePoints))
        trace = np.array(traceData)
        freq = self.create_frequency_array()
        return pd.DataFrame(dict(freq = freq, S = trace))


    def config_block_iq(self, cf=1e9, refLevel=0, iqBw=40e6, recordLength=10e3, sampling_rate = 0):
        recordLength = int(recordLength)
        self.rsa.CONFIG_SetCenterFreq(c_double(cf))
        self.rsa.CONFIG_SetReferenceLevel(c_double(refLevel))
    
        self.rsa.IQBLK_SetIQBandwidth(c_double(iqBw))
        self.rsa.IQBLK_SetIQRecordLength(c_int(recordLength))

        iqSampleRate = c_double(sampling_rate)
        self.rsa.IQBLK_GetIQSampleRate(byref(iqSampleRate))
        # print(iqSampleRate)
        # Create array of time data for plotting IQ vs time
        time = np.linspace(0, recordLength / iqSampleRate.value, recordLength)
        time1 = []
        step = recordLength / iqSampleRate.value / (recordLength - 1)
        for i in range(recordLength):
            time1.append(i * step)
        return time


    def config_trigger(self, trigMode='Free', trigLevel=-10, trigSource="ext"):
        if trigMode.lower() == 'free':
            self.rsa.TRIG_SetTriggerMode(c_int(0))
        else:
            self.rsa.TRIG_SetTriggerMode(c_int(1))
        self.rsa.TRIG_SetIFPowerTriggerLevel(c_double(trigLevel))
        if trigSource.lower() == 'ext':
            self.rsa.TRIG_SetTriggerSource(c_int(0))
        else:
            self.rsa.TRIG_SetTriggerSource(c_int(1))
        self.rsa.TRIG_SetTriggerPositionPercent(c_double(50))

    
    def acquire_block_iq(self, recordLength=10e3):
        recordLength = int(recordLength)
        ready = c_bool(False)
        iqArray = c_float * recordLength
        iData = iqArray()
        qData = iqArray()
        outLength = 0
        self.rsa.DEVICE_Run()
        self.rsa.IQBLK_AcquireIQData()
        while not ready.value:
            self.rsa.IQBLK_WaitForIQDataReady(c_int(100), byref(ready))
        self.rsa.IQBLK_GetIQDataDeinterleaved(byref(iData), byref(qData),
                                         byref(c_int(outLength)), c_int(recordLength))
        self.rsa.DEVICE_Stop()
    
        return np.array(iData) + 1j * np.array(qData)