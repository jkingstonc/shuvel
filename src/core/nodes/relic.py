# James Clarke
# 18/04/2019

# Relic that represents a file on disk

from .node import Node

class Relic(Node):

    def __init__(self):
        super().__init__()
        self.file_type=None             # The file extension that this relic is associated with
        self.raw_data_contents=None     # The raw data as a string that this relic is storing
        self.raw_data_size=None         # Size of raw data in bytes

    def __str__(self):
        return "Checksum: "+self.checksum+", File-Type: "+self.file_type+", Raw-Data-Size: "+str(self.raw_data_size)+", Raw-Data: "+self.raw_data_contents

    def create(self):
        self.checksum=Node.generate_checksum(self.get_file_contents())

    # Generates a string containing all the file contents to be written
    def get_file_contents(self):
        return self.file_type+self.raw_data_contents+str(self.raw_data_size)

    # Sets the relic's file type
    def set_file_type(self, file_type):
        self.file_type=file_type

    # Sets the relic's raw data to be written to file
    def set_raw_data(self, raw_data_contents):
        self.raw_data_contents=raw_data_contents
        self.raw_data_size=len(self.raw_data_contents.encode('utf-8'))
