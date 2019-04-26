# James Clarke
# 18/04/2019

# Collection that represents a directory of relics or sub-collections

from .node import Node

from datetime import date

class Collection(Node):

    CHECKSUM_SEPERATOR="?"

    def __init__(self):
        super().__init__()

        self._creation_date=None                # The date this relic was created
        self._name="DEFAULT"                    # Name associated with this collection
        self._relic_checksums=[]                # Contains array of relic checksums
    def __str__(self):
        return "Checksum: "+str(self.get_checksum_short())+"..., Creation-Date: "+str(self._creation_date)+", Relics: "+str(self._relic_checksums)
    
    # Set the checksum for this relic object
    def checksum_me(self):
        self._checksum=Node.generate_checksum(str(self._creation_date)+str(self._name)+str(self.get_relic_checksums_str()))
    # Set the creation date for this relic object
    def set_creation_date(self, creation_date=date.today()):
        self._creation_date=creation_date
    # Set the name associated with this relic
    def set_name(self, name):
        self._name=name
    # Set the array of relic checksums for this collection
    def set_relic_checksums(self, checksums):
        self._relic_checksums=checksums

    # Generate a string from the relic checksum array
    def get_relic_checksums_str(self):
        return "".join(checksum+Collection.CHECKSUM_SEPERATOR for checksum in self._relic_checksums)
    # Dump the relic contents into a single string
    def get_string_dump(self):
        return str(self._checksum)+Node.INFO_SEPERATOR+str(self._name)+Node.INFO_SEPERATOR+str(self._creation_date)+Node.INFO_SEPERATOR+Node.INFO_CONTENT_SEPERATOR+Node.INFO_SEPERATOR+self.get_relic_checksums_str()