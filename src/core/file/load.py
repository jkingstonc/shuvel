# James Clarke
# 02/05/2019

# All verification is done before any of these functions are called

from ..file.fileio import FileIO
from ..nodes.relic import Relic
from ..nodes.collection import Collection
from ..nodes.strata import Strata

import json

class Load:

    
    # Load a relic from disk to an object
    @staticmethod
    def load_relic(checksum,archive_dir):
        data = FileIO.read_string_full(archive_dir+checksum)
        data = json.loads(data)
        r=Relic(data['creation_date'],data['name'],data['content'])
        return r

    # Load a temporary relic from disk to an object
    @staticmethod
    def load_temp_relic(name,archive_dir):
        data = FileIO.read_string_full(archive_dir+name)
        data = json.loads(data)
        r=Relic(data['creation_date'],data['name'],data['content'])
        return r

    # Load a collection from disk to an object
    @staticmethod
    def load_collection(checksum,archive_dir):
        data = FileIO.read_string_full(archive_dir+checksum)
        data = json.loads(data)
        r=Relic(data['creation_date'],data['name'],data['content'])
        return r

    # Load a temporary collection from disk to an object
    @staticmethod
    def load_temp_collection(name,archive_dir):
        data = FileIO.read_string_full(archive_dir+name)
        data = json.loads(data)
        r=Relic(data['creation_date'],data['name'],data['content'])
        return r

    # Load a strata object from disk into an object
    @staticmethod
    def load_strata(chekcksum,archive_dir):
        data = FileIO.read_string_full(archive_dir+checksum)
        data = json.loads(data)
        r=Relic(data['creation_date'],data['name'],data['content'])
        return r

