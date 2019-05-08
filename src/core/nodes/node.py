""" 

A node represents a template for relics, collections and stratas to inherit from.
Cannot be instantiated itself.

"""


from ..utils import conversions

import json
from enum import Enum
import hashlib
from datetime import date
import random

class Node:
    INFO_SEPERATOR="::"
    INFO_CONTENT_SEPERATOR="info_sep"
    CHECKSUM_SHORT_SIZE = 5 # Number of characters for the short checksum

    class NodeType(Enum):
       relic=0          # Represents a file on disk
       collection=1     # Represents a directory of relics or sub-collections
       strata=2         # Represents a pointer to a collection root at a certian point in time

       
    def __init__(self):
        self._checksum=None   # Unique identifier for this node object
        self._type=None       # Describes what type of node this is

    # Generate a checksum for this node
    def checksum_me(self):
        raise NotImplementedError("This needs to be implemented by sub-classes")

    # Generate a random checksum for this node (used for temp nodes)
    def checksum_me_rand(self):
        self._checksum=Node.generate_checksum(str(random.randint(0,999999999)))

    # Return the short version of the checksum
    def get_checksum_short(self):
        return Node.to_short_checksum(self._checksum)

    # Convert a standard checksum to the short version
    @staticmethod
    def to_short_checksum(checksum):
        return checksum[:Node.CHECKSUM_SHORT_SIZE]

    # Generate a checksum based off file contents
    @staticmethod
    def generate_checksum(contents):
        return hashlib.sha256(conversions.str_to_bytes(contents)).hexdigest()