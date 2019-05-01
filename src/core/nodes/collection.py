# James Clarke
# 18/04/2019

# Collection that represents a directory of relics or sub-collections

from .node import Node

import json
from datetime import date

class Collection(Node):

    CHECKSUM_SEPERATOR="?"

    def __init__(self,creation_date=date.today(),name="DEFAULT",checksums=[]):
        super().__init__()

        self._creation_date=creation_date   # The date this relic was created
        self._name=name                     # Name associated with this collection
        self._checksums=checksums           # Contains array of relic checksums
    def __str__(self):
        return "Checksum: "+str(self.get_checksum_short())+"..., Creation-Date: "+str(self._creation_date)+", Relics: "+str(self._checksums)
    
    # Set the checksum for this relic object
    def checksum_me(self):
        self._checksum=Node.generate_checksum(str(self._creation_date)+str(self._name)+str(self.get_checksums_str()))
    # Set the creation date for this relic object
    def set_creation_date(self, creation_date=date.today()):
        self._creation_date=creation_date
    # Set the name associated with this relic
    def set_name(self, name):
        self._name=name
    # Set the array of relic checksums for this collection
    def set_checksums(self, checksums):
        self._checksums=checksums
    # Dump the relic contents into a single string
    def get_string_dump(self):
        data={}
        data['checksum'] = str(self._checksum)
        data['type']=str(Node.NodeType.collection.value)
        data['name']=str(self._name)
        data['creation_date']=str(self._creation_date)
        data['content']=[]
        for checksum in self._checksums:
            data['content'].append(checksum)
        return json.dumps(data)
       