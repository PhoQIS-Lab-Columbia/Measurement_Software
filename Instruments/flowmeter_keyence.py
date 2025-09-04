import subprocess
import psutil
import json
from EInstrument import EInstrument
class Flowmeter:
    def __init__(self):
        self.name = EInstrument.FLOW_METER
        with open('program_paths.json') as file:
            p = json.load(file)
        self.program_path = p[self.name.value]
        self.name = EInstrument.FLOW_METER
        self.app = subprocess.Popen([self.program_path], shell = False) # Placeholder for a path to 
    def load_csv(self, file_name =  None):
        
        pass
    def disconnect(self):
        """
        Ends data logging on the flowmeter.
        """
        self.app.terminate()