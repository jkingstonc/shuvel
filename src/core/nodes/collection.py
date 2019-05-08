""" 

A collection represents a folder than contains sub collections or relics

"""

from .node import Node

import json
import datetime

class Collection(Node):


    def __init__(self,creation_date=datetime.datetime.now(),name="DEFAULT",checksums=[]):
        super().__init__()

        self._creation_date=creation_date   
        self._name=name                     
        # Contains array of relic/collection checksums
        self._checksums=checksums

    def __str__(self):
        return self._name
    
    # Set the checksum for this relic object
    def checksum_me(self):
        self._checksum=Node.generate_checksum(str(self._creation_date)+str(self._name)+str(self._checksums))

    def set_creation_date(self, creation_date=datetime.datetime.now()):
        self._creation_date=creation_date

    def set_name(self, name):
        self._name=name

    def set_checksums(self, checksums):
        self._checksums=checksums

    # Dump the relic contents into a single JSON object
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
       