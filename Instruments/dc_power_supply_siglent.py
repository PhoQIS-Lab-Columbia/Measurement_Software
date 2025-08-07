from Instruments import Instrument
from EInstrument import EInstrument
import pyvisa

class DCPowerSupply(Instrument.Instrument):

    def __init__(self, instrument, save_files_path=None):
        super().__init__(instrument, EInstrument.DC_POWER_SUPPLY, save_files_path)
        self.channel1 = Channel(self.instrument, self.data_handler, "CH1")
        self.channel2 = Channel(self.instrument, self.data_handler, "CH2")
        
        #Class objects
    def save(self, name):
        """
        Save the current state in nonvolatile memory with the specified name.
        
        Parameters:
        name (str): The name to save the state under.
        """
        self.instrument.write(f"*SAV {name}")

    #TODO: Add SCPI functions below


    def recall(self, name):
        """
        Recall the state previously saved with the specified name.
        
        Parameters:
        name (str): The name of the state to recall.
        """
        return self.instrument.write(f"*RCL {name}")
    """def set_channel(self, channel):
        
        Select the channel that will be operated.
        
        Parameters:
        channel (str): The channel to operate on. Valid values are 'CH1' or 'CH2'.
        
        if channel in ['CH1', 'CH2']:
            self.instrument.write(f"INSTrument {channel}")
        else:
            print("Invalid channel. Please select 'CH1' or 'CH2'.")
    def get_current_channel(self):
        
        Query the currently selected channel.
        
        Returns:
        str: The currently selected channel ('CH1' or 'CH2').
        
        return self.instrument.query("INSTrument?")"""
    def get_system_error(self) -> str:
        """
        Queries the next error from the error queue, returning its code and message.
        Notes: Query only.
        """
        response = self.instrument.query(":SYST:ERR?").strip()
        return response
    
    def enable_output_channel(self, source: str, state: str):
        """
        Turn on/off the specified channel.

        Parameters:
        source (str): Channel to control ('CH1', 'CH2', 'CH3').
        state (str): Output state ('ON', 'OFF').
        """
        if source not in ['CH1', 'CH2', 'CH3']:
            raise ValueError("Invalid source. Must be 'CH1', 'CH2', or 'CH3'.")
        if state not in ['ON', 'OFF']:
            raise ValueError("Invalid state. Must be 'ON' or 'OFF'.")
        self.instrument.write(f"OUTPut {source},{state}")

    def set_output_mode(self, mode: int):
        """
        Select the operation mode.

        Parameters:
        mode (int): 0 for Independent, 1 for Series, 2 for Parallel.
        """
        if mode not in [0, 1, 2]:
            raise ValueError("Invalid mode. Must be 0 (Independent), 1 (Series), or 2 (Parallel).")
        self.instrument.write(f"OUTPut:TRACK {mode}")
    #TODO: Test
    def get_status(self):
        """
        Query the current working state and decode the status bits.

        Returns:
            dict: Decoded status information.
        """
        hex_status = self.instrument.query("SYSTem:STATus?").strip()
        # Remove '0x' if present and convert to int
        status_int = int(hex_status, 16)
        # Convert to 8-bit binary string (pad with zeros)
        status_bin = format(status_int, '08b')

        status = {
            "CH1_mode": "CC" if status_bin[-1] == '1' else "CV",
            "CH2_mode": "CC" if status_bin[-2] == '1' else "CV",
            "operation_mode": (
                "Independent" if status_bin[-4:-2] == '01' else
                "Parallel" if status_bin[-4:-2] == '10' else
                "Series" if status_bin[-4:-2] == '11' else
                "Unknown"
            ),
            "CH1_output": "ON" if status_bin[-5] == '1' else "OFF",
            "CH2_output": "ON" if status_bin[-6] == '1' else "OFF"
        }
        return status
    def lock_keys(self):
        """
        Lock the keys on the instrument.

        """
        self.instrument.write("*LOCK")

    def unlock_keys(self):
        """
        Unlock the keys on the instrument.

        """
        self.instrument.write("*UNLOCK")
        
class Channel:
    def __init__(self, instrument, data_handler, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.channel = channel
        self.current = Current(instrument, data_handler, channel)
        self.voltage = Voltage(instrument, data_handler, channel)

class Current:
    """Change and get the current of the selected channel."""
    def __init__(self, instrument, data_handler, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.channel = channel

    def get(self):
        """
        Query the current value.
        
        Returns:
        float: The current value in Amperes.
        """
        
        response = self.instrument.query(f"MEASure:CURRent? {self.channel}")
        return response
    def set(self, current):
        """Set current value for the current channel"""
        self.channel+":CURRent "+str(current)

class Voltage:
    """Change and get the voltage of the selected channel."""
    def __init__(self, instrument, data_handler, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.channel = channel

    def get(self):
        """
        Query the voltage value.
        
        Returns:
        float: The current value in Amperes.
        """
        
        response = self.instrument.query(f"MEASure:VOLTage? {self.channel}")
        return response
        
    def set(self, voltage):
        """Set voltage value for the current channel"""
        self.channel+":VOLTage "+str(voltage)