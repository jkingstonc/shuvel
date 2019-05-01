# James Clarke
# 18/04/2019

# Relic that represents a file on disk

from .node import Node

import json
from datetime import date

class Relic(Node):

    def __init__(self,creation_date=date.today(),name="DEFAULT",storage_contents=""):
        super().__init__()

        self._creation_date=creation_date               # The date this relic was created
        self._name=name                                 # Name associated with this relic
        self._storage_data_contents=storage_contents    # Contains the raw data that is described in the origin file to be written to disk
    def __str__(self):
        return "Checksum: "+str(self.get_checksum_short())+"..., Creation-Date: "+str(self._creation_date)+", Storage-Data-Contents: "+str(self._storage_data_contents)
    
    # Set the checksum for this relic object
    def checksum_me(self):
        self._checksum=Node.generate_checksum(str(self._creation_date)+str(self._name)+str(self._storage_data_contents))
    # Set the creation date for this relic object
    def set_creation_date(self, creation_date=date.today()):
        self._creation_date=creation_date
    # Set the name associated with this relic
    def set_name(self, name):
        self._name=name
    # Set the storage data contents for this relic object
    def set_storage_data_contents(self, contents):
        self._storage_data_contents=str(contents)
    # Dump the relic contents into a single string
    def get_string_dump(self):
        data={}
        data['checksum'] = str(self._checksum)
        data['type']=str(Node.NodeType.relic.value)
        data['name']=str(self._name)
        data['creation_date']=str(self._creation_date)
        data['content']=str(self._storage_data_contents)
        return json.dumps(data)



    