from ctypes import *
from os import chdir
import time
import numpy as np
import pandas as pd
from .RSA_API import *

class RSA306(object):
    def __init__(self, **kwargs):
        chdir("C:\\Tektronix\\RSA_API\\lib\\x64")
        self.rsa = cdll.LoadLibrary("C:\\Tektronix\\RSA_API\\lib\\x64\\RSA_API.dll")
        self._dll_handle = self.rsa._handle
        self._run = False
        self._preset_on_connect = bool(kwargs.get("preset_on_connect", True))
        self._restore_on_exit = bool(kwargs.get("restore_on_exit", False))
        self._preset_on_exit = bool(kwargs.get("preset_on_exit", False))
        self._signalvu_handoff_on_exit = bool(kwargs.get("signalvu_handoff_on_exit", True))
        self._signalvu_profile_cleanup = bool(kwargs.get("signalvu_profile_cleanup", True))
        self._signalvu_commit_cycle = bool(kwargs.get("signalvu_commit_cycle", True))
        self._signalvu_commit_settle_s = max(0.0, float(kwargs.get("signalvu_commit_settle_s", 0.03)))
        # Reconnect/reset can help with edge-case driver states, but should not be required.
        self._reconnect_on_exit = bool(kwargs.get("reconnect_on_exit", False))
        self._usb_reset_on_exit = bool(kwargs.get("usb_reset_on_exit", False))
        self._reset_settle_s = float(kwargs.get("reset_settle_s", 1.5))
        self._disconnect_retries = max(1, int(kwargs.get("disconnect_retries", 2)))
        self._disconnect_retry_delay_s = max(0.0, float(kwargs.get("disconnect_retry_delay_s", 0.05)))
        self._unload_dll_on_exit = bool(kwargs.get("unload_dll_on_exit", False))
        self._connected_device_id = None
        self._connected_serial = None
        self._entry_state = {}
        self.last_iq_acq_status = None

    def __enter__(self):
        self.searchConnect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.run = False
        if self._restore_on_exit:
            self.restore_entry_settings()
        elif self._preset_on_exit:
            self.rsa.CONFIG_Preset()
        if self._reconnect_on_exit:
            self.reconnect_cycle()
        else:
            self.release_to_signalvu()
        if self._unload_dll_on_exit:
            self._release_api_library()
        return False

    
    def err_check(self, rs):
        if ReturnStatus(rs) != ReturnStatus.noError:
            raise RSAError(ReturnStatus(rs).name)

    def _call_noerr(self, fn_name, *args):
        fn = getattr(self.rsa, fn_name, None)
        if fn is None:
            return False
        try:
            rs = fn(*args)
        except Exception:
            return False
        try:
            return ReturnStatus(rs) == ReturnStatus.noError
        except Exception:
            return False

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
            self._connected_device_id = int(deviceIDs[0])
            self.err_check(self.rsa.DEVICE_Connect(deviceIDs[0]))
            self._connected_serial = deviceSerial.value.decode(errors="ignore")
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
            self._connected_device_id = int(deviceIDs[selection])
            self.err_check(self.rsa.DEVICE_Connect(deviceIDs[selection]))
            serial_buf = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
            if self._call_noerr("DEVICE_GetSerialNumber", serial_buf):
                self._connected_serial = serial_buf.value.decode(errors="ignore")
        self._entry_state = self.get_state_snapshot()
        if self._preset_on_connect:
            self.rsa.CONFIG_Preset()
        self.specSet = Spectrum_Settings()
        self.rsa.SPECTRUM_GetSettings(byref(self.specSet))
    
    def disconnect(self):
        self._call_noerr("DEVICE_Stop")
        self._call_noerr("IQBLK_FinishedIQData")
        for attempt in range(self._disconnect_retries):
            if self._call_noerr("DEVICE_Disconnect"):
                break
            if attempt < (self._disconnect_retries - 1):
                time.sleep(self._disconnect_retry_delay_s)
                self._call_noerr("DEVICE_Stop")
        # Some API versions expose legacy top-level disconnect too.
        self._call_noerr("Disconnect")

    def release_to_signalvu(self):
        if self._signalvu_handoff_on_exit:
            self.handoff_to_signalvu()
        self.disconnect()

    def reconnect_cycle(self):
        # Explicitly recycle API ownership so SignalVu can pick the instrument right away.
        if self._signalvu_handoff_on_exit:
            self.handoff_to_signalvu()
        self.disconnect()
        if self._usb_reset_on_exit and self._connected_device_id is not None:
            self._call_noerr("DEVICE_Reset", c_int(int(self._connected_device_id)))
            if self._reset_settle_s > 0:
                time.sleep(self._reset_settle_s)

        if self._connected_device_id is None and not self._connected_serial:
            return

        reconnect_id = None
        numFound = c_int(0)
        intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
        deviceIDs = intArray()
        deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
        deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)
        if self._call_noerr("DEVICE_Search", byref(numFound), deviceIDs, deviceSerial, deviceType):
            if numFound.value == 1:
                reconnect_id = int(deviceIDs[0])
            elif numFound.value > 1 and self._connected_serial:
                for idx in range(numFound.value):
                    if self._call_noerr("DEVICE_Connect", deviceIDs[idx]):
                        serial_buf = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
                        match = self._call_noerr("DEVICE_GetSerialNumber", serial_buf) and (
                            serial_buf.value.decode(errors="ignore") == self._connected_serial
                        )
                        self._call_noerr("DEVICE_Disconnect")
                        if match:
                            reconnect_id = int(deviceIDs[idx])
                            break

        if reconnect_id is None and self._connected_device_id is not None:
            reconnect_id = int(self._connected_device_id)

        if reconnect_id is not None and self._call_noerr("DEVICE_Connect", c_int(reconnect_id)):
            self._connected_device_id = reconnect_id
            self.handoff_to_signalvu()
        self.disconnect()

    def _release_api_library(self):
        # Jupyter can keep the object alive after `with`; explicitly unload DLL so SignalVu can reacquire.
        if getattr(self, "rsa", None) is None:
            return
        handle = getattr(self, "_dll_handle", None)
        self.rsa = None
        if not handle:
            return
        try:
            kernel32 = WinDLL("kernel32", use_last_error=True)
            kernel32.FreeLibrary.argtypes = [c_void_p]
            kernel32.FreeLibrary.restype = c_int
            kernel32.FreeLibrary(c_void_p(handle))
        except Exception:
            pass

    def handoff_to_signalvu(self):
        # Minimal handoff: release active capture paths without forcing app configuration.
        self._call_noerr("DEVICE_Stop")
        self._call_noerr("IQBLK_FinishedIQData")
        self._call_noerr("AUDIO_Stop")
        self._call_noerr("IQSTREAM_Stop")
        self._call_noerr("IFSTREAM_SetEnable", c_bool(False))
        if self._signalvu_profile_cleanup:
            # Prevent API-side narrow/swept acquisition modes from limiting SignalVu span (e.g. ~3 MHz behavior).
            self._call_noerr("SetSweptIQMode", c_bool(False))
            self._call_noerr("CONFIG_SetNarrowFilterEnable", c_bool(False))
            if not self._call_noerr("DPX_SetEnable", c_bool(False)):
                self._call_noerr("SetDPXEnabled", c_bool(False))
            self._call_noerr("TRIG_SetTriggerMode", c_int(0))
            self._call_noerr("SPECTRUM_SetEnable", c_bool(True))
        if self._signalvu_commit_cycle:
            # Some config changes apply on a run-state cycle.
            if self._call_noerr("DEVICE_Run"):
                if self._signalvu_commit_settle_s > 0:
                    time.sleep(self._signalvu_commit_settle_s)
                self._call_noerr("DEVICE_Stop")

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
        return self._run

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


    def config_trigger(self, trigMode='Free', trigLevel=-10, trigSource="ext", trigPositionPercent=50):
        if trigMode.lower() == 'free':
            self.rsa.TRIG_SetTriggerMode(c_int(0))
            return
        else:
            self.rsa.TRIG_SetTriggerMode(c_int(1))
        self.rsa.TRIG_SetIFPowerTriggerLevel(c_double(trigLevel))
        if trigSource.lower() == 'ext':
            self.rsa.TRIG_SetTriggerSource(c_int(0))
        else:
            self.rsa.TRIG_SetTriggerSource(c_int(1))
        if trigPositionPercent is None:
            trigPositionPercent = 50
        trigPositionPercent = min(99.0, max(1.0, float(trigPositionPercent)))
        self.rsa.TRIG_SetTriggerPositionPercent(c_double(trigPositionPercent))

    
    def acquire_block_iq(self, recordLength=10e3, timeout_ms=100, max_wait_ms=10000, cleanup=False):
        recordLength = int(recordLength)
        ready = c_bool(False)
        iqArray = c_float * recordLength
        iData = iqArray()
        qData = iqArray()
        outLength = c_int(0)
        waited_ms = 0
        self.last_iq_acq_status = None

        self.err_check(self.rsa.DEVICE_Run())
        self._run = True
        try:
            self.err_check(self.rsa.IQBLK_AcquireIQData())
            while not ready.value:
                self.err_check(self.rsa.IQBLK_WaitForIQDataReady(c_int(timeout_ms), byref(ready)))
                waited_ms += int(timeout_ms)
                if waited_ms >= int(max_wait_ms):
                    raise TimeoutError("Timed out waiting for IQ block data.")

            self.err_check(
                self.rsa.IQBLK_GetIQDataDeinterleaved(
                    iData,
                    qData,
                    byref(outLength),
                    c_int(recordLength),
                )
            )
            acq_info = IQBLK_ACQINFO()
            if self._call_noerr("IQBLK_GetIQAcqInfo", byref(acq_info)):
                self.last_iq_acq_status = int(acq_info.acqStatus)
        finally:
            self._call_noerr("IQBLK_FinishedIQData")
            self.rsa.DEVICE_Stop()
            self._run = False
            if cleanup:
                self._call_noerr("CONFIG_Preset")

        valid = outLength.value if outLength.value > 0 else recordLength
        i_np = np.ctypeslib.as_array(iData)[:valid].copy()
        q_np = np.ctypeslib.as_array(qData)[:valid].copy()
        return i_np + 1j * q_np

    def get_state_snapshot(self):
        state = {}
        for key, fn, ctype, cast in (
            ("center_freq", "CONFIG_GetCenterFreq", c_double, float),
            ("ref_level", "CONFIG_GetReferenceLevel", c_double, float),
            ("iq_bw", "IQBLK_GetIQBandwidth", c_double, float),
            ("iq_record_length", "IQBLK_GetIQRecordLength", c_int, int),
            ("trig_mode", "TRIG_GetTriggerMode", c_int, int),
            ("trig_source", "TRIG_GetTriggerSource", c_int, int),
            ("trig_level", "TRIG_GetIFPowerTriggerLevel", c_double, float),
            ("trig_position_percent", "TRIG_GetTriggerPositionPercent", c_double, float),
            ("spectrum_enable", "SPECTRUM_GetEnable", c_bool, bool),
            ("rf_input_enable", "CONFIG_GetRFInputEnable", c_bool, bool),
            ("rf_preamp_enable", "CONFIG_GetRFPreampEnable", c_bool, bool),
            ("auto_atten", "CONFIG_GetAutoAttenuationEnable", c_bool, bool),
            ("narrow_filter_enable", "CONFIG_GetNarrowFilterEnable", c_bool, bool),
            ("rf_atten", "CONFIG_GetRFAttenuator", c_double, float),
        ):
            v = ctype()
            if self._call_noerr(fn, byref(v)):
                state[key] = cast(v.value)

        spec = Spectrum_Settings()
        if self._call_noerr("SPECTRUM_GetSettings", byref(spec)):
            state["spectrum_span"] = float(spec.span)
            state["spectrum_rbw"] = float(spec.rbw)
            state["spectrum_vbw"] = float(spec.vbw)
            state["spectrum_trace_length"] = int(spec.traceLength)

        return state

    def restore_entry_settings(self):
        if not self._entry_state:
            return
        s = self._entry_state
        self._call_noerr("DEVICE_Stop")
        if "center_freq" in s:
            self._call_noerr("CONFIG_SetCenterFreq", c_double(s["center_freq"]))
        if "ref_level" in s:
            self._call_noerr("CONFIG_SetReferenceLevel", c_double(s["ref_level"]))
        if "auto_atten" in s:
            self._call_noerr("CONFIG_SetAutoAttenuationEnable", c_bool(s["auto_atten"]))
        if ("rf_atten" in s) and ("auto_atten" in s and not s["auto_atten"]):
            self._call_noerr("CONFIG_SetRFAttenuator", c_double(s["rf_atten"]))
        if "rf_input_enable" in s:
            self._call_noerr("CONFIG_SetRFInputEnable", c_bool(s["rf_input_enable"]))
        if "rf_preamp_enable" in s:
            self._call_noerr("CONFIG_SetRFPreampEnable", c_bool(s["rf_preamp_enable"]))
        if "narrow_filter_enable" in s:
            self._call_noerr("CONFIG_SetNarrowFilterEnable", c_bool(s["narrow_filter_enable"]))
        if "trig_mode" in s:
            self._call_noerr("TRIG_SetTriggerMode", c_int(s["trig_mode"]))
        if "trig_source" in s:
            self._call_noerr("TRIG_SetTriggerSource", c_int(s["trig_source"]))
        if "trig_level" in s:
            self._call_noerr("TRIG_SetIFPowerTriggerLevel", c_double(s["trig_level"]))
        if "trig_position_percent" in s:
            self._call_noerr("TRIG_SetTriggerPositionPercent", c_double(s["trig_position_percent"]))
        if "spectrum_enable" in s:
            self._call_noerr("SPECTRUM_SetEnable", c_bool(s["spectrum_enable"]))
        self._entry_state = {}
