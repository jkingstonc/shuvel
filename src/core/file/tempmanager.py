# Class to help with converting temporary files to archive files

import os

from ..nodes.node import Node
from ..nodes.relic import Relic
from ..nodes.collection import Collection
from ..nodes.strata import Strata

from .dump import Dump
from .load import Load

class TempManager:
    
    
    # Archive all temporary nodes that span from the specified root node
    @staticmethod
    def archive_temp(root_node, strata_name, strata_message, strata_dir, archive_dir, temp_dir):
        # Only archiving a single relic here, so no traversing of checksums is required
        if type(root_node) is Relic:
            root_node.checksum_me()
            Dump.dump_relic(root_node,archive_dir)
            s=Strata(name=strata_name,message=strata_message,root_node=root_node._checksum)
            s.checksum_me()
            Dump.dump_strata(s,strata_dir)



        # We need to modify every collection checksum contents to the new updated checksums
        elif type(root_node) is Collection:

            root_collection_checksum = TempManager.gen_collection_checksum(root_node, strata_name, strata_message, strata_dir, archive_dir, temp_dir)
            s=Strata(name=strata_name,message=strata_message,root_node=root_collection_checksum)
            s.checksum_me()
            Dump.dump_strata(s,strata_dir)
                    

        else:
            print("Cannot archive Strata in temp folder!")
        
    
    # Recursively return the checksum of an archived relic
    @staticmethod
    def gen_collection_checksum(root_node, strata_name, strata_message, strata_dir, archive_dir, temp_dir):
        collection_checksums = []

        # Loop over every checksum this collection points to
        for checksum in root_node._checksums:
            next_node = Load.load_node(checksum,temp_dir)

            if type(next_node) is Relic:
                next_node.checksum_me()
                Dump.dump_relic(next_node,archive_dir)
                # Add the new relic checksum to the new collection checksums
                collection_checksums.append(next_node._checksum)

            # Recursively generate checksums if the next node is a collection
            elif type(next_node) is Collection:
                collection_checksums.append(
                    TempManager.gen_collection_checksum(next_node, strata_name, strata_message, strata_dir, archive_dir, temp_dir)
                )
        new_collection = root_node
        new_collection.set_checksums(collection_checksums)
        new_collection.checksum_me()
        Dump.dump_collection(new_collection,archive_dir)

        return new_collection._checksum

    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_temp_traversal(path, archive_dir):
        checksums = os.listdir(archive_dir)
        nodes=[Load.load_node(checksum, archive_dir) for checksum in checksums]

        # First determine which checksums don't belong to any other
        root_nodes=[]
        for node in nodes:
            passed=True
            for test_node in nodes:
                # Check we aren't comparing the same nodes
                if test_node != node:
                    # Check if we are looking in a collection
                    if type(test_node) is Collection:
                        # If the node name is in the collection checksums, then it isn't a root node
                        if node._name in test_node._checksums:
                            # node isn't a root node
                            passed=False
            if passed:
                root_nodes.append(node)
        #print(", ".join(node._name for node in root_nodes))

        for node in root_nodes:
            TempManager.traverse_node(None,node,archive_dir,TempManager.display_nodes_hierarchy)

    # Recursively return the checksum of an archived relic
    @staticmethod
    def traverse_node(previous_node,root_node, archive_dir, node_function):
        node_function(root_node,previous_node)
        # Loop over every checksum this collection points to
        for checksum in root_node._checksums:
            next_node = Load.load_node(checksum,archive_dir)
            
            # Recursively generate checksums if the next node is a collection
            if type(next_node) is Collection:
                TempManager.traverse_node(root_node,next_node, archive_dir, node_function)
            else:
                node_function(next_node,root_node)

    # Format the display of a node
    @staticmethod
    def display_nodes_hierarchy(node,root_node=None):
        prefix=""
        if type(node) is Relic:
            prefix="r: "

        elif type(node) is Collection:
            prefix="c: "

        if root_node != None:
            print(prefix+root_node._name+" -> "+node._name)
        else:
            print(prefix+node._name)
        


