from enum import Enum
'''MODIFY WHEN ADDING A NEW INSTRUMENT TYPE'''
class EFileType(Enum):
    CSV = ".csv"
    TXT = ".txt"
    JSON = ".json"
    BIN = ".bin"
    PNG = ".png"