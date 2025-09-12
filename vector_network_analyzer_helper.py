import json
class VNA_Helper:
    def __init__(self, inst):
        self.instrument = inst

    def set_voltage_parameters(self, channel: int, voltage: float):
        """Set the voltage parameters for a specific channel."""
        self.set_function1()
        self.set_function2()
        #...
        x = self.get_function1()
        y = self.get_function2()
        return x, y
