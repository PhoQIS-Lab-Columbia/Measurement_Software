import json
import csv
import os
import io
from PIL import Image
from EFileType import EFileType
class DataHandler():
    def __init__(self, format):
        self.writer = None
        self.reader = None
        self.format = EFileType.CSV
    def remove_tmc_header(self, bytes):
        """Removes TMC header from image bytes"""
        #First byte is #, ignore
        size_count = int.from_bytes(bytes[1])
        return bytes[2+size_count:]

    def bytes_to_image(self, bytes, image_name = "Image", format="PNG", header = None):
        """Converts bytes to image object"""
        if header is not None:
            if header == "TMC":
                #Remove TMC header if present
                bytes = self.remove_image_tmc_header(bytes)

        image = Image.open(io.BytesIO(bytes))
        im = image.save(f"{image_name}.{format.lower()}")
        return im, bytes
    
    def set_default_file_type(self, format):
        """"Sets default file type for reading and writing files."""
        if type(format) is str:
            format = EFileType(format).name
        self.format = format
        #TODO Change readers and writers
    
    def read_file(self, file_path, format = None):
        """Reads file and returns data"""
        fmt = self.format
        if format is not None:  
            fmt = format
        if fmt == EFileType.CSV:
            with open(file_path, mode='r', newline='') as csvfile:
                self.reader = csv.reader(csvfile)
                return list(self.reader)
        elif fmt == EFileType.JSON:
            with open(file_path, 'r') as jsonfile:
                return json.load(jsonfile)
        elif fmt == EFileType.TXT:
            with open(file_path, 'r') as txtfile:
                return txtfile.readlines()
        elif fmt == EFileType.BIN:  
            with open(file_path, 'rb') as binfile:
                return binfile.read()
        else:
            raise ValueError(f"Unsupported file format: {self.format}")
        
    def write_to_file(self, file_path, data, file_type = None, headers = None):
        """Writes data to file
        params: file_path: str - path to file
                data: list or dict - data to write to file
                file_type: EFileType - type of file to write to, if None then uses default format
                headers: list - headers for file, if None then numerical headers are used. Only used if data is not a dictionary.
                If file already exists, headers are not written again."""
        
        format = self.format
        if file_type is not None:
            format = file_type
        file_path = file_path + format.value if not file_path.endswith(format.value) else file_path
        file_exists = os.path(file_path).isfile()
        if file_exists:
            m = 'a'  
        else: 
            m = 'w'
            if headers is None:
                headers = range(0, len(data))

        #TODO Check data formatting possibilities

        if format == EFileType.CSV:
            with open(file_path, mode=m, newline='') as csvfile:
                self.writer = csv.writer(csvfile)
                if not file_exists:
                    self.writer.writerow(headers)
                self.writer.writerows(data)

        elif format == EFileType.JSON:
            if file_exists:
                with open(file_path, 'r') as jsonfile:
                    already_in_file = json.load(jsonfile)

            with open(file_path, 'w') as jsonfile:
                json.dump(data, jsonfile)

        elif format == EFileType.TXT:
            with open(file_path, m) as txtfile:
                if not file_exists:
                    self.writer.write(headers)
                if isinstance(data, list):
                    for item in data:
                        txtfile.write(f"{item}\n")
                elif isinstance(data, dict):
                    for key, value in data.items():
                        txtfile.write(f"{key}: {value}\n")
                else:
                    raise ValueError("Data must be a list or dictionary for TXT format.")
        elif format == EFileType.BIN:   
            with open(file_path, 'wb') as binfile:
                if isinstance(data, bytes):
                    binfile.write(data)
                elif isinstance(data, bytearray):
                    binfile.write(bytes(data))
                else:
                    raise ValueError("Data must be bytes or bytearray for BIN format.")
        else:
            raise ValueError(f"Unsupported file format: {self.format}")