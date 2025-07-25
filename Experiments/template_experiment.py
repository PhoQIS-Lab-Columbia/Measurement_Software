"""READ ME: All experiments must start with a few sentence readme giving a summation of what the experiment is."""
#You can install additional apis, just make sure to add them to the requirements.txt
from network_manager import NetworkManager
from Instruments.oscilloscope_rigol import Oscilloscope
from Instruments.oscilloscope_helper import OscilloscopeHelper
from Instruments.spectrum_analyzer_signal_hound import SignalHound
from Instruments.spectrum_analyzer_helper import SignalHoundHelper
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
        i.enable_auto_saving_data()
        inst_dict[i.name] = i
    #Create your automated helper objects
    osc_helper = OscilloscopeHelper(inst_dict[EInstrument.OSCILLOSCOPE])
    #You can access and talk to the instruments through a map
    inst_dict[EInstrument.OSCILLOSCOPE].set_acquistion_mode("normal")
    inst_dict[EInstrument.OSCILLOSCOPE].set_trigger_sweep_mode("auto")

    #OR you can individually cco the instrument
    osc = nm.connect_oscilloscope()
    osc_helper = OscilloscopeHelper(osc)
    osc.channel.set_coupling_mode("AC", 1)
    osc.channel.get_bandwidth_limit(1)

    osc_helper.set_timebase()

    spec.save_user_preset
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
    byteArray = osc.system.set_setup()
    #And read the results into a different experiment or visualization library

    #Visualization with matplotlib etc.

    #After done, disconnect instruments
    nm.disconnect(instruments)