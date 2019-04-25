from ..file.projectfiles import ProjectFiles
from ..file.fileio import FileIO

class Dump:

    # Write a relic object to disk in the archive directory of a project
    @staticmethod
    def dump_relic(relic,archive_dir):
        FileIO.write_string_overwride(archive_dir+relic.get_checksum_short(), relic.get_string_dump())

    def dump_collection():
        pass
