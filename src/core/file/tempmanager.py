# Class to help with converting temporary files to archive files

import sys, os, shutil
sys.path.append("...") # Adds higher directory to python modules path.

from core.nodes.node import Node
from core.nodes.relic import Relic
from core.nodes.collection import Collection
from core.nodes.strata import Strata

from core.file.dump import Dump
from core.file.load import Load
from core.file.traversal import Traversal

from out.log import Log

import queue 

class TempManager:
    
    # Completely clear the temp directory
    @staticmethod
    def clear_temp(temp_dir):
        for the_file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        TempManager.gen_root_temp("root",temp_dir)

    @staticmethod
    def gen_root_temp(name,temp_dir):
        root = Collection(name=name)
        root.checksum_me()
        return Dump.dump_temp_collection(root,temp_dir)
         
    
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
        # Dump the newly checksumed collection, and return its checksum
        new_collection = root_node
        new_collection.set_checksums(collection_checksums)
        new_collection.checksum_me()
        Dump.dump_collection(new_collection,archive_dir)

        return new_collection._checksum

    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_temp_files(archive_dir):
        
        # Get the root node of a project
        root = Load.load_node("root", archive_dir)
        if root != None:
            Log.status_message("Live Nodes:\n-----------")
            stack = queue.LifoQueue()
            stack.put(root)

            while not stack.empty():
                next_node, stack =Traversal.traverse_node(stack,archive_dir)
                depth=Traversal.get_level_of_node(root,next_node,0,archive_dir)
                Log.status_content(''.join(" - " for x in range(0,depth))+" "+str(next_node))
        else:
            Log.status_warning("Project empty!")

    # Move a node from one collection to another
    @staticmethod
    def move_node_to_collection(source, target, archive_temp):
        if source._name not in target._checksums:
            target._checksums.append(source._name)
            target.checksum_me()
            Dump.dump_temp_relic(target,archive_temp)

            root = Load.load_node("root", archive_temp)
            if root != None:
                stack = queue.LifoQueue()
                stack.put(root)

                while not stack.empty():
                    next_node, stack =Traversal.traverse_node(stack,archive_temp)
                    if type(next_node) is Collection:
                        # If the node is in the collection, and this collection ISN'T the target, remove it
                        if next_node._name != target._name and source._name in next_node._checksums:
                            next_node._checksums.remove(source._name)
                            next_node.checksum_me()
                            Dump.dump_temp_relic(next_node,archive_temp)
                            break

