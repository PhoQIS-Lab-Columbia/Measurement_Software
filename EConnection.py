from enum import Enum
'''MODIFY WHEN ADDING A NEW INSTRUMENT TYPE'''
class EConnection(Enum):
    USB = "USB"
    GPIB = "GPIB"
    TCPIP = "TCPIP"
    SERIAL = "SERIAL"
    VISA = "VISA"
    NONE = "NONE"  # For cases where no connection is used