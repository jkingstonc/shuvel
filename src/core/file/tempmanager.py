"""

Helper class for managing the temporary archive folder.
Deals with node moving, deleting, archiving, traversing etc.
Note: Alot of this code is highly inefficent and should be rewritten.

"""

import sys, os, shutil,queue 
sys.path.append("...")

from core.nodes.node import Node
from core.nodes.relic import Relic
from core.nodes.collection import Collection
from core.nodes.strata import Strata
from core.file.dump import Dump
from core.file.load import Load
from core.file.traversal import Traversal
from core.file.fileio import FileIO
from out.log import Log

class TempManager:
    
    # Generate a root collection in the temp folder
    @staticmethod
    def gen_root_temp(name,temp_dir):
        root = Collection(name=name)
        root.checksum_me()
        Dump.dump_temp_collection(root,temp_dir)
        return True
         
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
            return True

        # We need to modify every collection checksum contents to the new updated checksums
        elif type(root_node) is Collection:
            root_collection_checksum = TempManager.gen_collection_checksum(root_node, strata_name, strata_message, strata_dir, archive_dir, temp_dir)
            s=Strata(name=strata_name,message=strata_message,root_node=root_collection_checksum)
            s.checksum_me()
            Dump.dump_strata(s,strata_dir)
            return True
                    
        else:
            Log.status_error("Error: Cannot archive node specified in temp folder! [not relic or collection]")
            return False
        
    # Recursively return the checksum of a node and archive it
    @staticmethod
    def gen_collection_checksum(root_node, strata_name, strata_message, strata_dir, archive_dir, temp_dir):
        # List containing all new checksums to put in the root_node checksum list
        collection_checksums = []
        # Loop over every checksum this collection points to
        for checksum in root_node._checksums:
            next_node = Load.load_node(checksum,temp_dir)
            # If the next node is a relic, dump it in the archives
            if type(next_node) is Relic:
                next_node.checksum_me()
                Dump.dump_relic(next_node,archive_dir)
                # Add the new relic checksum to the new collection checksums
                collection_checksums.append(next_node._checksum)

            # Recursively generate checksums if the next node in the root_node checksums is a collection
            elif type(next_node) is Collection:
                # Append the new checksum list with the generated checksum of this collection
                collection_checksums.append(
                    TempManager.gen_collection_checksum(next_node, strata_name, strata_message, strata_dir, archive_dir, temp_dir)
                )
            elif next_node is None:
                Log.status_error("Error: Checksum points to no node!")
        # Dump the newly checksumed collection, and return its checksum
        new_collection = root_node
        new_collection.set_checksums(collection_checksums)
        new_collection.checksum_me()
        Dump.dump_collection(new_collection,archive_dir)

        return new_collection._checksum

    # Remove a node from the temp dir
    @staticmethod
    def del_node(node,temp_dir):
        # Get the root node of a project
        root = Load.load_node("root", temp_dir)
        if root != None:
            if node != None:
                # Traverse over all temp files to remove occurances of the node in collections
                stack = queue.LifoQueue()
                stack.put(root)
                while not stack.empty():
                    next_node, stack =Traversal.traverse_node(stack,temp_dir)
                    # If the next node is a collection, check if the node name occurs in there
                    if type(next_node) is Collection:
                        if node._name in next_node._checksums:
                            # Remove the name and re-dump the collection
                            next_node._checksums.remove(node._name)
                            next_node.checksum_me()
                            Dump.dump_temp_collection(next_node,temp_dir)
                # Delete the node
                FileIO.delete_file(temp_dir+node._name)
                return True
            else:
                Log.status_error("Error: Node doesn't exist!")
                return False
        else:
            Log.status_error("Error: Root temp file doesn't exist!")
            return False

    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_temp_files(archive_dir):
        # Get the root node of a project
        root = Load.load_node("root", archive_dir)
        if root != None:
            Log.status_message("Live Nodes:\n-----------")
            # Traverse over all temp files
            stack = queue.LifoQueue()
            stack.put(root)

            while not stack.empty():
                # Get the next node, and the depth of that node
                next_node, stack =Traversal.traverse_node(stack,archive_dir)
                depth=Traversal.get_level_of_node(root,next_node,0,archive_dir)
                Log.status_content(''.join(" - " for x in range(0,depth))+" "+str(next_node))
            return True
        else:
            Log.status_error("Error: Root temp file doesn't exist!")
            return False

    # Move a node from one collection to another
    @staticmethod
    def move_node_to_collection(source, target, archive_temp):
        if type(target) != Collection:
            Log.status_error("Error: Cannot move into non collection!")
            return False
        # First ensure the source isn't already in the target
        if source._name not in target._checksums:
            # Add the target to the source
            target._checksums.append(source._name)
            target.checksum_me()
            Dump.dump_temp_relic(target,archive_temp)
            # Now remove any other occurance of target from other collections
            root = Load.load_node("root", archive_temp)
            if root != None:
                stack = queue.LifoQueue()
                stack.put(root)
                while not stack.empty():
                    next_node, stack =Traversal.traverse_node(stack,archive_temp)
                    if type(next_node) is Collection:
                        # If the node is in the collection, and this collection isn't the target, remove it
                        if next_node._name != target._name and source._name in next_node._checksums:
                            next_node._checksums.remove(source._name)
                            next_node.checksum_me()
                            Dump.dump_temp_relic(next_node,archive_temp)
                            # We found the collection containing the source and removed it
                return True
            else:
                Log.status_error("Error: Root temp file doesn't exist!")
            # We didn't find an occurance of source, so it couldn't be moved
            return False
            # If we can't find the root file, then an error has occured