#!/usr/bin/env python3
"""
Rigol DG4162 Arbitrary Waveform Generator
Converted from MATLAB sendTo33522A.m for Agilent 33522A

This script generates complex ramp waveforms for frequency sweeping applications
and uploads them to a Rigol DG4162 arbitrary waveform generator.

Original MATLAB code by: Mark Harrington
Python conversion by: Greg Moille
Date: October 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from RigolDG4000 import RigolDG4162


def ramp_gen_v(ramp_speeds, ramp_voltages, sample_rate=250e6):
    """
    Generate voltage ramp waveform based on frequency sweep speeds.
    
    This function recreates the functionality of the MATLAB RampGenV function.
    
    Parameters:
    -----------
    ramp_speeds : array-like
        Frequency sweep speeds in GHz/us for each ramp segment
    ramp_voltages : array-like  
        AWG voltages at start of each ramp segment
    sample_rate : float, optional
        Sample rate in Hz. Default is 250 MHz.
        
    Returns:
    --------
    numpy.ndarray
        Generated voltage waveform data
    """
    ramp_speeds = np.array(ramp_speeds)
    ramp_voltages = np.array(ramp_voltages)
    
    # Estimate time duration for each segment based on voltage change and speed
    # This is an approximation - you may need to adjust based on your specific requirements
    time_segments = []
    voltage_segments = []
    
    for i in range(len(ramp_speeds)):
        if i < len(ramp_voltages) - 1:
            voltage_start = ramp_voltages[i]
            voltage_end = ramp_voltages[i + 1]
            voltage_change = abs(voltage_end - voltage_start)
            
            # Estimate segment duration (you may need to adjust this formula)
            if abs(ramp_speeds[i]) > 1e-6:  # Avoid division by zero
                segment_duration = voltage_change / (abs(ramp_speeds[i]) * 1e-3)  # Convert to seconds
            else:
                segment_duration = 1e-3  # Default 1ms for very slow ramps
                
            # Ensure minimum segment duration
            segment_duration = max(segment_duration, 1e-6)  # At least 1 microsecond
            
            # Generate time points for this segment
            n_points = int(segment_duration * sample_rate)
            n_points = max(n_points, 10)  # Minimum 10 points per segment
            
            t_segment = np.linspace(0, segment_duration, n_points)
            
            # Generate voltage ramp for this segment
            if ramp_speeds[i] >= 0:
                v_segment = np.linspace(voltage_start, voltage_end, n_points)
            else:
                v_segment = np.linspace(voltage_end, voltage_start, n_points)
                
            time_segments.append(t_segment)
            voltage_segments.append(v_segment)
    
    # Concatenate all segments
    if voltage_segments:
        data = np.concatenate(voltage_segments)
    else:
        # Fallback: create a simple waveform
        t = np.linspace(0, 1e-3, int(1e-3 * sample_rate))
        data = np.interp(t, np.linspace(0, 1e-3, len(ramp_voltages)), ramp_voltages)
    
    return data


def configure_rigol_advanced(rigol, frequency=None, phase=None, unlock_front_panel=True):
    """
    Configure advanced Rigol settings using all available properties.
    
    Parameters:
    -----------
    rigol : RigolDG4162
        Connected Rigol instance
    frequency : float, optional
        Override frequency setting
    phase : float, optional  
        Override phase setting
    unlock_front_panel : bool, optional
        Whether to unlock front panel. Default True.
    """
    # Unlock front panel for manual control if desired
    if unlock_front_panel:
        rigol.unlock = True
        print(f"Front panel unlocked: {rigol.unlock}")
    
    # Set frequency if provided
    if frequency is not None:
        rigol.freq = frequency
        print(f"Set frequency: {rigol.freq} Hz")
    
    # Set phase if provided
    if phase is not None:
        rigol.phase = phase
        print(f"Set phase: {rigol.phase} degrees")
    
    # Display all current settings
    print("\nCurrent Rigol Settings:")
    print(f"  Channel: {rigol.channel}")
    print(f"  Waveform: {rigol.waveform}")
    print(f"  Frequency: {rigol.freq} Hz")
    print(f"  Amplitude: {rigol.amplitude} V")
    print(f"  Offset: {rigol.offset} V")
    print(f"  Phase: {rigol.phase} degrees")
    print(f"  Front panel unlocked: {rigol.unlock}")
    if rigol.waveform == 'ARB':
        print(f"  Arbitrary waveform: {rigol.arbitrary_waveform}")
        print(f"  Available waveforms: {rigol.available_waveforms}")


def upload_ramp_to_rigol(rigol_ip, ramp_speeds, ramp_voltages, 
                        invert=True, sample_rate=250e6, 
                        waveform_name='RampWave', channel=1,
                        frequency_override=None, phase_override=0):
    """
    Generate and upload ramp waveform to Rigol DG4162.
    
    Parameters:
    -----------
    rigol_ip : str
        IP address of the Rigol DG4162
    ramp_speeds : array-like
        Frequency sweep speeds in GHz/us for each ramp
    ramp_voltages : array-like
        AWG voltages at start of each ramp
    invert : bool, optional
        Whether to invert the signal. Default is True.
    sample_rate : float, optional
        Sample rate in Hz. Default is 250 MHz.
    waveform_name : str, optional
        Name for the uploaded waveform. Default is 'RampWave'.
    channel : int, optional
        Channel number (1 or 2). Default is 1.
    frequency_override : float, optional
        Override the calculated frequency with a specific value.
    phase_override : float, optional
        Set a specific phase in degrees. Default is 0.
    """
    
    # Convert to numpy arrays
    ramp_speeds = np.array(ramp_speeds)
    ramp_voltages = np.array(ramp_voltages)
    
    # Apply inversion if requested
    if invert:
        ramp_voltages = np.max(ramp_voltages) - ramp_voltages
        ramp_speeds = -ramp_speeds
        
    print(f"Ramp speeds: {ramp_speeds}")
    print(f"Ramp voltages: {ramp_voltages}")
    
    # Generate the waveform data
    print("Generating waveform data...")
    data = ramp_gen_v(ramp_speeds, ramp_voltages, sample_rate)
    
    print(f"Generated {len(data)} data points")
    print(f"Data range: {np.min(data):.4f} to {np.max(data):.4f} V")
    
    # Get min/max values
    data_min = np.min(data)
    data_max = np.max(data)
    
    # Normalize data to [-1, 1] range for the Rigol class
    data_range = max(abs(data_max), abs(data_min))
    if data_range > 0:
        data_normalized = data / data_range
    else:
        data_normalized = data
        
    print(f"Normalized data range: {np.min(data_normalized):.4f} to {np.max(data_normalized):.4f}")
    
    # Connect to Rigol and upload waveform
    try:
        with RigolDG4162(ip=rigol_ip) as rigol:
            print(f"Connected to: {rigol.idn}")
            
            # Set channel using property
            rigol.channel = channel
            print(f"Selected channel: {rigol.channel}")
            
            # Check current waveform info using properties
            print(f"Current waveform: {rigol.waveform}")
            print(f"Current waveform data info: {rigol.waveform_data}")
            
            # Unlock front panel for manual control using property
            rigol.unlock = True
            print(f"Front panel unlocked: {rigol.unlock}")
            
            # Clear any existing waveforms (optional)
            try:
                rigol.delete_arbitrary_waveform(waveform_name)
                print(f"Cleared existing waveform: {waveform_name}")
            except:
                pass  # Ignore if waveform doesn't exist
            
            # Upload the waveform using property setter
            print(f"Uploading waveform data ({len(data_normalized)} points)...")
            rigol.waveform_data = {
                'data': data_normalized,
                'name': waveform_name,
                'volatile': True
            }
            
            # Check available waveforms using property
            print(f"Available waveforms: {rigol.available_waveforms}")
            
            # Select the uploaded waveform using property
            rigol.arbitrary_waveform = waveform_name
            print(f"Selected arbitrary waveform: {rigol.arbitrary_waveform}")
            
            # Set the voltage range using properties
            # Calculate amplitude and offset
            amplitude = data_max - data_min  # Peak-to-peak amplitude
            offset = (data_max + data_min) / 2  # DC offset
            
            # Set amplitude using property
            rigol.amplitude = amplitude
            print(f"Set amplitude: {rigol.amplitude:.4f} V (peak-to-peak)")
            
            # Set offset using property  
            rigol.offset = offset
            print(f"Set offset: {rigol.offset:.4f} V")
            
            # Set frequency using property (with override option)
            if frequency_override is not None:
                rigol.freq = frequency_override
                print(f"Set frequency (override): {rigol.freq:.2f} Hz")
            else:
                # Default frequency based on waveform duration
                rigol.freq = sample_rate / len(data_normalized)
                print(f"Set frequency (calculated): {rigol.freq:.2f} Hz")
            
            # Set phase using property (with override option)
            rigol.phase = phase_override
            print(f"Set phase: {rigol.phase} degrees")
            
            # Check final waveform status
            print(f"Final waveform: {rigol.waveform}")
            print(f"Final waveform data info: {rigol.waveform_data}")
            
            print(f"\n✓ Waveform '{waveform_name}' configured successfully!")
            print(f"Final Configuration (using all RigolDG4162 properties):")
            print(f"  Channel: {rigol.channel}")
            print(f"  Waveform type: {rigol.waveform}")
            print(f"  Arbitrary waveform: {rigol.arbitrary_waveform}")
            print(f"  Amplitude: {rigol.amplitude:.4f} V (peak-to-peak)")
            print(f"  Offset: {rigol.offset:.4f} V")
            print(f"  Frequency: {rigol.freq:.2f} Hz")
            print(f"  Phase: {rigol.phase} degrees")
            print(f"  Front panel unlocked: {rigol.unlock}")
            print(f"  Available waveforms: {rigol.available_waveforms}")
            print(f"  Waveform data info: {rigol.waveform_data}")
            
            return True
            
    except Exception as e:
        print(f"Error uploading waveform: {e}")
        return False


def plot_waveform(ramp_speeds, ramp_voltages, invert=True, sample_rate=250e6):
    """
    Plot the generated waveform for visualization.
    """
    # Convert to numpy arrays
    ramp_speeds = np.array(ramp_speeds)
    ramp_voltages = np.array(ramp_voltages)
    
    # Apply inversion if requested
    if invert:
        ramp_voltages_plot = np.max(ramp_voltages) - ramp_voltages
        ramp_speeds_plot = -ramp_speeds
    else:
        ramp_voltages_plot = ramp_voltages.copy()
        ramp_speeds_plot = ramp_speeds.copy()
        
    # Generate the waveform data
    data = ramp_gen_v(ramp_speeds_plot, ramp_voltages_plot, sample_rate)
    
    # Create time axis
    t = np.arange(len(data)) / sample_rate * 1e6  # Convert to microseconds
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(t, data, 'b-', linewidth=1)
    plt.xlabel('Time (μs)')
    plt.ylabel('Voltage (V)')
    plt.title('Generated Ramp Waveform')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print(f"Waveform statistics:")
    print(f"  Duration: {t[-1]:.2f} μs")
    print(f"  Points: {len(data)}")
    print(f"  Min voltage: {np.min(data):.4f} V")
    print(f"  Max voltage: {np.max(data):.4f} V")
    print(f"  Sample rate: {sample_rate/1e6:.1f} MS/s")


if __name__ == '__main__':
    # Configuration from the original MATLAB file
    # For uva Chip3 wg84 900 mW edfa pzt at 3.225 amplitude
    ramp_speeds = np.array([-0.001, 36, 0.01, 0.004, 0.002, 0.001, 0.0005, 0.0000005]) * 1.5
    ramp_voltages = np.array([0.0750, 2.5, 0.2940, 0.2190, 0.1590, 0.1140, 0.0840, 0.0765, 0.0750])
    
    # Configuration parameters
    RIGOL_IP = '10.0.0.61'
    INVERT = True
    SAMPLE_RATE = 250e6  # 250 MS/s
    WAVEFORM_NAME = 'ChipRamp'
    CHANNEL = 1
    
    print("Rigol DG4162 Ramp Waveform Generator")
    print("=" * 40)
    
    # Plot the waveform first
    print("Plotting waveform...")
    plot_waveform(ramp_speeds, ramp_voltages, INVERT, SAMPLE_RATE)
    
    # Ask user if they want to upload
    response = input("Upload waveform to Rigol? (y/n): ").lower().strip()
    
    if response == 'y' or response == 'yes':
        print("Uploading to Rigol DG4162...")
        
        # Advanced configuration options - now using all RigolDG4162 properties
        FREQUENCY_OVERRIDE = None  # Set to specific Hz if needed (overrides calculated frequency)
        PHASE_OVERRIDE = 0  # Phase in degrees
        
        success = upload_ramp_to_rigol(
            RIGOL_IP, ramp_speeds, ramp_voltages,
            invert=INVERT, sample_rate=SAMPLE_RATE,
            waveform_name=WAVEFORM_NAME, channel=CHANNEL,
            frequency_override=FREQUENCY_OVERRIDE, 
            phase_override=PHASE_OVERRIDE
        )
        
        if success:
            print("Upload completed successfully!")
        else:
            print("Upload failed!")
    else:
        print("Upload cancelled.")