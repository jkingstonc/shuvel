# Helper class for performing operations related to the archived nodees

import sys
sys.path.append("...") # Adds higher directory to python modules path.

from core.file.dump import Dump
from core.file.load import Load
from core.file.traversal import Traversal
from core.nodes.node import Node
from core.nodes.relic import Relic
from core.nodes.collection import Collection
from core.nodes.strata import Strata
from core.file.tempmanager import TempManager

from out.log import Log

import os, queue, datetime


class ArchiveManager:
    
    
    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_archived_files_from_strata(strata, archive_dir):
        # Get the root node of a project
        root = Load.load_node(strata._root_node_checksum, archive_dir,using_checksum=True)
        if root != None:
            stack = queue.LifoQueue()
            stack.put(root)

            while not stack.empty():
                next_node, stack =Traversal.traverse_node(stack,archive_dir,using_checksum=True)
                depth=Traversal.get_level_of_node(root,next_node,0,archive_dir,using_checksum=True)
                print(''.join(" - " for x in range(0,depth))+" "+str(next_node))
        else:
            Log.status_error("No archives!")
    
    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_stratas(strata_dir):
        
        stratas = [Load.load_node(checksum,strata_dir) for checksum in os.listdir(strata_dir)]

        stratas = sorted(
            stratas,
            key=lambda x: x._creation_date, reverse=True
            # key=lambda x: datetime.strptime(x['Created'], '%m/%d/%y %H:%M'), reverse=True
        )
        
        if len(stratas) > 0:
            Log.status_message("Stratas:\n--------")
            for strata in stratas:
                Log.status_content("checksum: "+strata._checksum)
                Log.status_content("-> date:    "+strata._creation_date)
                Log.status_content("-> name:    "+strata._name)
                Log.status_content("-> message: "+strata._message)
                Log.status_content("\n")
        else:
            Log.status_warning("No stratas!")

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


        # We need to modify every collection checksum contents to the new updated checksums
        elif type(root_node) is Collection:

            root_collection_name = ArchiveManager.gen_collection_name(root_node, archive_dir, archive_temp_dir)
            
            # If the root node isn't root, we need to move it to root
            if root_node._name != "root":
                # Move the node to the root collection after everything is finished
                TempManager.move_node_to_collection(Load.load_node(root_collection_name,archive_temp_dir,using_checksum=False),Load.load_node("root",archive_temp_dir),archive_temp_dir)

    # Recursively return the checksum of an archived relic
    @staticmethod
    def gen_collection_name(root_node,archive_dir, temp_dir):
        collection_checksums = []

        # Loop over every checksum this collection points to
        for checksum in root_node._checksums:
            next_node = Load.load_node(checksum,archive_dir,using_checksum=True)

            if type(next_node) is Relic:
                next_node.checksum_me()
                Dump.dump_temp_relic(next_node,temp_dir)
                # Add the new relic checksum to the new collection checksums
                collection_checksums.append(next_node._name)

            # Recursively generate checksums if the next node is a collection
            elif type(next_node) is Collection:
                collection_checksums.append(
                    ArchiveManager.gen_collection_name(next_node, archive_dir, temp_dir)
                )
        # Dump the newly checksumed collection, and return its name
        new_collection = root_node
        new_collection.set_checksums(collection_checksums)
        new_collection.checksum_me()
        Dump.dump_temp_collection(new_collection,temp_dir)

        return new_collection._name


    @staticmethod
    def get_full_checksum(checksum,archive_dir):
        files=os.listdir(archive_dir)
        for f in files:
            if f in checksum or checksum in f:
                return f

        return checksum