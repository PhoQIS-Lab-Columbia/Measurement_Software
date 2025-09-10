from Instruments import Instrument
from EInstrument import EInstrument
import pyvisa
import time
from data_handler import DataHandler
 
class RF_Switch():

    def __init__(self, instrument, save_files_path):
        self.instrument = instrument
        self.name = EInstrument.RF_SWITCH
        if save_files_path is None:
            self.data_handler = DataHandler()  # Default format set to JSON
        else:
            self.data_handler = DataHandler(save_files_path)
        self.switch1 = Switch(self.instrument, self.data_handler, "CH1")
        self.switch2 = Switch(self.instrument, self.data_handler, "CH2")
        #Class objects
    
    def disconnect(self):
        pass
    def reset_all(self):
        """
        Reset all switches to their default state. If successfully returns 000000
        """
        res = self.instrument.write("Reset")
        return res
    
    #TODO: Add SCPI functions below
class Switch:
    """RF Switch class"""
    def __init__(self, instrument, data_handler, switch):
        self.instrument = instrument
        self.data_handler = data_handler
        self.switch = switch
        self.channel1 = Channel(instrument, data_handler, switch, 1)
        self.channel2 = Channel(instrument, data_handler, switch, 2)
        self.channel3 = Channel(instrument, data_handler, switch, 3)
        self.channel4 = Channel(instrument, data_handler, switch, 4)
        self.channel5 = Channel(instrument, data_handler, switch, 5)
        self.channel6 = Channel(instrument, data_handler, switch, 6)
    def reset(self):
        """
        Reset the switch to its default state. If successfully returns 000000
        """
        res = self.instrument.write(f"{self.switch}_RES")
        return res
    def get_status(self):
        """Get which switch channels are enabled.
        Returns:
            str: A string representing the status of the switch channels.
        """
        res = self.instrument.write(f"{self.switch}_Status")
        return res
class Channel:
    def __init__(self, instrument, data_handler, switch, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.switch = switch
        self.channel = channel

    def enable(self):
        """
        Enable the channel for this switch.
        """
        status = self.get_status()
        #if status == '000000':
        self.instrument.write(f"CH{self.switch}_{self.channel}_ON")
        #else:
            #print(f"Channel {status.index('1')} is already on. Please disable it or reset the switch before turning on channel {self.channel}")
    
    def disable(self):
        """
        Enable the channel for this switch.
        """
        self.instrument.write(f"CH{self.switch}_{self.channel}_OFF")

    def get_status(self):
        """Get which switch channels are enabled.
        Returns:
            str: A string representing the status of the switch channels.
        """
        res = self.instrument.write(f"{self.switch}_Status?")
        return res