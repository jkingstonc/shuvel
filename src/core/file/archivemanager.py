# Helper class for performing operations related to the archived nodees

from .dump import Dump
from .load import Load

import os


class ArchiveManager:
    
    
    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_archived_files_from_strata(strata, archive_dir, strata_dir):

        # Get the root node of a project
        root = Load.load_node(strata._root_node_checksum, archive_dir)
        if root != None:
            stack = queue.LifoQueue()
            stack.put(root)

            while not stack.empty():
                next_node, stack =Traversal.traverse_node(stack,archive_dir)
                depth=Traversal.get_level_of_node(root,next_node,0,archive_dir)
                print(''.join(" - " for x in range(0,depth))+" "+str(next_node))
        else:
            print("No archives!")
    
    # Display a visual representation of a traversal of the temp directory
    @staticmethod
    def display_stratas(strata_dir):
        print("Stratas:")
        stratas = [Load.load_node(checksum,strata_dir) for checksum in os.listdir(strata_dir)]
        for strata in stratas:
            print("checksum: "+strata._checksum)
            print("-> name: "+strata._name)
            print("-> name: "+strata._message)