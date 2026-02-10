import pyvisa as visa
import numpy as np 
import scipy as sp 
import struct 


class RigolDG4162(object):
    '''
    Waveform generator class for the Rigol DG4162
    '''
    __author__ = 'Greg Moille'
    __version__ = '0.1'
    __date__ = '2023-11-01'

    def __init__(self, **kargs):
        self.ip = kargs.get('ip', None)
        self._connected = False
        self._rm = visa.ResourceManager()
        self._freq = 0
        self._phase = 0
        self._offset = 0
        self._ampl = 0
        self._channel = 1
        self._waveform = 'SIN'
        # try:
        #     self.idn = self._resource.query('*IDN?')
        #     print('\nSuccessfully connected to instrument:\n' + self.idn)
        # except:
        #     print('Unable to connect to instrument!')

    def __enter__(self):
        self.connect= True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connected = False
        return self

    @property 
    def connect(self):
        if self._connect:
            return self.idn
        else:
            return self._connected 
    
    @connect.setter
    def connect(self, value):
        if value: 
            self._resource = self._rm.open_resource(f"TCPIP0::{self.ip}::inst0::INSTR")
            try:
                self.idn = self._resource.query('*IDN?')
                print(f'Successfully connected to instrument:{self.idn}')
                self._connected = True
                _ = self.channel
            except:
                print('Unable to connect to instrument!')
        else:
            self._resource.close()
            self._connected = False
            print('Connection closed')

    @property
    def unlock(self):
        return self._resource.query(':SYST:KLOC:STATE?')
    
    @unlock.setter
    def unlock(self, value):
        if value:
            self._resource.write(':SYST:KLOC:STATE OFF')
        else:
            self._resource.write(':SYST:KLOC:STATE ON')
		

    @property
    def channel(self):
        _ = self.waveform
        return self._channel
    
    @channel.setter
    def channel(self, value):
        self._channel = value
        command_string = f':SOURCE{self._channel}'
        self._resource.write(command_string)
        _ = self.waveform
    
    @property
    def freq(self):
        _ = self.waveform
        return self._freq

    @freq.setter
    def freq(self, value):
        self._freq = value
        command_string = f':SOURCE{self._channel}:APPL:{self._waveform} {self._freq},{self._ampl},{self._offset},{self._phase}'
        self._resource.write(command_string)

    @property
    def waveform(self):
        out = self._resource.query(f":SOURCE{self._channel}:APPL?").strip().strip('"')
        self._waveform = out.split(',')[0].strip('"')
        self._freq = float(out.split(',')[1])
        self._ampl = float(out.split(',')[2])
        self._offset = float(out.split(',')[3])
        self._phase = float(out.split(',')[4])
        return self._waveform

    
    @waveform.setter
    def waveform(self, value):
        self._waveform = value
        command_string = f':SOURCE{self._channel}:APPL:{self._waveform} {self._freq},{self._ampl},{self._offset},{self._phase}'
        self._resource.query(command_string)
	
    @property
    def amplitude(self):
        _ = self.waveform
        return self._ampl
    
    @amplitude.setter
    def amplitude(self, value):
        self._ampl = value
        command_string = f':SOURCE{self._channel}:APPL:{self._waveform} {self._freq},{self._ampl},{self._offset},{self._phase}'
        self._resource.write(command_string)

    @property
    def offset(self):
        _ = self.waveform
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        command_string = f':SOURCE{self._channel}:APPL:{self._waveform} {self._freq},{self._ampl},{self._offset},{self._phase}'
        self._resource.write(command_string)

    @property
    def phase(self):
        _ = self.waveform
        return self._phase
    
    @phase.setter
    def phase(self, value):
        self._phase = value
        command_string = f':SOURCE{self._channel}:APPL:{self._waveform} {self._freq},{self._ampl},{self._offset},{self._phase}'
        self._resource.write(command_string)
        
    # Arbitrary Waveform Properties and Methods
    
    @property
    def arbitrary_waveform(self):
        """Get the current arbitrary waveform name"""
        try:
            return self._resource.query(f':SOURCE{self._channel}:FUNC:ARB?').strip().strip('"')
        except:
            return None
    
    @arbitrary_waveform.setter
    def arbitrary_waveform(self, name):
        """Set the arbitrary waveform to use"""
        try:
            self._resource.write(f':SOURCE{self._channel}:FUNC:ARB {name}')
            self._waveform = 'ARB'
        except Exception as e:
            print(f"Error selecting arbitrary waveform: {e}")
    
    @property
    def available_waveforms(self):
        """Get list of available arbitrary waveforms in volatile memory"""
        try:
            result = self._resource.query(':DATA:CAT? VOLATILE')
            return [name.strip('"') for name in result.strip().split(',') if name.strip()]
        except Exception as e:
            print(f"Error getting waveform list: {e}")
            return []
    
    @property
    def waveform_data(self):
        """Get information about the current waveform data (not the actual data)"""
        try:
            # Return info about current arbitrary waveform if in ARB mode
            if self._waveform == 'ARB':
                return f"Arbitrary waveform: {self.arbitrary_waveform}"
            else:
                return f"Standard waveform: {self._waveform}"
        except:
            return "No waveform data available"
    
    @waveform_data.setter
    def waveform_data(self, data_dict):
        """
        Upload arbitrary waveform data to the instrument.
        
        Parameters:
        -----------
        data_dict : dict
            Dictionary containing:
            - 'data': array-like, waveform points normalized between -1 and 1
            - 'name': str, optional, waveform name (default 'USER1')
            - 'volatile': bool, optional, use volatile memory (default True)
        """
        # Handle both dict and direct array input for convenience
        if isinstance(data_dict, dict):
            waveform_data = data_dict['data']
            name = data_dict.get('name', 'USER1')
            volatile = data_dict.get('volatile', True)
        else:
            # Direct array input - use defaults
            waveform_data = data_dict
            name = 'USER1'
            volatile = True
            
        try:
            # Convert to numpy array and normalize
            data = np.array(waveform_data, dtype=float)
            
            # Ensure data is normalized between -1 and 1
            if np.max(np.abs(data)) > 1.0:
                data = data / np.max(np.abs(data))
                print("Warning: Waveform data was normalized to [-1, 1] range.")
            
            # Convert to 14-bit DAC values (DG4000 series uses 14-bit DAC)
            # Range: 0 to 16383 (2^14 - 1), with 8191 as center
            dac_data = np.round((data + 1) * 8191.5).astype(np.uint16)
            dac_data = np.clip(dac_data, 0, 16383)
            
            # Prepare binary data
            binary_data = b''
            for point in dac_data:
                binary_data += struct.pack('<H', point)  # Little-endian 16-bit unsigned
            
            # Calculate data length
            data_length = len(binary_data)
            
            # Choose memory type
            memory_type = 'VOLATILE' if volatile else 'NVRAM'
            
            # Send the waveform data
            header = f':DATA:DAC {memory_type},{name},'
            length_str = f'#{len(str(data_length))}{data_length}'
            
            # Send command with binary data
            command = header + length_str
            self._resource.write_raw(command.encode() + binary_data + b'\n')
            
            # Check for errors
            error = self._resource.query(':SYST:ERR?')
            if not error.startswith('0,'):
                raise Exception(f"Upload error: {error}")
                
            print(f"Successfully uploaded waveform '{name}' with {len(data)} points.")
            
        except Exception as e:
            print(f"Error uploading arbitrary waveform: {e}")
    

    
    def delete_arbitrary_waveform(self, name, memory_type='VOLATILE'):
        """
        Delete an arbitrary waveform from memory.
        
        Parameters:
        -----------
        name : str
            Name of the waveform to delete.
        memory_type : str, optional
            Memory type. 'VOLATILE' or 'NVRAM'. Default is 'VOLATILE'.
        """
        try:
            self._resource.write(f':DATA:DEL {memory_type},{name}')
            print(f"Deleted waveform: {name}")
        except Exception as e:
            print(f"Error deleting waveform: {e}")
    

    

if __name__ == '__main__':
    # Example usage
    with RigolDG4162(ip='10.0.0.61') as w: 
        w.channel = 2
        
        # User creates their own waveform data
        t = np.linspace(0, 1, 1000)
        sine_wave = np.sin(2 * np.pi * t)
        custom_wave = np.sin(2*np.pi*t) + 0.5*np.sin(6*np.pi*t)
        
        # Upload waveform using property setter
        w.waveform_data = {'data': sine_wave, 'name': 'MySine'}
        
        # Or upload with direct array (uses default name 'USER1')
        w.waveform_data = custom_wave
        
        # Select the waveform
        w.arbitrary_waveform = 'MySine'
        
        # Check current waveform info
        print("Current waveform info:", w.waveform_data)
        print("Available waveforms:", w.available_waveforms)
        
        # Set output parameters
        w.freq = 1000  # 1 kHz
        w.amplitude = 2.0  # 2V peak-to-peak
