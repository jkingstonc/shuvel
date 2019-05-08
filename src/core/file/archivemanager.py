"""

Helper class for performing operations related to the archived nodes and stratas.

"""
import sys, os, queue, datetime
sys.path.append("...") # Adds higher directory to python modules path.

from core.file.dump import Dump
from core.file.load import Load
from core.file.traversal import Traversal
from core.nodes.node import Node
from core.nodes.relic import Relic
from core.nodes.collection import Collection
from core.nodes.strata import Strata
from core.file.tempmanager import TempManager
from core.file.fileio import FileIO
from out.log import Log

class ArchiveManager:
    
    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_archived_files_from_strata(strata, archive_dir):
        Log.status_message("Nodes in archive '"+strata._name+"' ["+strata._checksum+"]:\n--------------------------------------------------------------------------------------------")
        # Get the root node of a project
        root = Load.load_node(strata._root_node_checksum, archive_dir,using_checksum=True)
        if root != None:
            # Traverse over all files
            stack = queue.LifoQueue()
            stack.put(root)
            while not stack.empty():
                next_node, stack =Traversal.traverse_node(stack,archive_dir,using_checksum=True)
                depth=Traversal.get_level_of_node(root,next_node,0,archive_dir,using_checksum=True)
                Log.status_content(''.join(" - " for x in range(0,depth))+" "+str(next_node))
            return True
        else:
            Log.status_error("No archives!")
            return False
    
    # Return a node that is archived via a given strata located using a given name
    @staticmethod
    def get_node_from_strata(strata, node_name, archive_dir):
        # Load the root node that this strata points to
        root = Load.load_node(strata._root_node_checksum, archive_dir,using_checksum=True)
        if root != None:
            # Traverse over the root archive
            stack = queue.LifoQueue()
            stack.put(root)
            while not stack.empty():
                next_node, stack =Traversal.traverse_node(stack,archive_dir,using_checksum=True)
                # Check if the next node is the one we're trying to find
                if next_node._name == node_name:
                    return next_node
            Log.status_warning("Warning: No file named '"+node_name+"' in specified archive!")
            return None
        else:
            Log.status_error("Error: Archive doesn't seem to exist :/!")
            return None

    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_stratas(strata_dir): 
        # Load up all stratas found in the strata_dir
        stratas = [Load.load_node(checksum,strata_dir) for checksum in os.listdir(strata_dir)]
        # Sort the stratas by creation date
        stratas = sorted(
            stratas,
            key=lambda x: x._creation_date, reverse=True
        )
        if len(stratas) > 0:
            Log.status_message("Stratas:\n--------")
            for strata in stratas:
                Log.status_content("checksum: "+strata._checksum)
                Log.status_content("-> date:    "+strata._creation_date)
                Log.status_content("-> name:    "+strata._name)
                Log.status_content("-> message: "+strata._message)
                Log.status_content("\n")
            return True
        else:
            Log.status_warning("No archives!")
            return False

    # Move an archived strata to the temp dir
    @staticmethod
    def excavate_strata(strata, archive_dir, archive_temp_dir):
        # Get the root node of the strata
        root_node = Load.load_node(strata._root_node_checksum, archive_dir, using_checksum=True) 
        # Only archiving a single relic here, so no traversing of checksums is required
        if type(root_node) is Relic:
            root_node.checksum_me()
            Dump.dump_temp_relic(root_node,archive_temp_dir)
            # Move the node to the root collection after everything is finished
            TempManager.move_node_to_collection(root_node,Load.load_node("root",archive_temp_dir),archive_temp_dir)
            return True
        # We need to modify every collection checksum contents to the new updated checksums
        elif type(root_node) is Collection:
            root_collection_name = ArchiveManager.gen_collection_name(root_node, archive_dir, archive_temp_dir)
            # If the root node isn't root, we need to move it to root
            if root_node._name != "root":
                # Move the node to the root collection after everything is finished
                TempManager.move_node_to_collection(Load.load_node(root_collection_name,archive_temp_dir,using_checksum=False),Load.load_node("root",archive_temp_dir),archive_temp_dir)
            return True
        else:
            Log.status_error("Error: Cannot archive node specified in temp folder! [not relic or collection]")
            return False

    # Recursively return the name of a node and archive it
    # [Used for excavating archived nodes to the temp folder where we need to convert a checksum to a name]
    @staticmethod
    def gen_collection_name(root_node,archive_dir, temp_dir):
        # List containing all new names to put in the root_node checksum list
        collection_checksums = []
        # Loop over every checksum this collection points to
        for checksum in root_node._checksums:
            next_node = Load.load_node(checksum,archive_dir,using_checksum=True)
            # If the next node is a relic, dump it in the temp archives
            if type(next_node) is Relic:
                next_node.checksum_me()
                Dump.dump_temp_relic(next_node,temp_dir)
                # Add the new relic name to the new collection checksum list
                collection_checksums.append(next_node._name)

            # Recursively generate names if the next node is a collection
            elif type(next_node) is Collection:
                # Append the new checksum list with the generated name of this collection
                collection_checksums.append(
                    ArchiveManager.gen_collection_name(next_node, archive_dir, temp_dir)
                )
        # Dump the newly checksumed collection, and return its name
        new_collection = root_node
        new_collection.set_checksums(collection_checksums)
        new_collection.checksum_me()
        Dump.dump_temp_collection(new_collection,temp_dir)
        return new_collection._name

    # Get the full checksum from a smaller checksum
    @staticmethod
    def get_full_checksum(checksum,archive_dir):
        found=False
        files=os.listdir(archive_dir)
        for f in files:
            if f in checksum or checksum in f:
                return f
        return None