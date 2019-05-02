# James Clarke
# 18/04/2019

# Strata that represents a pointer to a collection root at a certian point in time

from .node import Node

import json
from datetime import date

class Strata(Node):

    def __init__(self, creation_date=date.today(), name="DEFAULT",message="DEFAULT",root_node=None):
        super().__init__()

        self._creation_date=creation_date                   # The date this relic was created
        self._name=name                                     # Name associated with this strata
        self._message=message                               # Message accociated with this strata
        self._root_node_checksum=root_node                  # Contains checksum for the root node this strata is pointing to
    def __str__(self):
        return "Checksum: "+str(self.get_checksum_short())+"..., Creation-Date: "+str(self._creation_date)+", Root Collection: "+str(self._root_node_checksum)
    
    # Set the checksum for this relic object
    def checksum_me(self):
        self._checksum=Node.generate_checksum(str(self._creation_date)+str(self._name)+str(self._message)+self._root_node_checksum)
    # Set the creation date for this relic object
    def set_creation_date(self, creation_date=date.today()):
        self._creation_date=creation_date
    # Set the name associated with this relic
    def set_name(self, name):
        self._name=name
    # Set the message associated with this relic
    def set_message(self, message):
        self._message=name
    # Set the root collection checksum for this strata
    def set_root_node_checksum(self, checksum):
        self._root_node_checksum=checksum

    # Dump the relic contents into a single string
    def get_string_dump(self):
        data={}
        data['checksum'] = str(self._checksum)
        data['type']=str(Node.NodeType.relic.value)
        data['name']=str(self._name)
        data['message']=str(self._message)
        data['creation_date']=str(self._creation_date)
        data['content']=str(self._root_node_checksum)
        return json.dumps(data)