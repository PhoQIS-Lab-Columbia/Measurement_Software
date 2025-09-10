import subprocess
import psutil
import json
import csv
from EInstrument import EInstrument
class Flowmeter:
    def __init__(self, csv_paths):
        #TODO Add pop up about how experiemtn must be set up in flowmeter, but if project already set up (check if can do,) the ndo not need to set blah blah blah
        self.name = EInstrument.FLOW_METER
        with open('program_paths.json') as file:
            p = json.load(file)
        self.program_path = p[self.name.value]
        self.name = EInstrument.FLOW_METER
        self.app = subprocess.Popen([self.program_path], shell = False) # Placeholder for a path to 
        self.csv_paths = [csv_paths]
        self.flowmeter_count = 1
    def set_csv_path(self, flowmeter_port, new_path):
        self.csv_paths[flowmeter_port] = new_path
    def load_csv(self):
        data = []
        for i in range(0,self.flowmeter_count):
            with open(self.csv_paths[i], 'r') as file:
                d = csv.DictReader(file) # Returns rows as dictionaries
                data.append(d)

        return data
        
    def disconnect(self):
        """
        Ends data logging on the flowmeter.
        """
        self.app.terminate()