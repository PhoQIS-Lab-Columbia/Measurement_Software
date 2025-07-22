from time import sleep
from time import sleep
from EFileType import EFileType
from Instruments import Instrument
import pyvisa
from EInstrument import EInstrument
from SCPICommandTree.route import Route
from SCPICommandTree.trigger import Trigger

class SignalSwitcher(Instrument.Instrument):

    def __init__(self, instru, name=None):
        super().__init__(instru, name)
        self.route = self.routeClass(instru)
        self.trigger = self.triggerClass(instru)
        self.name = name

    class routeClass:
        def __init__(self, instru):
            self.instru = instru
            self.route = Route(instru)

        def close(self, channel_list: str):
            """Closes specific individual channels."""
            self.route.close_route_channel(channel_list)

        def open(self, channel_list: str):
            """Opens specific individual channels."""
            self.route.open_route_channel(channel_list)

        def open_all(self):
            """Opens all channels."""
            self.route.open_route_all_channels()

        def get_close_state(self, channel_list: str = None):
            """Queries the condition of individual switches (closed state)."""
            return self.route.get_route_close_state(channel_list)

        def get_open_state(self, channel_list: str):
            """Queries the condition of individual switches (open state)."""
            return self.route.get_route_open_state(channel_list)
        def scan(self, channel_list: str):
            """Specifies a list of channels for the instrument to sequence through."""
            self.route.set_route_scan(channel_list)

        def get_scan_list(self) -> str:
            """Returns the scan list."""
            return self.route.get_route_scan_list()
        
    class triggerClass():
        def __init__(self, instrument):
            self.trigger_obj = Trigger(instrument)
        def abort(self):
            """Resets the trigger system and aborts any in-progress trigger actions."""
            self.trigger_obj.abort()

        def initiate(self):
            """Initiates all trigger sequences as a group."""
            self.trigger_obj.initiate_immediate()

        def initiate_all(self):
            """Initiates all sequences."""
            self.trigger_obj.initiate_immediate_all()

        def set_continuous(self, enable: bool):
            """Sets whether the trigger system is continuously initiated."""
            self.trigger_obj.set_initiate_continuous(enable)

        def get_continuous(self) -> bool:
            """Queries whether the trigger system is continuously initiated."""
            return self.trigger_obj.get_initiate_continuous()

        def trigger(self):
            """Qualifies a single event before enabling the triggered sequence operation."""
            self.trigger_obj.trigger_sequence_immediate()

        def set_sequence_count(self, value: int):
            """Sets the count for the trigger sequence."""
            self.trigger_obj.set_trigger_sequence_count(value)

        def get_sequence_count(self) -> int:
            """Gets the count for the trigger sequence."""
            return self.trigger_obj.get_trigger_sequence_count()

        def set_sequence_source(self, source_type: str, source_index: int = None):
            """Sets the source for the event detector in the trigger sequence."""
            self.trigger_obj.set_trigger_sequence_source(source_type, source_index)

        def get_sequence_source(self) -> str:
            """Gets the source for the event detector in the trigger sequence."""
            return self.trigger_obj.get_trigger_sequence_source()