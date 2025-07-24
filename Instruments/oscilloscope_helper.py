from oscilloscope_rigol import Oscilloscope
class Oscilloscope_Helper:
    def __init__(self,oscilloscope:Oscilloscope):
        self.oscilloscope = oscilloscope
    def set_timebase(self, timebase: float):
        """Set the oscilloscope time base."""
        
        if self.oscilloscope.math.is_fft_split_enabled():
            self.oscilloscope.math.set_source1("CHAN1")
        
        self.oscilloscope.set_timebase(timebase)