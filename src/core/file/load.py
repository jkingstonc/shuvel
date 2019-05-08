"""

Class for loading nodes from disk.

"""

from ..file.fileio import FileIO
from ..nodes.node import Node
from ..nodes.relic import Relic
from ..nodes.collection import Collection
from ..nodes.strata import Strata

import json

class Load:

    # Load a node from disk to object
    @staticmethod
    def load_node(checksum,archive_dir,using_checksum=False):
        # If we are loading via a checksum, we need the short version of it
        if using_checksum:
            checksum=Node.to_short_checksum(checksum)
        data = FileIO.read_string_full(archive_dir+checksum)
        if data == None:
            return None
        data = json.loads(data)
        if data['type']==str(Node.NodeType.relic.value):
            r=Relic(data['creation_date'],data['name'],data['content'])
            r.checksum_me()
            return r
        elif data['type']==str(Node.NodeType.collection.value):
            c=Collection(data['creation_date'],data['name'],data['content'])
            c.checksum_me()
            return c
        elif data['type']==str(Node.NodeType.strata.value):
            s=Strata(creation_date=data['creation_date'],name=data['name'],message=data['message'],root_node=data['content'])
            s.checksum_me()
            return s
        else:
            return None