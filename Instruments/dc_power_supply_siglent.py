from Instruments import Instrument
from Instruments.EInstrument import EInstrument
import pyvisa
from data_handler import DataHandler
class DCPowerSupply():

    def __init__(self, instrument, save_files_path=None):
        self.instrument = instrument
        self.name = EInstrument.DC_POWER_SUPPLY
        
        if save_files_path is None:
            self.data_handler = DataHandler()  # Default format set to JSON
        else:
            self.data_handler = DataHandler(save_files_path)
        self.channel1 = Channel(self.instrument, self.data_handler, "CH1")
        self.channel2 = Channel(self.instrument, self.data_handler, "CH2")
        
        #Class objects
    def get_id(self):
        """
        Query the ID string of the instrument.

        Returns:
        str: The ID string in the format "RIGOL TECHNOLOGIES,<model>,<serial number>,<software version>".
        """
        response = self.instrument.query("*IDN?")
        return response.strip()

    def save(self, name):
        """
        Save the current state in nonvolatile memory with the specified name.
        
        Parameters:
        name (str): The name to save the state under.
        """
        self.instrument.write(f"*SAV {name}")


    def recall(self, name):
        """
        Recall the state previously saved with the specified name.
        
        Parameters:
        name (str): The name of the state to recall.
        """
        return self.instrument.write(f"*RCL {name}")
    def set_work_operation(self, mode: str):
        """
        Set the work operation mode to 2-wire or 4-wire.

        Parameters:
        mode (str): '2W' for 2-wire, '4W' for 4-wire.
        """
        if mode not in ['2W', '4W']:
            raise ValueError("Invalid mode. Must be '2W' or '4W'.")
        self.instrument.write(f"MODE:SET {mode}")

    def get_system_error(self) -> str:
        """
        Queries the next error from the error queue, returning its code and message.
        Notes: Query only.
        """
        response = self.instrument.query(":SYST:ERR?").strip()
        return response
    
    def enable_output_channel(self, source: str):
        """
        Turn on the specified channel.

        Parameters:
        source (str): Channel to control ('CH1', 'CH2', 'CH3').
        state (str): Output state ('ON', 'OFF').
        """
        if source not in ['CH1', 'CH2', 'CH3']:
            raise ValueError("Invalid source. Must be 'CH1', 'CH2', or 'CH3'.")
        
        self.instrument.write(f"OUTPut {source},ON")
    
    def disable_output_channel(self, source: str):
        """
        Turn off the specified channel.

        Parameters:
        source (str): Channel to control ('CH1', 'CH2', 'CH3').
        
        """
        if source not in ['CH1', 'CH2', 'CH3']:
            raise ValueError("Invalid source. Must be 'CH1', 'CH2', or 'CH3'.")
    
        self.instrument.write(f"OUTPut {source},OFF")

    def set_output_mode(self, mode: int):
        """
        Select the operation mode.

        Parameters:
        mode (int): 0 for Independent, 1 for Series, 2 for Parallel.
        """
        if mode not in [0, 1, 2]:
            raise ValueError("Invalid mode. Must be 0 (Independent), 1 (Series), or 2 (Parallel).")
        self.instrument.write(f"OUTPut:TRACK {mode}")

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
        self.power = Power(instrument,data_handler,channel)
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
        self.instrument.write(f"INSTrument {self.channel}")
        response = self.instrument.query(f"MEASure:CURRent? {self.channel}")
        return response
    def set(self, current):
        """Set current value for the current channel"""
        self.instrument.write(f"INSTrument {self.channel}")
        self.instrument.write(self.channel+":CURRent "+str(current))
    def set_over_current_protection(self, value):
        """
        Set the over-current protection (OCP) value for the current channel.

        Parameters:
        value (float): The OCP value to set (in Amperes).
        """
        self.instrument.write(f"INSTrument {self.channel}")
        self.instrument.write(f"{self.channel}:OCP {value}")

    def get_over_current_protection(self):
        """
        Query the over-current protection (OCP) value for the current channel.

        Returns:
        float: The OCP value in Amperes.
        """
        self.instrument.write(f"INSTrument {self.channel}")
        response = self.instrument.query(f"{self.channel}:OCP?")
        return response
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
        self.instrument.write(f"INSTrument {self.channel}")
        response = self.instrument.query(f"MEASure:VOLTage? {self.channel}")
        return response
        
    def set(self, voltage):
        """Set voltage value for the current channel"""
        self.instrument.write(f"INSTrument {self.channel}")
        self.instrument.write(self.channel+":VOLTage "+str(voltage))
    def set_over_voltage_protection(self, value):
        """
        Set the over-voltage protection (OVP) value for the current channel.

        Parameters:
        value (float): The OVP value to set (in Volts).
        """
        self.instrument.write(f"INSTrument {self.channel}")
        self.instrument.write(f"{self.channel}:OVP {value}")

    def get_over_voltage_protection(self):
        """
        Query the over-voltage protection (OVP) value for the current channel.

        Returns:
        float: The OVP value in Volts.
        """
        self.instrument.write(f"INSTrument {self.channel}")
        response = self.instrument.query(f"{self.channel}:OVP?")
        return response
    
class Power:
    """Change and get the power of the selected channel."""
    def __init__(self, instrument, data_handler, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.channel = channel

    def get(self):
        """
        Query the power value.
        
        Returns:
        float: The power value in watt.
        """
        self.instrument.write(f"INSTrument {self.channel}")
        response = self.instrument.query(f"MEASure:POWEr? {self.channel}")
        return response
        
    def set(self, voltage):
        """Set power value for the current channel"""
        self.instrument.write(f"INSTrument {self.channel}")
        self.instrument.write(self.channel+":POWEr "+str(voltage))