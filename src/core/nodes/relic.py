""" 

A relic represents a file on disk that contains any type of data.

"""

from .node import Node

import json
import datetime

class Relic(Node):

    def __init__(self,creation_date=datetime.datetime.now(),name="DEFAULT",storage_contents=""):
        super().__init__()

        self._creation_date=creation_date               
        self._name=name                             
        # Contains the raw string that this relic holds
        # Note: this can be extremely large and may beed to be implemented in a different way becuase of that
        self._storage_data_contents=storage_contents

    def __str__(self):
        return self._name
    
    # Passing all the relic member variables into the node checksum function
    def checksum_me(self):
        self._checksum=Node.generate_checksum(str(self._creation_date)+str(self._name)+str(self._storage_data_contents))

    def set_creation_date(self, creation_date=datetime.datetime.now()):
        self._creation_date=creation_date

    def set_name(self, name):
        self._name=name

    def set_storage_data_contents(self, contents):
        self._storage_data_contents=str(contents)
    
    # Dump the relic contents into a single JSON object
    # Note: type is required for loading objects, as load only has 1 load function for all nodes
    def get_string_dump(self):
        data={}
        data['checksum'] = str(self._checksum)
        data['type']=str(Node.NodeType.relic.value)
        data['name']=str(self._name)
        data['creation_date']=str(self._creation_date)
        data['content']=str(self._storage_data_contents)
        return json.dumps(data)



    