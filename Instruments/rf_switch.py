from Instruments.Instrument import Instrument
from Instruments.EInstrument import EInstrument
import pyvisa
import time
from Instruments.data_handler import DataHandler
 
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
        self.auto_disable = False
        self.channel_1 = Channel(instrument, data_handler, switch, 1)
        self.channel_2 = Channel(instrument, data_handler, switch, 2)
        self.channel_3 = Channel(instrument, data_handler, switch, 3)
        self.channel_4 = Channel(instrument, data_handler, switch, 4)
        self.channel_5 = Channel(instrument, data_handler, switch, 5)
        self.channel_6 = Channel(instrument, data_handler, switch, 6)
        self.list_channels = [self.channel_1, self.channel_2, self.channel_3, self.channel_4, self.channel_5, self.channel_6]
    def enable_auto_disable(self):
        """
        If on, then if a channel is already enabled when another channel is trying to turn on, 
        the first channel will be automatically turned off. Otherwise it will not turn on the new channel and jsut issue a warning.
        
        """
        self.auto_disable = True
        for c in self.list_channels:
            c.auto_disable = True

    def disable_auto_disable(self):
        """
        If off, it will not turn on the new channel and just issue a warning. Otherwise, if a channel is already enabled when another channel is trying to turn on, 
        the first channel will be automatically turned off.
        
        """
        self.auto_disable = False
        for c in self.list_channels:
            c.auto_disable = False
    def is_auto_disable_on(self):
        """
        Return true if auto disable is on.
        """
        return self.auto_disable
    
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
        res = self.instrument.query("Read_Channel_Status?")
        idx = res.find(self.switch) + len(self.switch+"_status:")
        return res[idx:idx+6]
class Channel:
    def __init__(self, instrument, data_handler, switch, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.switch = switch
        self.channel = channel
        self.auto_disable = False
    def enable(self):
        """
        Enable the channel for this switch.
        """
        status = self.get_status()
        if status == '000000':
            self.instrument.write(f"{self.switch}_{self.channel}_ON")
        else:
            if self.auto_disable:
                idx = status.index('1')
                self.instrument.write(f"{self.switch}_{idx+1}_OFF")
                time.sleep(0.3)
                self.instrument.write(f"{self.switch}_{self.channel}_ON")
            else: 
                print(f"Channel {status.index('1')+1} is already on. Please disable it or reset the switch before turning on channel {self.channel}")
    
    def disable(self):
        """
        Disable the channel for this switch.
        """
        self.instrument.write(f"{self.switch}_{self.channel}_OFF")

    def get_status(self):
        """Return true if the channel is enabled.
        Returns:
            boolean: True if channel is enable, false otherwise.
        """
        
        res = self.instrument.query("Read_Channel_Status?")
        idx = res.find(self.switch) + len(self.switch+"_status:")
        switch_stats = res[idx:idx+6]
        return switch_stats