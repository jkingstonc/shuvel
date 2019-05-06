import sys
sys.path.append("..") # Adds higher directory to python modules path.

from . import commands

from core.file.projectfiles import ProjectFiles
from core.file.dump import Dump
from core.file.load import Load
from core.file.tempmanager import TempManager
from core.file.archivemanager import ArchiveManager
from core.file.traversal import Traversal

from core.nodes.node import Node
from core.nodes.relic import Relic
from core.nodes.collection import Collection
from core.nodes.strata import Strata

# Class for dispatching project related commands
class ProjectAction:

    # Initialse a project in the given directory
    @staticmethod
    def init(path, args):
        print("initializing project...")
        ProjectFiles.init_project(path)
        print("successfully created Shuvel project.")

    # Gives current status of the project
    @staticmethod
    def status(path, args):
        TempManager.display_temp_files(ProjectFiles.Dirs.archive_relics_temp.value)
        ArchiveManager.display_stratas(ProjectFiles.Dirs.archive_strata.value)
        

# Class for dispatching project file (node) related commands
class FileAction:

    # Create a new temporary node in a project
    @staticmethod
    def new(path, args):
        move_to = None
        node = None
        name = getattr(args, commands.node_name)
        node_type = getattr(args, commands.node_type)
        destination = getattr(args, commands.destination_node_name)
        if destination != None:
            move_to=Load.load_node(destination,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
        else:
           move_to=Load.load_node(ProjectFiles.Files.temp_root.value,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))

        

        if node_type == "relic" or node_type == "r":
            node = Relic(name=name)
            node.checksum_me_rand()
            Dump.dump_temp_relic(node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
        elif node_type == "collection" or node_type == "c":
            node = Collection(name=name)
            node.checksum_me_rand()
            Dump.dump_temp_collection(node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))

        TempManager.move_node_to_collection(node,move_to,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
        print("successfully created '"+name+"' in '"+destination+"'.")

    # Move a node from one location to another
    @staticmethod
    def move(path, args):
        name = getattr(args, commands.node_name)
        target = getattr(args, commands.destination_node_name)

        source_node = Load.load_node(name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
        target_node = Load.load_node(target,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))

        TempManager.move_node_to_collection(source_node,target_node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
        print("successfully moved '"+name+"' to '"+target+"'.")

    # Archive a given node name
    @staticmethod
    def archive_node(path, args):
        name = getattr(args, commands.archive_name)
        message = getattr(args, commands.message)
        TempManager.archive_temp(
            Load.load_node(getattr(args, commands.node_name),ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)),
            name,
            message,
            ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata),
            ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics),
            ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)
            )
        print("successfully archived '"+name+"'.")