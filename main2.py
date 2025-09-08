import subprocess
import json
from EInstrument import EInstrument
import pyvisa

rm = pyvisa.ResourceManager()
with open('program_paths.json') as file:
    p = json.load(file)
program_path = p[EInstrument.VECTOR_NETWORK_ANALYZER.value]
app = subprocess.Popen([program_path], shell = False)


# Open a session to the S4VNA software, S4VNA must be running at this point
inst = rm.open_resource('TCPIP0::localhost::5025::SOCKET')

# For SOCKET programming, we want to tell VISA to use a terminating character
#   to end a read and write operation.
inst.read_termination = '\n'
inst.write_termination = '\n'