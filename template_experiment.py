"""READ ME: All experiments must start with a few sentence readme giving a summation of what the experiment is."""
import sys
from os import path

parent_dir = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.dirname(parent_dir))

from network_manager import NetworkManager
from Instruments.oscilloscope_rigol import Oscilloscope
from Instruments.oscilloscope_helper import Oscilloscope_Helper
from Instruments.spectrum_analyzer_signal_hound import SpectrumAnalyzer
from Instruments.spectrum_analyzer_helper import SpectrumAnalyzer
from EInstrument import EInstrument
from EFileType import EFileType
from data_handler import DataHandler
def __main__():
    nm = NetworkManager()
    dh = DataHandler()
    instruments = nm.connect_instruments()
    inst_dict = {}
    #Insert your instrument calls here
    for i in instruments:
        #if you want byte stream data to be automatically saved
        i.data_handler.enable_auto_saving_data()
        inst_dict[i.name] = i
    #Create your automated helper objects
    osc_helper = Oscilloscope_Helper(inst_dict[EInstrument.OSCILLOSCOPE])
    #You can access and talk to the instruments through a map
    inst_dict[EInstrument.OSCILLOSCOPE].stop()
    inst_dict[EInstrument.OSCILLOSCOPE].trigger.set_mode("RS232")

    #OR you can individually cco the instrument
    osc = nm.connect_oscilloscope()
    
    osc.run()
    print(osc)
    osc_helper.set_timebase(2)
    
    #spec.save_user_preset
    #If you have 
    #Circuit code
    #....
    #Can iteratively collect data - probably best to put code like this in helper class for easy call
    data = []
    for i in range(10):
        #Collect data
        #
        data.append(osc.trigger.get_pulse_level())
    #Then write to file
    dh.write_to_file("Experiments/Outputs/osc_data", data, EFileType.CSV)

    #OR if data auto saving is mentioned in a description, then you can just call that function
    osc.data_handler.enable_auto_saving_data()
    byteArray = osc.system.set_setup()
    #And read the results into a different experiment or visualization library

    #Visualization with matplotlib etc.

    #After done, disconnect instruments"""
    nm.disconnect(instruments)

if __name__ == "__main__":
    __main__()