""" 

A strata represents a pointer to a collection root at a certian point in time [points to an archive].

"""

from .node import Node

import json
import datetime

class Strata(Node):

    def __init__(self, creation_date=datetime.datetime.now(), name="DEFAULT",message="DEFAULT",root_node=None):
        super().__init__()
        self._creation_date=creation_date                   
        self._name=name                                     
        self._message=message             
        # Contains checksum for the archive node that this strata is pointing to                  
        self._root_node_checksum=root_node
        
    def __str__(self):
        return self._name
    
    # Passing all the strata member variables into the node checksum function
    def checksum_me(self):
        self._checksum=Node.generate_checksum(str(self._creation_date)+str(self._name)+str(self._message)+self._root_node_checksum)

    def set_creation_date(self, creation_date=datetime.datetime.now()):
        self._creation_date=creation_date

    def set_name(self, name):
        self._name=name

    def set_message(self, message):
        self._message=name

    def set_root_node_checksum(self, checksum):
        self._root_node_checksum=checksum

    # Dump the relic contents into a single JSON object
    # Note: type is required for loading objects, as load only has 1 load function for all nodes
    def get_string_dump(self):
        data={}
        data['checksum'] = str(self._checksum)
        data['type']=str(Node.NodeType.strata.value)
        data['name']=str(self._name)
        data['message']=str(self._message)
        data['creation_date']=str(self._creation_date)
        data['content']=str(self._root_node_checksum)
        return json.dumps(data)