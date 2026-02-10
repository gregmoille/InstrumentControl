#!/Users/greg/miniforge3/bin/python

import threading
import time
from scipy import constants as cts
from yokogawa import Yokogawa


class TraceOSA(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self._running = False
        self.ip = kwargs.get('ip', '10.0.0.21')
        self.fig = kwargs.get('fig', None)
        self.trace = None
        self.current_settings = None
        self.settings_updated = False  # Flag to track if settings have been read
        self.current_scan_mode = "repeat"  # Track current scan mode
        self.scan_mode_updated = False  # Flag to track if scan mode has been read
        self.applying_settings = False  # Flag to pause trace acquisition during settings application
        self.got_trace = False
        self.getFirstTrace = True  # Flag to get the first trace immediately
        self.display_mode = "wavelength"  # Track display mode: "wavelength" or "frequency"
        self.osa = Yokogawa(ip=self.ip)  # Create single OSA instance

    def run(self):
        self._running = True
        try:
            self.osa.connected = True  # Connect to OSA
            print("OSA connected")
            # self.osa.scan = "repeat"  # Set initial scan mode
            # self.current_scan_mode = "repeat"  # Update internal tracking
            time.sleep(1)
            self.current_scan_mode = self.osa.scan  # Initialize current scan mode from OSA
            print(f"Initial scan mode: {self.current_scan_mode}")
            print("Getting settings")
            self.current_settings = self.osa.settings
            # Store current settings for UI updates
            print(f"Current settings: {self.current_settings}")

            while self._running:
                try:
                    # Only fetch trace if not in stop mode and not applying settings
                    
                    if (self.current_scan_mode != "stop" and not self.applying_settings) or self.getFirstTrace:
                        self.got_trace = False
                        self.trace = self.osa.trace
                        self.trace['freq'] = cts.c/self.trace.lbd
                        if self.trace is not None:
                            print("Updating trace data")
                            figdata = self.fig.data[0]
                            
                            # Update x-axis data based on display mode
                            if self.display_mode == "wavelength":
                                figdata.x = self.trace.lbd * 1e9  # Convert to nm
                            else:  # frequency mode
                                figdata.x = self.trace.freq * 1e-12  # Convert to THz
                            
                            y = self.trace.S
                            y[y<-120] = -120  # Clip values below -120 dBm
                            figdata.y = y
                            self.got_trace = True
                            self.getFirstTrace = False
                    else:
                        # In stop mode or applying settings, just wait a bit to avoid busy loop
                        self.got_trace = True
                        time.sleep(0.1)
                except Exception as e:
                    print(f"Error getting trace: {e}")
        except Exception as e:
            print(f"Error connecting to OSA: {e}")
        finally:
            # Always disconnect when stopping
            if self.osa.connected:
                self.osa.connected = False
                print("OSA disconnected")
                    
    def stop(self):
        self._running = False
