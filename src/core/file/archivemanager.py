# Helper class for performing operations related to the archived nodees

from .dump import Dump
from .load import Load
from .traversal import Traversal
from ..nodes.node import Node

import os, queue


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
            print("No archives!")
    
    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_stratas(strata_dir):
        
        stratas = [Load.load_node(checksum,strata_dir) for checksum in os.listdir(strata_dir)]
        if len(stratas) > 0:
            print("Stratas:")
            for strata in stratas:
                print("checksum: "+strata._checksum)
                print("-> name: "+strata._name)
                print("-> name: "+strata._message)
        else:
            print("No stratas!")

    @staticmethod
    def get_full_checksum(checksum,archive_dir):
        files=os.listdir(archive_dir)
        for f in files:
            if f in checksum or checksum in f:
                return f

        return checksum