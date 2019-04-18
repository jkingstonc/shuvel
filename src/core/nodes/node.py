# James Clarke
# 18/04/2019

# Node that represents a node object on disk

from enum import Enum

class Node:
    class NodeType(Enum):
       relic=0          # Represents a file on disk
       collection=1     # Represents a directory of relics or sub-collections
       strata=2         # Represents a pointer to a collection root at a certian point in time

       
    def __init__(self):
        self.checksum=None  # Unique identifier for this node object

    # Generate a checksum based off file contents
    @staticmethod
    def generate_checksum(file_contents):
        pass