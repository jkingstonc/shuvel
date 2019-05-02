# Class to help with converting temporary files to archive files

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
            pass
        else:
            print("Cannot archive Strata in temp folder!")
        


