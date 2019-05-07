import sys
sys.path.append("..") # Adds higher directory to python modules path.

from . import commands

from core.file.projectfiles import ProjectFiles
from core.file.dump import Dump
from core.file.load import Load
from core.file.fileio import FileIO
from core.file.tempmanager import TempManager
from core.file.archivemanager import ArchiveManager
from core.file.traversal import Traversal

from core.nodes.node import Node
from core.nodes.relic import Relic
from core.nodes.collection import Collection
from core.nodes.strata import Strata

from out.log import Log


def are_you_sure():
    Log.status_warning("Are you sure? y/n")
    sure=input("")
    if sure=="y":
        return True
    else:
        return False

def check_in_project(path):
    if not ProjectFiles.check_project_in_path(path):
        Log.status_warning("Not in an active shuvel project! [Use shuvel init to create a project]")
        return False
    return True

# Class for dispatching project related commands
class ProjectAction:

    # Initialse a project in the given directory
    @staticmethod
    def init(path, args):
        Log.status_message("initializing project...")
        ProjectFiles.init_project(path)
        Log.status_confirmed("successfully created Shuvel project.")

    # Gives current status of the project
    @staticmethod
    def status(path, args):
        if check_in_project(path):
            TempManager.display_temp_files(ProjectFiles.Dirs.archive_relics_temp.value)

    # Log all stratas
    @staticmethod
    def log(path, args):
        if check_in_project(path):
            ArchiveManager.display_stratas(ProjectFiles.Dirs.archive_strata.value)

# Class for dispatching project file (node) related commands
class FileAction:

    # Clears temp folder
    @staticmethod
    def clear(path, args):
        if check_in_project(path):
            if are_you_sure():
                FileIO.clear_dir(ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
                TempManager.gen_root_temp("root",ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
                Log.status_confirmed("Successfully cleared temp folder!")


    # Wipe all stratas and archives
    @staticmethod
    def wipe(path, args):
        if check_in_project(path):
            if are_you_sure():
                FileIO.clear_dir(ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata))
                FileIO.clear_dir(ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics))
                Log.status_confirmed("Successfully wiped archives!")


    # Create a new temporary node in a project
    @staticmethod
    def new(path, args):
        if check_in_project(path):
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
            Log.status_confirmed("successfully created '"+name+"'.")

    # Delete file
    @staticmethod
    def delete_node(path, args):
        if check_in_project(path):
            if are_you_sure():
                name = getattr(args, commands.node_name)
                if TempManager.del_node(Load.load_node(name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)),ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)):   
                    Log.status_confirmed("Succsessfully deleted '"+name+"'.")

    # Peek at a node contents
    @staticmethod
    def peek(path, args):
        if check_in_project(path):
            name = getattr(args, commands.node_name)
            out_type=getattr(args,commands.output_type)
            variable_type=getattr(args,commands.variable_type)
            message = getattr(args,commands.message)

            node = Load.load_node(name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))

            to_peek=""
            if variable_type == "date" or variable_type == "d":
                to_peek=node._creation_date
            elif variable_type == "checksum" or variable_type == "c":
                to_peek == node._checksum
            else:
                if type(node) is Relic:
                    to_peek=node._storage_data_contents
                elif type(node) is Collection:
                    for checksum in node._checksums:
                        to_peek+=checksum+"\n"

      
            if out_type == "file" or out_type == "f":
                FileIO.write_string_overwride(message,to_peek)
                Log.status_confirmed("successfully peeked '"+name+"' to '"+message+"'.")
            if out_type == "text" or out_type ==  "t":
                Log.status_content(to_peek)
           
    
    # Move a node from one location to another
    @staticmethod
    def move(path, args):
        if check_in_project(path):
            name = getattr(args, commands.node_name)
            target = getattr(args, commands.destination_node_name)

            source_node = Load.load_node(name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
            target_node = Load.load_node(target,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))

            TempManager.move_node_to_collection(source_node,target_node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
            Log.status_confirmed("successfully moved '"+name+"' to '"+target+"'.")

    @staticmethod
    def write(path, args):
        if check_in_project(path):
            name=getattr(args, commands.node_name)
            
            write_type=getattr(args,commands.write_type)
            input_type=getattr(args,commands.input_type)

            message = getattr(args,commands.message)


            node = Load.load_node(name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
            if type(node) is Relic:
                new_data=None

                if input_type == "text" or input_type == "t":
                    new_data=message
                elif input_type == "file" or input_type == "f":
                    new_data=FileIO.read_string_full(message)
                    if new_data is None:
                        Log.status_error("Error reading file :/")
                        return
                
                if write_type=="overwride" or write_type=="o":
                    node.set_storage_data_contents(new_data)
                elif write_type=="append" or write_type=="a":
                    node._storage_data_contents=node._storage_data_contents+new_data

                node.checksum_me()
                Dump.dump_temp_relic(node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
                Log.status_confirmed("Successfully added to '"+name+"'.")
            else:
                Log.status_warning("'"+name+"' is not a Relic!")



    # Archive a given node name
    @staticmethod
    def archive_node(path, args):
        if check_in_project(path):
            name = getattr(args, commands.node_name)
            message = getattr(args, commands.message)
            TempManager.archive_temp(
                Load.load_node(getattr(args, commands.destination_node_name),ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)),
                name,
                message,
                ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata),
                ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics),
                ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)
                )
            Log.status_confirmed("successfully archived '"+name+"'.")

    # View a directory layout of a checksum in the archives
    @staticmethod
    def overview_checksum(path, args):
        if check_in_project(path):
            checksum = getattr(args, commands.node_name)
            checksum=ArchiveManager.get_full_checksum(checksum,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata))
            strata = Load.load_node(checksum,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata))
            ArchiveManager.display_archived_files_from_strata(strata, ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics))

    # Load an archive contents into the live temp folder
    @staticmethod
    def excavate_checksum(path, args):

        if check_in_project(path):
            if are_you_sure():
                FileIO.clear_dir(ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
                TempManager.gen_root_temp("root",ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
                checksum = getattr(args, commands.node_name)
                checksum=ArchiveManager.get_full_checksum(checksum,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata))
                strata = Load.load_node(checksum,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata),using_checksum=True)
                ArchiveManager.excavate_strata(strata, ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics),ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
                Log.status_confirmed("successfully excavated '"+checksum+"'.")

    # View an archived node, via specifying strata and node
    @staticmethod
    def view(path, args):
        if check_in_project(path):
            node_name = getattr(args, commands.node_name)
            strata_name = getattr(args, commands.destination_node_name)
            out_type=getattr(args,commands.output_type)
            variable_type=getattr(args,commands.variable_type)
            message = getattr(args,commands.message)

            strata_name=ArchiveManager.get_full_checksum(strata_name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata))
            strata = Load.load_node(strata_name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata),using_checksum=True)
            node = ArchiveManager.get_node_from_strata(strata, node_name, ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics))

            if node != None: 
                to_view=""
                if variable_type == "date" or variable_type == "d":
                    to_view=node._creation_date
                elif variable_type == "checksum" or variable_type == "c":
                    to_view == node._checksum
                else:
                    if type(node) is Relic:
                        to_view=node._storage_data_contents
                    elif type(node) is Collection:
                        for checksum in node._checksums:
                            to_view+=checksum+"\n"
                if out_type == "file" or out_type == "f":
                    FileIO.write_string_overwride(message,to_view)
                    Log.status_confirmed("successfully viewed '"+node_name+"' to '"+message+"'.")
                if out_type == "text" or out_type ==  "t":
                    if to_view != "":
                        Log.status_content(to_view)