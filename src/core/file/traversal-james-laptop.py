# Helper class for traversing node trees

from ..nodes.node import Node
from ..nodes.relic import Relic
from ..nodes.collection import Collection
from ..nodes.strata import Strata

from .load import Load

class Traversal:
    
    @staticmethod
    def test(archive_dir):
        previous_node= Load.load_node("root",archive_dir)
        previous_collection=None

        while True:
            previous_node,previous_collection=Traversal.traverse_node(previous_node,previous_collection,archive_dir)
            input(">")


    # Returns the node that would be traversed next on a traversal of all nodes in a tree
    @staticmethod
    def traverse_node(previous_node,previous_collection,archive_dir):
        # Loop over every checksum this collection points to
        if type(previous_node) is Collection:
            # Get the first node in the checksum list of the previous node (which is a collection)
            next_node = Load.load_node(previous_node._checksums[0],archive_dir)
            return next_node, previous_node

        # The previous node is a relic so we need to return the next relic in the previous collection
        elif type(previous_node) is Relic:
            counter=0
            while True:
                next_node = Load.load_node(previous_collection._checksums[counter],archive_dir)
                if next_node == previous_collection:
                    if counter < len(previous_collection._checksums):
                        next_node = Load.load_node(previous_collection._checksums[counter+1],archive_dir)
                        return next_node, previous_collection
                    else:
                        # We have reached the last relic in the collection
                        # ... Not sure what to do here
                        return None, None
                else:
                    counter+=1
