# Helper class for traversing node trees

from ..nodes.node import Node
from ..nodes.relic import Relic
from ..nodes.collection import Collection
from ..nodes.strata import Strata

from .load import Load

import queue 
  

class Traversal:

    # Returns the node that would be traversed next on a traversal of all nodes in a tree
    @staticmethod
    def traverse_node(stack, archive_dir,using_checksum=False):
        # Pop the top item from stack
        node = stack.get()
        # Push all checksums to the stack
        if type(node) is Collection:
            for checksum in node._checksums:
                next_node = Load.load_node(checksum, archive_dir,using_checksum)
                stack.put(next_node)
        
        return node, stack

    # Get the level of a node in a node tree
    @staticmethod
    def get_level_of_node(root, target, level, archive_dir,using_checksum=False):
        # If we found the target, return the level
        if root._name == target._name:
            return level
        # If the root is a collection, check level every child node
        if type(root) is Collection:
            for checksum in root._checksums:
                next_node = Load.load_node(checksum,archive_dir,using_checksum)
                result=Traversal.get_level_of_node(next_node,target,level+1,archive_dir,using_checksum)
                if result!=0:
                    return result
        return 0
	
