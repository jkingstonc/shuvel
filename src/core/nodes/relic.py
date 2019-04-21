# James Clarke
# 18/04/2019

# Relic that represents a file on disk

from .node import Node

from datetime import date

class Relic(Node):

    def __init__(self):
        super().__init__()

        self.origin_directory=None        # The directory that this relic lives in
        self.origin_file=None             # The file that this relic is associated with

        self.creation_date=None   # The date this relic was created

        self.origin_data_contents="None"  # Contains the raw data that is described in the origin file to be written to disk

    def __str__(self):
        return "Checksum: "+str(self.get_checksum_short())+"..., Origin-Directory: "+str(self.origin_file)+", Origin-File: "+str(self.origin_data_contents)+", Creation-Date: "+str(self.creation_date)+", Origin-Data-Contents: "+str(self.origin_data_contents)
    
    def checksum_me(self):
        self.checksum=Node.generate_checksum(str(self.origin_directory)+str(self.origin_file)+str(self.creation_date)+str(self.origin_data_contents))


    def set_origin_directory(self, origin_directory):
        self.origin_directory=origin_directory
    def set_origin_file(self, origin_file):
        self.origin_file=origin_file
    def set_creation_date(self, creation_date=date.today()):
        self.creation_date=creation_date
    def set_origin_data_contents(self, contents):
        self.origin_data_contents=str(contents)