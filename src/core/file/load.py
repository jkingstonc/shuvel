# James Clarke
# 02/05/2019

# All verification is done before any of these functions are called

from ..file.fileio import FileIO
from ..nodes.node import Node
from ..nodes.relic import Relic
from ..nodes.collection import Collection
from ..nodes.strata import Strata

import json

class Load:

    # Load a node from disk to object
    @staticmethod
    def load_node(checksum,archive_dir):
        data = FileIO.read_string_full(archive_dir+checksum)
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
            s=Strata(data['creation_date'],data['name'],data['content'])
            s.checksum_me()
            return s
        else:
            return None

    # # Load a relic from disk to an object
    # @staticmethod
    # def load_relic(checksum,archive_dir):
    #     data = FileIO.read_string_full(archive_dir+checksum)
    #     data = json.loads(data)
    #     r=Relic(data['creation_date'],data['name'],data['content'])
    #     return r

    # # Load a temporary relic from disk to an object
    # @staticmethod
    # def load_temp_relic(name,archive_dir):
    #     data = FileIO.read_string_full(archive_dir+name)
    #     data = json.loads(data)
    #     r=Relic(data['creation_date'],data['name'],data['content'])
    #     return r

    # # Load a collection from disk to an object
    # @staticmethod
    # def load_collection(checksum,archive_dir):
    #     data = FileIO.read_string_full(archive_dir+checksum)
    #     data = json.loads(data)
    #     r=Collection(data['creation_date'],data['name'],data['content'])
    #     return r

    # # Load a temporary collection from disk to an object
    # @staticmethod
    # def load_temp_collection(name,archive_dir):
    #     data = FileIO.read_string_full(archive_dir+name)
    #     data = json.loads(data)
    #     r=Collection(data['creation_date'],data['name'],data['content'])
    #     return r

    # # Load a strata object from disk into an object
    # @staticmethod
    # def load_strata(chekcksum,archive_dir):
    #     data = FileIO.read_string_full(archive_dir+checksum)
    #     data = json.loads(data)
    #     r=Strata(data['creation_date'],data['name'],data['content'])
    #     return r

