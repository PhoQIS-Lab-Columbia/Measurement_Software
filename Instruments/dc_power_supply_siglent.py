from Instruments import Instrument
from Instruments.EInstrument import EInstrument
import pyvisa
from Instruments.data_handler import DataHandler
class DCPowerSupply():
    """Class for controlling the a DC Power Supply instrument."""

    def __init__(self, instrument, save_files_path=None):
        """Initialize the DC Power Supply instrument.
        
        :param instrument: The pyvisa instrument instance.
        :type instrument: pyvisa.resources.Resource
        :param save_files_path: Optional path to save data files. If None, defaults to JSON format.
        :type save_files_path: str or None"""
        self.instrument = instrument
        self.name = EInstrument.DC_POWER_SUPPLY
        
        if save_files_path is None:
            self.data_handler = DataHandler()  # Default format set to JSON
        else:
            self.data_handler = DataHandler(save_files_path)
        self.channel_1 = Channel(self.instrument, self.data_handler, "CH1")
        self.channel_2 = Channel(self.instrument, self.data_handler, "CH2")
        
        #Class objects
    def get_id(self):
        """
        Query the ID string of the instrument.

        :return: The ID string in the format "RIGOL TECHNOLOGIES,<model>,<serial number>,<software version>".
        :rtype: str
        """
        response = self.instrument.query("*IDN?")
        return response.strip()

    def save(self, name):
        """
        Save the current state in nonvolatile memory with the specified name.  
        
        :param name: The name to save the state under.
        :type name: str
        """
        self.instrument.write(f"*SAV {name}")


    def recall(self, name):
        """
        Recall the state previously saved with the specified name.

        :param name: The name of the state to recall.
        :type name: str
        """
        return self.instrument.write(f"*RCL {name}")
    def set_work_operation(self, mode: str):
        """
        Set the work operation mode to 2-wire or 4-wire.

        :param mode: '2W' for 2-wire, '4W' for 4-wire.
        :type mode: str
        """
        if mode not in ['2W', '4W']:
            raise ValueError("Invalid mode. Must be '2W' or '4W'.")
        self.instrument.write(f"MODE:SET {mode}")

    def get_system_error(self) -> str:
        """
        Query the system error queue.   
       
        :return: The error code and message in the format "<code>,<message>".
        :rtype: str
        """
        response = self.instrument.query(":SYST:ERR?").strip()
        return response
    
    def enable_output_channel(self, source: str):
        """
        Turn on the specified channel.

        :param source: Channel to control ('CH1', 'CH2', 'CH3').
        :type source: str
        :param state: Output state ('ON', 'OFF').
        :type state: str
        """
        if source not in ['CH1', 'CH2', 'CH3']:
            raise ValueError("Invalid source. Must be 'CH1', 'CH2', or 'CH3'.")
        
        self.instrument.write(f"OUTPut {source},ON")
    
    def disable_output_channel(self, source: str):
        """
        Turn off the specified channel.

        :param source: Channel to control ('CH1', 'CH2', 'CH3').
        :type source: str
        
        """
        if source not in ['CH1', 'CH2', 'CH3']:
            raise ValueError("Invalid source. Must be 'CH1', 'CH2', or 'CH3'.")
    
        self.instrument.write(f"OUTPut {source},OFF")

    def set_output_mode(self, mode: int):
        """
        Select the operation mode.

        :param mode: 0 for Independent, 1 for Series, 2 for Parallel.
        :type mode: int
        """
        if mode not in [0, 1, 2]:
            raise ValueError("Invalid mode. Must be 0 (Independent), 1 (Series), or 2 (Parallel).")
        self.instrument.write(f"OUTPut:TRACK {mode}")

    def get_status(self):
        """
        Query the current working state and decode the status bits.

        :return: Decoded status information.
        :rtype: dict
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
    """Channel to be selected."""
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

        :return: The current value in Amperes.
        :rtype: float
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

        :param value: The OCP value to set (in Amperes).
        :type value: float
        """
        self.instrument.write(f"INSTrument {self.channel}")
        self.instrument.write(f"{self.channel}:OCP {value}")

    def get_over_current_protection(self):
        """
        Query the over-current protection (OCP) value for the current channel.

        :return: The OCP value in Amperes.
        :rtype: float
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

        :return: The current value in Volts.
        :rtype: float
        """
        self.instrument.write(f"INSTrument {self.channel}")
        response = self.instrument.query(f"MEASure:VOLTage? {self.channel}")
        return response
        
    def set(self, voltage):
        """Set voltage value for the current channel
        
        :param voltage: The voltage value to set (in Volts).
        :type voltage: float"""
        self.instrument.write(f"INSTrument {self.channel}")
        self.instrument.write(self.channel+":VOLTage "+str(voltage))
    def set_over_voltage_protection(self, value):
        """
        Set the over-voltage protection (OVP) value for the current channel.

        :param value: The OVP value to set (in Volts).
        :type value: float
        """
        self.instrument.write(f"INSTrument {self.channel}")
        self.instrument.write(f"{self.channel}:OVP {value}")

    def get_over_voltage_protection(self):
        """
        Query the over-voltage protection (OVP) value for the current channel.

        :return: The OVP value in Volts.
        :rtype: float
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

        :return: The power value in watt.
        :rtype: float
        """
        self.instrument.write(f"INSTrument {self.channel}")
        response = self.instrument.query(f"MEASure:POWEr? {self.channel}")
        return response
        
    def set(self, voltage):
        """Set power value for the current channel
        
        :param voltage: The power value to set (in watt).
        :type voltage: float"""
        self.instrument.write(f"INSTrument {self.channel}")
        self.instrument.write(self.channel+":POWEr "+str(voltage))