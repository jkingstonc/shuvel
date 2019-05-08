"""

Helper class for traversing node trees from a root node.
Note: All traversal algorithms use an iterative approach so the boilerplate code should
be implemented manually. However, getting the depth of a node uses a recursive traversal
of each node individually which is extremely inefficent [When getting the depth of each node,
we currently use nested traversals which has complexity O(n^2)].

"""

from ..nodes.node import Node
from ..nodes.relic import Relic
from ..nodes.collection import Collection
from ..nodes.strata import Strata
from .load import Load

import queue 

class Traversal:

    # Returns the node that would be traversed next on a traversal of all nodes in a tree
    # Uses depth-first-traversal, using a modified queue implementation 
    @staticmethod
    def traverse_node(stack, archive_dir,using_checksum=False):
        # Pop the top item from stack
        node = stack.get()
        # Push all checksums to the stack if node is collection
        if type(node) is Collection:
            for checksum in node._checksums:
                next_node = Load.load_node(checksum, archive_dir,using_checksum)
                stack.put(next_node)
        # Return the node popped as the next node, and the stack
        return node, stack

    # Get the level of a node in a node tree
    # This uses a recursive depth-first-search
    # This implementation is currently very slow as for each node being traversed in
    # the default traversal implementation, this will be called if we want the depth
    # calling a further traversal
    @staticmethod
    def get_level_of_node(root, target, level, archive_dir,using_checksum=False):
        # If we found the target, return the level
        if root._name == target._name:
            return level
        # If the root is a collection, check level every child node
        if type(root) is Collection:
            for checksum in root._checksums:
                next_node = Load.load_node(checksum,archive_dir,using_checksum)
                # Traverse the next node
                result=Traversal.get_level_of_node(next_node,target,level+1,archive_dir,using_checksum)
                # If the result isn't 0 [we found the target at a level], return the level
                if result!=0:
                    return result
        # We haven't found the target
        return 0
	
