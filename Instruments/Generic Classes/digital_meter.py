from time import sleep
from time import sleep
from EFileType import EFileType
from Instruments import Instrument
import pyvisa
from EInstrument import EInstrument
from PIL import Image
from SCPICommandTree.trigger import Trigger
from SCPICommandTree.route import Route
from SCPICommandTree.sense import Sense
from EInstrument import EInstrument
class DigitalMeter(Instrument.Instrument):
    def __init__(self, instru, name=None):
        super().__init__(instru, name)
        self.trigger = self.triggerClass(instru)
        self.route = self.routeClass(instru)
        self.name = name
        if name is EInstrument.OHM_METER:
              self.sense = self.senseClass(instru)

    class triggerClass():
        def __init__(self, instrument):
            self.trigger_obj = Trigger(instrument)
        def abort(self):
                """
                Resets the trigger system and places all trigger sequences in the IDLE state.
                Any actions related to the trigger system that are in progress shall also be aborted.
                This command is an event and has no associated *RST condition or query form.
                """
                return self.trigger_obj.abort()

        def initiate_immediate(self):
                """
                Causes all sequences to exit the IDLE state; they are initiated.
                The IMMediate command causes the trigger system to initiate and complete one full trigger cycle,
                returning to IDLE on completion.
                This command is an event and cannot be queried as there is no state associated with it.
                """
                return self.trigger_obj.initiate_immediate()

        

        def set_trigger_sequence_count(self, value):
                """
                Controls the path of the trigger system in the upward traverse of the event detection layer.
                :param value: The count value (numeric value, 1 or greater).
                Notes: At *RST, this value is set to 1.
                """
                return self.trigger_obj.set_trigger_sequence_count(value)

        def get_trigger_sequence_count(self):
                """
                Queries the count for the TRIGger sequence.
                :return: The count value.
                """
                return self.trigger_obj.get_trigger_sequence_count()

        def set_trigger_sequence_delay(self, value):
                """
                Sets the time duration between the recognition of an event(s) and the downward exit of the specified layer.
                :param value: The delay time in seconds (numeric value, zero or positive).
                Notes: At *RST, this value is set to 0 or the smallest available positive value.
                """
                return self.trigger_obj.set_trigger_sequence_delay(value)

        def get_trigger_sequence_delay(self):
                """
                Queries the delay time for the TRIGger sequence.
                Return: The delay time in seconds.
                """
                return self.trigger_obj.get_trigger_sequence_delay()

        def set_trigger_sequence_source(self, source_type):
                """
                Selects the source for the event detector. Only one source may be specified at a time.
                :param source_type: The type of source (e.g., "AINTernal", "BUS", "ECLTrg", "EXTernal", "HOLD",
                        "IMMediate", "INTernal", "LINE", "LINK", "MANual", "OUTPut", "TIMer", "TTLTrg").
                Notes: At *RST, IMMediate shall be selected as the SOURce.
                """
                return self.trigger_obj.set_trigger_sequence_source(source_type)

        def get_trigger_sequence_source(self):
                """
                Queries the source for the event detector for the TRIGger sequence.
                Return: The source type string (e.g., "IMMediate", "TTLTrg0").
                """
                return self.trigger_obj.get_trigger_sequence_source()
      
        def set_arm_sequence_layer_source(self, source_type: str, source_index: int = None, sequence_number: int = None, layer_number: int = None):
            """
            Selects the source for the event detector. Only one source may be specified at a time.
            :param source_type: The type of source (e.g., "AINTernal", "BUS", "ECLTrg", "EXTernal", "HOLD",
                                "IMMediate", "INTernal", "LINE", "LINK", "MANual", "OUTPut", "TIMer", "TTLTrg").
            :param source_index: Optional. Numeric suffix for sources like ECLTrg, EXTernal, INTernal, OUTPut, TTLTrg.
            :param sequence_number: Optional. The numeric suffix for SEQuence.
            :param layer_number: Optional. The numeric suffix for LAYer.
            Notes: At *RST, IMMediate shall be selected as the SOURce.
            """
            return self.trigger_obj.set_arm_sequence_layer_source(source_type, source_index,sequence_number,layer_number)

        def get_arm_sequence_layer_source(self, sequence_number: int = None, layer_number: int = None):
            """
            Queries the source for the event detector for the ARM sequence layer.
            :param sequence_number: Optional. The numeric suffix for SEQuence.
            :param layer_number: Optional. The numeric suffix for LAYer.
            :return: The source type string (e.g., "IMMediate", "TTLTrg0").
            """
            return self.trigger_obj.get_arm_sequence_layer_source()
        
    class routeClass():
        def __init__(self, instrument):
            self.route_obj = Route(instrument)
        def set_route_terminals(self, terminal_type: str):
            """Configures the terminal connections.
            Parameters:
            terminal_type: FRONT|REAR|BOTH|NONE"""
            self.route_obj.set_route_terminals(terminal_type)
        
    class senseClass():
        def __init__(self, instrument):
            self.sense_obj = Sense(instrument)
        def set_sense_bandwidth_resolution(self, value: float):
            """Controls the resolution bandwidth of the instrument in Hz.
            Parameters:
            value: The resolution bandwidth in Hz (numeric value)."""
            self.sense_obj.set_sense_bandwidth_resolution(value)

        def get_sense_bandwidth_resolution(self) -> float:
            """Returns the resolution bandwidth of the instrument in Hz."""
            return self.sense_obj.get_sense_bandwidth_resolution()
        def set_sense_resistance_ocompensated(self, enable: bool):
            """Enables or disables the offset compensation when measuring resistance.
            Parameters:
            enable: True to enable, False to disable."""
            self.sense_obj.set_sense_resistance_ocompensated(enable)

        def get_sense_resistance_ocompensated(self) -> bool:
            """Returns: True if offset compensation is enabled for Resistance, False if disabled."""
            return self.sense_obj.get_sense_resistance_ocompensated()