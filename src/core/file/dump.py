# James Clarke
# 25/04/2019

# All verification is done before any of these functions are called

from ..file.projectfiles import ProjectFiles
from ..file.fileio import FileIO

class Dump:

    # Write a relic object to disk in the archive directory of a project
    @staticmethod
    def dump_relic(relic,archive_dir):
        FileIO.write_string_overwride(archive_dir+relic.get_checksum_short(), relic.get_string_dump())

    # Write a temp relic object to disk in the archive temp directory of a project
    @staticmethod
    def dump_temp_relic(relic,archive_dir):
        FileIO.write_string_overwride(archive_dir+relic.get_checksum_short(), relic.get_string_dump())

    # Write a collection object to disk in the archive directory of a project
    def dump_collection(collection,archive_dir):
        FileIO.write_string_overwride(archive_dir+collection.get_checksum_short(), collection.get_string_dump())
