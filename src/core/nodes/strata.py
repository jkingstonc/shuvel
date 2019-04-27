# James Clarke
# 18/04/2019

# Strata that represents a pointer to a collection root at a certian point in time

from .node import Node
from datetime import date

class Strata(Node):

    def __init__(self):
        super().__init__()

        self._creation_date=None                # The date this relic was created
        self._name="DEFAULT"                    # Name associated with this collection
        self._root_collection_checksum=None              # Contains checksum for the root collection this strata is pointing to
    def __str__(self):
        return "Checksum: "+str(self.get_checksum_short())+"..., Creation-Date: "+str(self._creation_date)+", Root Collection: "+str(self._root_collection_checksum)
    
    # Set the checksum for this relic object
    def checksum_me(self):
        self._checksum=Node.generate_checksum(str(self._creation_date)+str(self._name)+self._root_collection_checksum)
    # Set the creation date for this relic object
    def set_creation_date(self, creation_date=date.today()):
        self._creation_date=creation_date
    # Set the name associated with this relic
    def set_name(self, name):
        self._name=name
    # Set the root collection checksum for this strata
    def set_root_collection_checksum(self, checksum):
        self._root_collection_checksum=checksum

    # Dump the relic contents into a single string
    def get_string_dump(self):
        return str(self._checksum)+Node.INFO_SEPERATOR+str(Node.NodeType.strata)+Node.INFO_SEPERATOR+str(self._name)+Node.INFO_SEPERATOR+str(self._creation_date)+Node.INFO_SEPERATOR+Node.INFO_CONTENT_SEPERATOR+Node.INFO_SEPERATOR+Node.to_short_checksum(self._root_collection_checksum)