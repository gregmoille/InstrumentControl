from ctypes import (
    CDLL,
    byref,
    c_bool,
    c_char,
    c_char_p,
    c_double,
    c_float,
    c_int,
    create_string_buffer,
)
import os
import time
from datetime import datetime
from pathlib import Path
import shutil

import numpy as np

from .RSA_API import (
    DEVINFO_MAX_STRLEN,
    DEVSRCH_MAX_NUM_DEVICES,
    DEVSRCH_SERIAL_MAX_STRLEN,
    DEVSRCH_TYPE_MAX_STRLEN,
    IQBLK_ACQINFO,
    RSAError,
    Spectrum_Limits,
    Spectrum_Settings,
    SpectrumTraces,
    SpectrumVerticalUnits,
    SpectrumWindows,
)


class RSA306SignalVu(object):
    """
    SignalVu-aligned RSA wrapper.

    This class intentionally follows the official API example flow:
    - DEVICE_Search/DEVICE_Connect
    - configure settings
    - DEVICE_Run + IQBLK_AcquireIQData + wait + get data
    - DEVICE_Stop + DEVICE_Disconnect

    It does not use reconnect/reset handoff tricks by default.
    """

    SIGNALVU_BASE_DIR = r"C:\Program Files\Tektronix\SignalVu-PC\RSA"
    SIGNALVU_DLL_DIR = r"C:\Program Files\Tektronix\SignalVu-PC\RSA\HALSV\DigitizerSourceFactories"
    SIGNALVU_DLL_PATH = (
        r"C:\Program Files\Tektronix\SignalVu-PC\RSA\HALSV\DigitizerSourceFactories\RSA_API.dll"
    )
    LEGACY_DLL_DIR = r"C:\Tektronix\RSA_API\lib\x64"
    LEGACY_DLL_PATH = r"C:\Tektronix\RSA_API\lib\x64\RSA_API.dll"
    DEFAULT_SPECTRUM_POINTS = None

    def __init__(self, **kwargs):
        self._device_index = int(kwargs.get("device_index", 0))
        self._device_serial = kwargs.get("device_serial", None)
        self._reset_before_connect = bool(kwargs.get("reset_before_connect", False))
        self._reset_settle_s = float(kwargs.get("reset_settle_s", 1.5))
        self._preset_on_connect = bool(kwargs.get("preset_on_connect", False))
        self._preset_on_exit = bool(kwargs.get("preset_on_exit", False))

        self._prefer_signalvu_dll = bool(kwargs.get("prefer_signalvu_dll", True))
        self._dll_path_override = kwargs.get("dll_path", None)
        self._extra_dll_dirs = list(kwargs.get("extra_dll_dirs", []))

        self._dll_path = None
        self._dll_search_handles = []
        self.rsa = None
        self.api_version = None
        self.connected_device_id = None
        self.connected_serial = None
        self.last_iq_acq_status = None
        self._run = False
        self.specSet = Spectrum_Settings()
        self._last_spectrum_request = {}
        self._spectrum_trace_buf = None
        self._spectrum_trace_capacity = 0
        self._spectrum_freq_cache = None
        self._spectrum_param_cache = None

        self._load_api()

    def __enter__(self):
        self.search_connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._run = False
        if self._preset_on_exit:
            self._call_noerr("CONFIG_Preset")
        self._call_noerr("DEVICE_Stop")
        self._call_noerr("DEVICE_Disconnect")
        self.rsa = None
        self._close_dll_search_handles()
        return False

    def _resolve_dll_path(self):
        if self._dll_path_override:
            return self._dll_path_override
        if self._prefer_signalvu_dll and os.path.exists(self.SIGNALVU_DLL_PATH):
            return self.SIGNALVU_DLL_PATH
        if os.path.exists(self.LEGACY_DLL_PATH):
            return self.LEGACY_DLL_PATH
        if os.path.exists(self.SIGNALVU_DLL_PATH):
            return self.SIGNALVU_DLL_PATH
        raise FileNotFoundError("Could not locate RSA_API.dll in SignalVu or legacy API locations.")

    def _default_dll_dirs(self, dll_path):
        dirs = []
        if os.path.normcase(dll_path) == os.path.normcase(self.SIGNALVU_DLL_PATH):
            dirs.extend([self.SIGNALVU_BASE_DIR, self.SIGNALVU_DLL_DIR])
        else:
            dirs.append(os.path.dirname(dll_path))
        dirs.extend(self._extra_dll_dirs)
        out = []
        for d in dirs:
            if d and os.path.isdir(d) and d not in out:
                out.append(d)
        return out

    def _configure_dll_search_dirs(self, dirs):
        if hasattr(os, "add_dll_directory"):
            for d in dirs:
                try:
                    self._dll_search_handles.append(os.add_dll_directory(d))
                except OSError:
                    pass
        else:
            current = os.environ.get("PATH", "")
            prefix = ";".join(dirs)
            os.environ["PATH"] = prefix + (";" + current if current else "")

    def _close_dll_search_handles(self):
        for h in self._dll_search_handles:
            try:
                h.close()
            except Exception:
                pass
        self._dll_search_handles = []

    def _load_api(self):
        self._dll_path = self._resolve_dll_path()
        self._configure_dll_search_dirs(self._default_dll_dirs(self._dll_path))
        self.rsa = CDLL(self._dll_path)

        err_fn = getattr(self.rsa, "DEVICE_GetErrorString", None)
        if err_fn is not None:
            err_fn.argtypes = [c_int]
            err_fn.restype = c_char_p

        api_version = create_string_buffer(DEVINFO_MAX_STRLEN)
        rs = self.rsa.DEVICE_GetAPIVersion(api_version)
        self._err_check(rs, "DEVICE_GetAPIVersion")
        self.api_version = api_version.value.decode(errors="ignore")

    def _status_name(self, status_code):
        fn = getattr(self.rsa, "DEVICE_GetErrorString", None)
        if fn is None:
            return "ReturnStatus {}".format(int(status_code))
        try:
            text = fn(c_int(int(status_code)))
            if isinstance(text, bytes):
                return text.decode(errors="ignore")
            if text:
                return str(text)
        except Exception:
            pass
        return "ReturnStatus {}".format(int(status_code))

    def _err_check(self, rs, context):
        code = int(rs)
        if code != 0:
            raise RSAError("{} failed: {} ({})".format(context, self._status_name(code), code))

    def _call_noerr(self, fn_name, *args):
        fn = getattr(self.rsa, fn_name, None)
        if fn is None:
            return False
        try:
            return int(fn(*args)) == 0
        except Exception:
            return False

    def search_connect(self):
        num_found = c_int(0)
        device_id_arr = c_int * DEVSRCH_MAX_NUM_DEVICES
        device_ids = device_id_arr()

        serial_arr = (c_char * DEVSRCH_SERIAL_MAX_STRLEN) * DEVSRCH_MAX_NUM_DEVICES
        type_arr = (c_char * DEVSRCH_TYPE_MAX_STRLEN) * DEVSRCH_MAX_NUM_DEVICES
        device_serials = serial_arr()
        device_types = type_arr()

        self._err_check(
            self.rsa.DEVICE_Search(byref(num_found), device_ids, device_serials, device_types),
            "DEVICE_Search",
        )

        if num_found.value < 1:
            raise RSAError("No instruments found.")

        found = []
        for i in range(num_found.value):
            serial = bytes(device_serials[i]).split(b"\x00", 1)[0].decode(errors="ignore")
            dtype = bytes(device_types[i]).split(b"\x00", 1)[0].decode(errors="ignore")
            found.append(
                {
                    "index": i,
                    "device_id": int(device_ids[i]),
                    "serial": serial,
                    "type": dtype,
                }
            )

        target = None
        if self._device_serial:
            for info in found:
                if info["serial"] == self._device_serial:
                    target = info
                    break
            if target is None:
                raise RSAError(
                    "Requested serial '{}' not found. Available: {}".format(
                        self._device_serial, [f["serial"] for f in found]
                    )
                )
        else:
            if not (0 <= self._device_index < len(found)):
                raise RSAError(
                    "device_index {} out of range. Found {} device(s).".format(
                        self._device_index, len(found)
                    )
                )
            target = found[self._device_index]

        if self._reset_before_connect:
            self._err_check(self.rsa.DEVICE_Reset(c_int(target["device_id"])), "DEVICE_Reset")
            if self._reset_settle_s > 0:
                time.sleep(self._reset_settle_s)

        self._err_check(self.rsa.DEVICE_Connect(c_int(target["device_id"])), "DEVICE_Connect")
        self.connected_device_id = int(target["device_id"])

        sn = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
        if self._call_noerr("DEVICE_GetSerialNumber", sn):
            self.connected_serial = sn.value.decode(errors="ignore")
        else:
            self.connected_serial = target["serial"]

        if self._preset_on_connect:
            self._err_check(self.rsa.CONFIG_Preset(), "CONFIG_Preset")

        self._call_noerr("SPECTRUM_GetSettings", byref(self.specSet))
        return found

    def config_block_iq(self, cf=1e9, refLevel=0, iqBw=40e6, recordLength=10e3, sampling_rate=0):
        recordLength = int(recordLength)
        self._err_check(self.rsa.CONFIG_SetCenterFreq(c_double(cf)), "CONFIG_SetCenterFreq")
        self._err_check(
            self.rsa.CONFIG_SetReferenceLevel(c_double(refLevel)), "CONFIG_SetReferenceLevel"
        )
        self._err_check(self.rsa.IQBLK_SetIQBandwidth(c_double(iqBw)), "IQBLK_SetIQBandwidth")
        self._err_check(
            self.rsa.IQBLK_SetIQRecordLength(c_int(recordLength)), "IQBLK_SetIQRecordLength"
        )

        iq_sample_rate = c_double(sampling_rate)
        self._err_check(self.rsa.IQBLK_GetIQSampleRate(byref(iq_sample_rate)), "IQBLK_GetIQSampleRate")
        return np.linspace(0, recordLength / iq_sample_rate.value, recordLength)

    def config_trigger(self, trigMode="Free", trigLevel=-10, trigSource="ext", trigPositionPercent=50):
        if trigMode.lower() == "free":
            self._err_check(self.rsa.TRIG_SetTriggerMode(c_int(0)), "TRIG_SetTriggerMode")
            return

        self._err_check(self.rsa.TRIG_SetTriggerMode(c_int(1)), "TRIG_SetTriggerMode")
        self._err_check(
            self.rsa.TRIG_SetIFPowerTriggerLevel(c_double(trigLevel)),
            "TRIG_SetIFPowerTriggerLevel",
        )
        src = 0 if trigSource.lower() == "ext" else 1
        self._err_check(self.rsa.TRIG_SetTriggerSource(c_int(src)), "TRIG_SetTriggerSource")

        if trigPositionPercent is None:
            trigPositionPercent = 50
        trigPositionPercent = min(99.0, max(1.0, float(trigPositionPercent)))
        self._err_check(
            self.rsa.TRIG_SetTriggerPositionPercent(c_double(trigPositionPercent)),
            "TRIG_SetTriggerPositionPercent",
        )

    def _resolve_spectrum_window(self, window):
        if isinstance(window, int):
            return c_int(window)
        if isinstance(window, c_int):
            return window
        key = str(window).strip().lower()
        mapping = {
            "kaiser": SpectrumWindows.SpectrumWindow_Kaiser,
            "mil6db": SpectrumWindows.SpectrumWindow_Mil6dB,
            "blackmanharris": SpectrumWindows.SpectrumWindow_BlackmanHarris,
            "rectangle": SpectrumWindows.SpectrumWindow_Rectangle,
            "rect": SpectrumWindows.SpectrumWindow_Rectangle,
            "flattop": SpectrumWindows.SpectrumWindow_FlatTop,
            "hann": SpectrumWindows.SpectrumWindow_Hann,
        }
        if key not in mapping:
            raise ValueError("Unsupported spectrum window '{}'".format(window))
        return mapping[key]

    def _resolve_spectrum_vertical_unit(self, vertical_unit):
        if isinstance(vertical_unit, int):
            return c_int(vertical_unit)
        if isinstance(vertical_unit, c_int):
            return vertical_unit
        key = str(vertical_unit).strip().lower()
        mapping = {
            "dbm": SpectrumVerticalUnits.SpectrumVerticalUnit_dBm,
            "watt": SpectrumVerticalUnits.SpectrumVerticalUnit_Watt,
            "volt": SpectrumVerticalUnits.SpectrumVerticalUnit_Volt,
            "amp": SpectrumVerticalUnits.SpectrumVerticalUnit_Amp,
            "dbmv": SpectrumVerticalUnits.SpectrumVerticalUnit_dBmV,
        }
        if key not in mapping:
            raise ValueError("Unsupported spectrum vertical unit '{}'".format(vertical_unit))
        return mapping[key]

    def _resolve_trace_selector(self, trace):
        if isinstance(trace, c_int):
            return trace
        try:
            t = int(trace)
        except Exception as exc:
            raise ValueError("Trace selector must be 1, 2, 3, 0, 1, 2, or c_int.") from exc

        if t in (1, 2, 3):
            return {
                1: SpectrumTraces.SpectrumTrace1,
                2: SpectrumTraces.SpectrumTrace2,
                3: SpectrumTraces.SpectrumTrace3,
            }[t]
        if t in (0, 1, 2):
            return {
                0: SpectrumTraces.SpectrumTrace1,
                1: SpectrumTraces.SpectrumTrace2,
                2: SpectrumTraces.SpectrumTrace3,
            }[t]
        raise ValueError("Trace selector must be 1, 2, 3, 0, 1, 2, or c_int.")

    def _set_center_freq_with_recovery(self, cf_hz, recover_on_param_error=True):
        rs = self.rsa.CONFIG_SetCenterFreq(c_double(cf_hz))
        code = int(rs)
        if code == 302 and recover_on_param_error:
            # Recover once from incompatible/stale analyzer state.
            self._call_noerr("CONFIG_Preset")
            rs = self.rsa.CONFIG_SetCenterFreq(c_double(cf_hz))
            code = int(rs)
        self._err_check(rs, "CONFIG_SetCenterFreq")

    def _coerce_trace_length(self, trace_length):
        if trace_length is None:
            return None
        n = int(trace_length)
        if n < 1:
            raise ValueError("trace_length/points must be >= 1.")

        limits = Spectrum_Limits()
        if self._call_noerr("SPECTRUM_GetLimits", byref(limits)):
            min_n = int(limits.minTraceLength)
            max_n = int(limits.maxTraceLength)
            if not (min_n <= n <= max_n):
                raise ValueError(
                    "Requested points {} outside API limits [{}, {}].".format(n, min_n, max_n)
                )
        return n

    def _ensure_spectrum_buffers(self, trace_len):
        trace_len = int(trace_len)
        if trace_len < 1:
            raise ValueError("trace_len must be >= 1.")
        if self._spectrum_trace_capacity != trace_len or self._spectrum_trace_buf is None:
            trace_array = c_float * trace_len
            self._spectrum_trace_buf = trace_array()
            self._spectrum_trace_capacity = trace_len
            self._spectrum_freq_cache = self.specSet.actualStartFreq + np.arange(
                trace_len
            ) * self.specSet.actualFreqStepSize

    def config_spectrum(
        self,
        cf=1e9,
        refLevel=0,
        span=40e6,
        rbw=300e3,
        trace_length=None,
        points=DEFAULT_SPECTRUM_POINTS,
        window="hann",
        vertical_unit="dbm",
        enable_vbw=False,
        vbw=300e3,
        force_wide_mode=True,
        recover_on_param_error=True,
        enforce_trace_length=False,
        start_device=True,
    ):
        if points is not None and trace_length is not None and int(points) != int(trace_length):
            raise ValueError("Use either points or trace_length, or provide the same value to both.")

        cf = float(cf)
        refLevel = float(refLevel)
        span = float(span)
        rbw = float(rbw)
        vbw = float(vbw)
        requested_trace_length = points if points is not None else trace_length
        requested_trace_length = self._coerce_trace_length(requested_trace_length)

        if force_wide_mode:
            self._call_noerr("DEVICE_Stop")
            self._call_noerr("IQBLK_FinishedIQData")
            self._call_noerr("CONFIG_SetNarrowFilterEnable", c_bool(False))
            self._call_noerr("TRIG_SetTriggerMode", c_int(0))

        self._err_check(self.rsa.SPECTRUM_SetEnable(c_bool(True)), "SPECTRUM_SetEnable")
        self._set_center_freq_with_recovery(
            cf_hz=cf, recover_on_param_error=bool(recover_on_param_error)
        )
        self._err_check(
            self.rsa.CONFIG_SetReferenceLevel(c_double(refLevel)), "CONFIG_SetReferenceLevel"
        )

        spec = Spectrum_Settings()
        self._err_check(self.rsa.SPECTRUM_GetSettings(byref(spec)), "SPECTRUM_GetSettings")
        spec.span = span
        spec.rbw = rbw
        spec.enableVBW = c_bool(bool(enable_vbw)).value
        if bool(enable_vbw):
            spec.vbw = vbw
        if requested_trace_length is not None:
            spec.traceLength = requested_trace_length
        spec.window = self._resolve_spectrum_window(window).value
        spec.verticalUnit = self._resolve_spectrum_vertical_unit(vertical_unit).value

        self._err_check(self.rsa.SPECTRUM_SetSettings(spec), "SPECTRUM_SetSettings")
        self._err_check(self.rsa.SPECTRUM_GetSettings(byref(spec)), "SPECTRUM_GetSettings")
        self.specSet = spec
        if (
            requested_trace_length is not None
            and bool(enforce_trace_length)
            and int(self.specSet.traceLength) != int(requested_trace_length)
        ):
            raise RSAError(
                "Trace length request {} not accepted by API (actual {}).".format(
                    int(requested_trace_length), int(self.specSet.traceLength)
                )
            )
        self._ensure_spectrum_buffers(self.specSet.traceLength)
        self._last_spectrum_request = {
            "cf_hz": cf,
            "ref_level_dbm": refLevel,
            "span_hz": span,
            "rbw_hz": rbw,
            "vbw_enabled": bool(enable_vbw),
            "vbw_hz": vbw,
            "requested_trace_length": requested_trace_length,
            "requested_points": requested_trace_length,
            "window": str(window),
            "vertical_unit": str(vertical_unit),
            "force_wide_mode": bool(force_wide_mode),
            "enforce_trace_length": bool(enforce_trace_length),
        }
        self._spectrum_param_cache = None
        if bool(start_device) and not self._run:
            self._err_check(self.rsa.DEVICE_Run(), "DEVICE_Run")
            self._run = True
        return self.specSet

    def get_spectrum(
        self,
        trace=1,
        timeout_ms=20,
        max_wait_ms=2000,
        start_device=False,
        stop_device=False,
        wait_for_data=False,
        return_dict=False,
        refresh_settings=False,
    ):
        try:
            import pandas as pd
        except Exception as exc:
            raise ImportError("pandas is required for get_spectrum().") from exc

        self._err_check(self.rsa.SPECTRUM_SetEnable(c_bool(True)), "SPECTRUM_SetEnable")
        if bool(refresh_settings) or self._spectrum_trace_capacity < 1:
            self._err_check(
                self.rsa.SPECTRUM_GetSettings(byref(self.specSet)), "SPECTRUM_GetSettings"
            )
        self._ensure_spectrum_buffers(self.specSet.traceLength)
        trace_selector = self._resolve_trace_selector(trace)

        out_points = c_int(0)

        if bool(start_device) and not self._run:
            self._err_check(self.rsa.DEVICE_Run(), "DEVICE_Run")
            self._run = True

        try:
            self._err_check(self.rsa.SPECTRUM_AcquireTrace(), "SPECTRUM_AcquireTrace")
            wait_fn = getattr(self.rsa, "SPECTRUM_WaitForDataReady", None)
            if wait_for_data and wait_fn is not None:
                ready = c_bool(False)
                waited_ms = 0
                while not ready.value:
                    rs = wait_fn(c_int(timeout_ms), byref(ready))
                    code = int(rs)
                    if code not in (0, 304):
                        self._err_check(rs, "SPECTRUM_WaitForDataReady")
                    waited_ms += int(timeout_ms)
                    if waited_ms >= int(max_wait_ms):
                        raise TimeoutError("Timed out waiting for spectrum trace.")

            self._err_check(
                self.rsa.SPECTRUM_GetTrace(
                    trace_selector,
                    c_int(self._spectrum_trace_capacity),
                    byref(self._spectrum_trace_buf),
                    byref(out_points),
                ),
                "SPECTRUM_GetTrace",
            )
        finally:
            if bool(stop_device):
                self._call_noerr("DEVICE_Stop")
                self._run = False

        valid = out_points.value if out_points.value > 0 else self._spectrum_trace_capacity
        freq_np = self._spectrum_freq_cache[:valid].copy()
        trace_np = np.ctypeslib.as_array(self._spectrum_trace_buf)[:valid].copy()

        if bool(return_dict):
            return {"freq_hz": freq_np, "trace": trace_np}

        df = pd.DataFrame({"freq": freq_np, "S": trace_np})
        if self._spectrum_param_cache is None:
            self._spectrum_param_cache = self.get_spectrum_params()
        param = dict(self._spectrum_param_cache)
        param["trace"] = int(trace)
        param["points"] = int(len(df))
        return df, param

    def get_spectrum_params(self, trace=None, points=None):
        self._call_noerr("SPECTRUM_GetSettings", byref(self.specSet))
        params = {
            "api_version": self.api_version,
            "dll_path": self._dll_path,
            "span_hz": float(self.specSet.span),
            "rbw_hz": float(self.specSet.rbw),
            "vbw_enabled": bool(self.specSet.enableVBW),
            "vbw_hz": float(self.specSet.vbw),
            "trace_length": int(self.specSet.traceLength),
            "window": int(self.specSet.window),
            "vertical_unit": int(self.specSet.verticalUnit),
            "actual_start_freq_hz": float(self.specSet.actualStartFreq),
            "actual_stop_freq_hz": float(self.specSet.actualStopFreq),
            "actual_freq_step_hz": float(self.specSet.actualFreqStepSize),
            "actual_rbw_hz": float(self.specSet.actualRBW),
            "actual_vbw_hz": float(self.specSet.actualVBW),
            "actual_num_iq_samples": float(self.specSet.actualNumIQSamples),
        }
        params.update(self._last_spectrum_request)
        center_freq = self._query_double("CONFIG_GetCenterFreq")
        ref_level = self._query_double("CONFIG_GetReferenceLevel")
        if center_freq is not None:
            params["center_freq_hz"] = center_freq
        if ref_level is not None:
            params["ref_level_dbm"] = ref_level
        if trace is not None:
            try:
                params["trace"] = int(trace)
            except Exception:
                pass
        if points is not None:
            params["points"] = int(points)
        return params

    def get_spectrum_df_param(
        self,
        trace=1,
        timeout_ms=20,
        max_wait_ms=2000,
        start_device=False,
        stop_device=False,
        wait_for_data=False,
        refresh_settings=False,
    ):
        return self.get_spectrum(
            trace=trace,
            timeout_ms=timeout_ms,
            max_wait_ms=max_wait_ms,
            start_device=start_device,
            stop_device=stop_device,
            wait_for_data=wait_for_data,
            return_dict=False,
            refresh_settings=refresh_settings,
        )

    def acquire_spectrum_df_param(
        self,
        cf=1e9,
        refLevel=0,
        span=40e6,
        rbw=300e3,
        trace_length=None,
        points=DEFAULT_SPECTRUM_POINTS,
        window="hann",
        vertical_unit="dbm",
        enable_vbw=False,
        vbw=300e3,
        force_wide_mode=True,
        recover_on_param_error=True,
        enforce_trace_length=False,
        trace=1,
        timeout_ms=100,
        max_wait_ms=10000,
        start_device=True,
        stop_device=True,
        wait_for_data=False,
    ):
        self.config_spectrum(
            cf=cf,
            refLevel=refLevel,
            span=span,
            rbw=rbw,
            trace_length=trace_length,
            points=points,
            window=window,
            vertical_unit=vertical_unit,
            enable_vbw=enable_vbw,
            vbw=vbw,
            force_wide_mode=force_wide_mode,
            recover_on_param_error=recover_on_param_error,
            enforce_trace_length=enforce_trace_length,
        )
        df, param = self.get_spectrum_df_param(
            trace=trace,
            timeout_ms=timeout_ms,
            max_wait_ms=max_wait_ms,
            start_device=start_device,
            stop_device=stop_device,
            wait_for_data=wait_for_data,
        )
        req_points = points if points is not None else trace_length
        if req_points is not None:
            param["requested_trace_length"] = int(req_points)
            param["requested_points"] = int(req_points)
        return df, param

    def acquire_block_iq(self, recordLength=10e3, timeout_ms=100, max_wait_ms=10000, cleanup=False):
        recordLength = int(recordLength)
        ready = c_bool(False)
        iq_array = c_float * recordLength
        i_data = iq_array()
        q_data = iq_array()
        out_length = c_int(0)
        waited_ms = 0
        self.last_iq_acq_status = None

        self._err_check(self.rsa.DEVICE_Run(), "DEVICE_Run")
        self._run = True
        try:
            self._err_check(self.rsa.IQBLK_AcquireIQData(), "IQBLK_AcquireIQData")
            while not ready.value:
                self._err_check(
                    self.rsa.IQBLK_WaitForIQDataReady(c_int(timeout_ms), byref(ready)),
                    "IQBLK_WaitForIQDataReady",
                )
                waited_ms += int(timeout_ms)
                if waited_ms >= int(max_wait_ms):
                    raise TimeoutError("Timed out waiting for IQ block data.")

            self._err_check(
                self.rsa.IQBLK_GetIQDataDeinterleaved(
                    i_data,
                    q_data,
                    byref(out_length),
                    c_int(recordLength),
                ),
                "IQBLK_GetIQDataDeinterleaved",
            )

            acq_info = IQBLK_ACQINFO()
            if self._call_noerr("IQBLK_GetIQAcqInfo", byref(acq_info)):
                self.last_iq_acq_status = int(acq_info.acqStatus)
        finally:
            self._call_noerr("DEVICE_Stop")
            self._run = False
            if cleanup:
                self._call_noerr("CONFIG_Preset")

        valid = out_length.value if out_length.value > 0 else recordLength
        i_np = np.ctypeslib.as_array(i_data)[:valid].copy()
        q_np = np.ctypeslib.as_array(q_data)[:valid].copy()
        return i_np + 1j * q_np

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, val):
        if val:
            self._err_check(self.rsa.DEVICE_Run(), "DEVICE_Run")
            self._run = True
        else:
            self._call_noerr("DEVICE_Stop")
            self._run = False

    def _query_double(self, fn_name):
        v = c_double()
        if self._call_noerr(fn_name, byref(v)):
            return float(v.value)
        return None

    def _query_int(self, fn_name):
        v = c_int()
        if self._call_noerr(fn_name, byref(v)):
            return int(v.value)
        return None

    def get_state_snapshot(self):
        return {
            "api_version": self.api_version,
            "dll_path": self._dll_path,
            "center_freq": self._query_double("CONFIG_GetCenterFreq"),
            "ref_level": self._query_double("CONFIG_GetReferenceLevel"),
            "iq_bw": self._query_double("IQBLK_GetIQBandwidth"),
            "iq_record_length": self._query_int("IQBLK_GetIQRecordLength"),
            "trig_mode": self._query_int("TRIG_GetTriggerMode"),
            "trig_source": self._query_int("TRIG_GetTriggerSource"),
        }

    @staticmethod
    def signalvu_state_files():
        base = Path(r"C:\ProgramData\Tektronix\RSA\SignalVu-PC")
        return [base / "persist.xml", base / "_tempSave.xml"]

    @staticmethod
    def backup_and_reset_signalvu_state(backup_root=None):
        files = RSA306SignalVu.signalvu_state_files()
        if backup_root is None:
            backup_root = Path(r"C:\ProgramData\Tektronix\RSA\SignalVu-PC\backup")
        else:
            backup_root = Path(backup_root)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = backup_root / ts
        target.mkdir(parents=True, exist_ok=True)

        result = {"backup_dir": str(target), "files": []}
        for f in files:
            entry = {"path": str(f), "exists": f.exists()}
            if f.exists():
                backup_file = target / f.name
                shutil.copy2(f, backup_file)
                try:
                    f.unlink()
                    entry["reset"] = True
                except OSError:
                    entry["reset"] = False
                entry["backup"] = str(backup_file)
            result["files"].append(entry)
        return result


# Alias name for clarity in notebooks/scripts.
RSA306Official = RSA306SignalVu
