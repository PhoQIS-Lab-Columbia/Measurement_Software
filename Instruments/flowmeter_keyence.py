import subprocess
import psutil
import json
from EInstrument import EInstrument
class Flowmeter:
    def __init__(self):
        with open('program_paths.json') as file:
            p = json.load(file)
        self.program_path = p[self.name.value]
        self.name = EInstrument.FLOW_METER
        self.datalogger = subprocess.Popen([self.program_path], shell = False) # Placeholder for a path to 
    def end_data_logging(self):
        """
        Ends data logging on the flowmeter.
        """
        subprocess.terminate([""])