# James Clarke
# 18/04/2019

# Node that represents a node object on disk

from ..utils.conversions import Conversions

from enum import Enum
import hashlib
from datetime import date

class Node:

    CHECKSUM_SHORT_SIZE = 5 # Number of characters for the short checksum

    class NodeType(Enum):
       relic=0          # Represents a file on disk
       collection=1     # Represents a directory of relics or sub-collections
       strata=2         # Represents a pointer to a collection root at a certian point in time

       
    def __init__(self):
        self.checksum=None   # Unique identifier for this node object
        self.type=None       # Describes what type of node this is

    # Generate a checksum for this node
    def checksum_me(self):
        raise NotImplementedError("This needs to be implemented by sub-classes")

    # Return the short version of the checksum
    def get_checksum_short(self):
        return self.checksum[:Node.CHECKSUM_SHORT_SIZE]

    # Generate a checksum based off file contents
    @staticmethod
    def generate_checksum(contents):
        return hashlib.sha256(Conversions.str_to_bytes(contents)).hexdigest()