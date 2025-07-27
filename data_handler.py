import json
import csv
import os as os
import io
from PIL import Image
from EFileType import EFileType

class DataHandler():
    def __init__(self):
        self.format = EFileType.CSV
        self.default_save_path = "~/Measurement_Software/Experiments/Outputs/"        
        self.save_path = self.default_save_path
        self.auto_save = False
    def get_save_path(self):
        """
        Get the current folder where data is saved.
        
        Returns:
        str: The current save path.
        """
        return self.save_path
    
    def is_auto_saving_data_enabled(self):
        """
        Check if auto-saving of data is enabled.
        
        Returns:
        bool: True if auto-saving is enabled, False otherwise.
        """
        return self.auto_save
    
    def enable_auto_saving_data(self, save_path=None):
        """
        Enable the automatic saving of data to a specified path.
        
        Parameters:
        save_path (str): The path where data will be saved. If None, auto-saving is disabled.
        """
        self.auto_save = True
        
        if save_path is not None:
            self.save_path = save_path
        else:
            self.save_path = self.default_save_path
        
        print(f"Auto-saving enabled. Data will be saved to {self.save_path}")
            
    def disable_auto_saving_data(self):
        """
        Disable the automatic saving of data to a specified path.
        
        Parameters:
        save_path (str): The path where data will be saved.
        """
        self.auto_save = False
        print("Auto-saving disabled.")

    def remove_tmc_header(self, bytes):
        """Removes TMC header from image bytes"""
        #First byte is #, ignore
        size_count = 0 
        print(bytes[1])
        #size_count = int.from_bytes(bytes[1]
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
    #TODO Add update_file

    def read_file(self, file_path, format = None):
        """Reads file and returns data"""
        fmt = self.format
        if format is not None:  
            fmt = format
        file_path = file_path + format.value if not file_path.endswith(format.value) else file_path
        if fmt == EFileType.CSV:
            with open(file_path, mode='r') as csvfile:
                data = list(csv.reader(csvfile))
                for i in range(1, len(data)):
                    data[i] = [float(x) for x in data[i]]
                return data
        elif fmt == EFileType.JSON:
            with open(file_path, 'r') as jsonfile:
                return json.load(jsonfile)
        elif fmt == EFileType.TXT:
            with open(file_path, 'r') as txtfile:
                return txtfile.readlines()
        elif fmt == EFileType.BIN:  
            with open(file_path, 'rb') as binfile:
                return binfile.read()
        elif fmt == EFileType.PNG:
            return Image.open(file_path)

        else:
            raise ValueError(f"Unsupported file format: {self.format}")
        
    def write_to_file(self, file_name, data, file_type = None, headers = None):
        """Writes data to file
        params: file_path: str - path to file
                data: list or dict - data to write to file
                file_type: EFileType - type of file to write to, if None then uses default format
                headers: list - headers for file, if None then numerical headers are used. Only used if data is not a dictionary.
                If file already exists, headers are not written again."""
        file_path = file_name#self.default_save_path+file_name
        format = self.format
        if file_type is not None:
            format = file_type
        file_path = file_path + format.value if not file_path.endswith(format.value) else file_path
        file_exists = os.path.isfile(file_path)
        if file_exists:
            m = 'a'  
        else: 
            m = 'w'
            if headers is None:
                headers = range(0, len(data))

        #TODO Check data formatting possibilities

        if format == EFileType.CSV:
            with open(file_path, mode=m) as csvfile:
                if data is dict:
                    headers = list(data.keys())
                    data = list(data.values())
                elif data[0] is not list:
                    data = [data]
                self.writer = csv.writer(csvfile)
                if not file_exists:
                    self.writer.writerow(headers)
                self.writer.writerows(data)

        elif format == EFileType.JSON:
            already_in_file = {}
            data_dict = {}
            if(type(data) is list):
                for d in range(0,len(data)):
                    data_dict[headers[d]] = data[d]
            else:
                data_dict = data
            if file_exists:
                with open(file_path, 'r') as jsonfile:
                    already_in_file = json.load(jsonfile)
            data = {**already_in_file, **data_dict}
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
        elif format == EFileType.PNG:
            if isinstance(data, Image.Image):
                data.save(file_path)
            elif isinstance(data, bytes):
                image = Image.open(io.BytesIO(data))
                image.save(file_path)
            else:
                raise ValueError("Data must be an Image object or bytes for PNG format.")
        else:
            raise ValueError(f"Unsupported file format: {self.format}")