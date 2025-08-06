from enum import Enum
'''MODIFY WHEN ADDING A NEW INSTRUMENT TYPE'''
class EInstrument(Enum):
    OSCILLOSCOPE = "oscilloscope"
    SPECTRUM_ANALYZER = "spectrum analyzer"
    OHM_METER = "ohm meter"
    VECTOR_NETWORK_ANALYZER = "vector network analyzer"
    DIGITAL_ATTENUATOR = "digital attenuator"
    SIGNAL_GENERATOR = "signal generator"
    DC_POWER_SUPPLY = "DC power supply"
    LOCK_IN_AMP = "Lock In Amplifier"