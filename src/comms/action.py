import sys
sys.path.append("..") # Adds higher directory to python modules path.
from core.file.projectfiles import ProjectFiles
from core.file.dump import Dump
from core.file.load import Load
from core.file.tempmanager import TempManager

from core.nodes.node import Node
from core.nodes.relic import Relic
from core.nodes.collection import Collection
from core.nodes.strata import Strata

# Class for dispatching project related commands
class ProjectAction:

    # Initialse a project in the given directory
    @staticmethod
    def init(path, args):
        print("Initialising project...")
        ProjectFiles.init_project(path)

# Class for dispatching project file (node) related commands
class FileAction:

    # Create a new temporary node in a project
    @staticmethod
    def new(path, args):
        node = None
        name = getattr(args, 'node_name')
        node_type = getattr(args, 'node_type')
        if node_type == "relic" or node_type == "r":
            node = Relic(name=name)
            node.checksum_me_rand()
            Dump.dump_temp_relic(node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
        elif node_type == "collection" or node_type == "c":
            node = Collection(name=name)
            node.checksum_me_rand()
            Dump.dump_temp_collection(node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))


    # Archive a given node name
    @staticmethod
    def archive_node(path, args):
        # Archive the temp folder from the "test file 1" relic
        TempManager.archive_temp(
            Load.load_node(getattr(args, 'node_name'),ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)),
            getattr(args, 'archive_name'),
            getattr(args, 'message'),
            ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata),
            ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics),
            ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)
            )