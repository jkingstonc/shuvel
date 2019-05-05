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

    @staticmethod
    def traverse_nodes(path, archive_dir):
        checksums = os.listdir(archive_dir)
        nodes=[Load.load_node(checksum, archive_dir) for checksum in checksums]

        # First determine which checksums don't belong to any other
        root_checksums=[]
        

        


