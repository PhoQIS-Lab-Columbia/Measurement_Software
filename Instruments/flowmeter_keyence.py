import subprocess
import psutil
import json
import csv
import psutil
from Instruments.EInstrument import EInstrument
class Flowmeter:
    def __init__(self, csv_paths, program_open = False):
        #TODO Add pop up about how experiemtn must be set up in flowmeter, but if project already set up (check if can do,) the ndo not need to set blah blah blah
        self.name = EInstrument.FLOW_METER
        with open('program_paths.json') as file:
            p = json.load(file)
        self.program_path = p[self.name.value]
        self.name = EInstrument.FLOW_METER
        pieces = self.program_path.split('/')
        self.default_csv_path = "C:/Users/phoqi/Documents/NQ Sensor Monitor/"
        if self.process_exists(pieces[len(pieces)-1]):
            self.app = self.get_process_by_name(pieces[len(pieces)-1])
        else:
            self.app = subprocess.Popen([self.program_path], shell = False) # Placeholder for a path to 
        self.flowmeter_count = 1
        self.csv_paths = [""]*self.flowmeter_count
        print("The flowmeter will open a pop up window. Press start to begin monitoring. When enough time has passed, collect a csv using the NQ software. Copy the file path and load ")
    
    def process_exists(self, process_name): 
        call = 'TASKLIST', '/FI', f'imagename eq {process_name}'
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(process_name.lower())
    def get_process_by_name(self,name):
        """Return the first psutil.Process object matching the process name."""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() == name.lower():
                return proc  # This is a psutil.Process object
        return None
    def add_csv(self, flowmeter_ports, new_files):
        """Add a new csv path for a specfic flowmeter in a particular NQ port."
        Parameters:
        flowmeter_port (int): The port number of the flowmeter (0-indexed).
        new_path (str): The file path to the csv file."""
        self.csv_paths[flowmeter_ports] = new_files
    def load_csv(self, folder_path = None):
        """Load csv data into a lsit of dictionaries.
        Parameters:
        (optional) folder_path (str): The folder path where the csv files are located. If None, uses default path.
        Returns:
        list: A list of dictionaries containing the csv data for each flowmeter."""
        data = []
        if folder_path is None:
            folder_path = self.default_csv_path
        for i in range(0,self.flowmeter_count):
            with open(folder_path+self.csv_paths[i], 'r') as file:
                d = csv.DictReader(file) # Returns rows as dictionaries
                data.append(d)

        return data
        
    def disconnect(self):
        """
        Ends data logging on the flowmeter and closes NQ.
        """
        
        self.app.terminate()