"""

File that contains multiple classes that handles the operations of all shuvel commands.
Note: This implementation is sloppy as part of the action code is implemented here, and other
parts is implemented in other files.

"""

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

# Asks an are you sure message before proceeding with an action
def are_you_sure():
    Log.status_warning("Warning: Are you sure? y/n")
    sure=input("")
    if sure=="y":
        return True
    else:
        return False

# Checks if we are in a project before carrying out an action
def check_in_project(path):
    if not ProjectFiles.check_project_in_path(path):
        Log.status_warning("Warning: Not in an active shuvel project! [Use shuvel init to create a project]")
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
    # Note: This currently only displays temp files, should display more?
    @staticmethod
    def status(path, args):
        if check_in_project(path):
            TempManager.display_temp_files(ProjectFiles.Dirs.archive_relics_temp.value)

    # Display all stratas
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
                # Clear the temp dir and create a new root collection
                if FileIO.clear_dir(ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)) and \
                    TempManager.gen_root_temp("root",ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)):
                    Log.status_confirmed("successfully cleared temp folder!")


    # Wipe all stratas and archives
    @staticmethod
    def wipe(path, args):
        if check_in_project(path):
            if are_you_sure():
                if FileIO.clear_dir(ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata),clear_dirs=True) and \
                    FileIO.clear_dir(ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics),clear_dirs=False):
                    Log.status_confirmed("Successfully wiped archives!")


    # Create a new temporary node in a project
    @staticmethod
    def new(path, args):
        if check_in_project(path):
            move_to = None
            node = None
            name = getattr(args, commands.node_name)
            node_type = getattr(args, commands.node_type)
            # Name and type are required
            if name == None or node_type == None:
                Log.status_error("Error: Name and type required!")
                return
            # Get the specified destination, if None then get the root collection
            destination = getattr(args, commands.destination_node_name)
            if destination != None:
                move_to=Load.load_node(destination,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
            else:
                move_to=Load.load_node(ProjectFiles.Files.temp_root.value,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
            # If the type is relic, then dump the relic
            if node_type == "relic" or node_type == "r":
                node = Relic(name=name)
                node.checksum_me_rand()
                if Dump.dump_temp_relic(node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)) == False:
                    Log.status_error("Error: Couldn't create '"+name+"'.")
            # If the type is relic, then dump the collection
            elif node_type == "collection" or node_type == "c":
                node = Collection(name=name)
                node.checksum_me_rand()
                if Dump.dump_temp_collection(node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)) == False:
                    Log.status_error("Error: Couldn't create '"+name+"'.")
            # Move the node to the target collection
            if TempManager.move_node_to_collection(node,move_to,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)):
                Log.status_confirmed("successfully created '"+name+"'.")
            else:
                Log.status_error("Error: Couln't move '"+name+"' to root collection!")

    # Delete a node
    @staticmethod
    def delete_node(path, args):
        if check_in_project(path):
            if are_you_sure():
                name = getattr(args, commands.node_name)
                if name == "root":
                    Log.status_error("Error: Cannot delete root!")
                    return
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
            # Name and type are required
            if name == None:
                Log.status_error("Error: Name required")
                return
            node = Load.load_node(name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
            if node == None:
                Log.status_error("Error: '"+name+"' doesn't exist!")
                return
            # The message we want
            to_peek=""
            # First check if we have specified a variable
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
            # Check if we have specified text or file, if not, use text by default
            if out_type == "file" or out_type == "f":
                FileIO.write_string_overwride(message,to_peek)
                Log.status_confirmed("successfully peeked '"+name+"' to '"+message+"'.")
            elif out_type == "text" or out_type ==  "t" or out_type==None:
                Log.status_content(to_peek)
    
    # Move a node from one location to another
    @staticmethod
    def move(path, args):
        if check_in_project(path):
            name = getattr(args, commands.node_name)
            target = getattr(args, commands.destination_node_name)
            if name == None or target == None:
                Log.status_error("Error: Name & target required!")
                return
            # Get the nodes that are being utalised
            source_node = Load.load_node(name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
            target_node = Load.load_node(target,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
            if source_node == None or target_node == None:
                Log.status_error("Error: Node couldn't be loaded!")
                return
            # Move the source to target
            if TempManager.move_node_to_collection(source_node,target_node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)):
                Log.status_confirmed("successfully moved '"+name+"' to '"+target+"'.")
            else:
                Log.status_error("Error: Couldn't move '"+name+"' to '"+target+"'!")

    # Write data to a relic
    @staticmethod
    def write(path, args):
        if check_in_project(path):
            name=getattr(args, commands.node_name)
            write_type=getattr(args,commands.write_type)
            input_type=getattr(args,commands.input_type)
            message = getattr(args,commands.message)
            if name == None or message == None:
                Log.status_error("Error: Name & input required!")
                return
            # Load the node we are writing to
            node = Load.load_node(name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp))
            if node == None:
                Log.status_error("Error: Node couldn't be loaded!")
                return
            # Ensure we are trying to write to a Relic
            if type(node) is Relic:
                new_data=None
                if message != None:
                    # Check whether input is a file or raw text, raw text by default
                    if input_type == "file" or input_type == "f":
                        new_data=FileIO.read_string_full(message)
                        if new_data is None:
                            Log.status_error("Error: Couldn't read file!")
                            return
                    elif input_type == "text" or input_type == "t" or input_type==None:
                        new_data=message
                    # Check whether write type is overwride or append, overwride by default
                    if write_type=="append" or write_type=="a":
                        node._storage_data_contents=node._storage_data_contents+new_data
                    elif write_type=="overwride" or write_type=="o" or write_type==None:
                        node.set_storage_data_contents(new_data)
                else:
                    Log.status_error("Error: Input required!")
                    return
                node.checksum_me()
                # Dump the relic to file
                if Dump.dump_temp_relic(node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)):
                    Log.status_confirmed("Successfully added to '"+name+"'.")
                else:
                    Log.status_warning("Error: Couldn't dump relic!")
            else:
                Log.status_error("Error: '"+name+"' is not a Relic!")

    # Archive a given node name
    @staticmethod
    def archive_node(path, args):
        if check_in_project(path):
            name = getattr(args, commands.node_name)
            message = getattr(args, commands.message)
            target_node = getattr(args, commands.destination_node_name)
            if name == None or target_node == None:
                Log.status_error("Error: Name and target node required!")
                return
            if message==None:
                Log.status_warning("Warning: You are archiving without a message")
                are_you_sure()
            # Archive the node
            if TempManager.archive_temp( \
                Load.load_node(target_node,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)), \
                name, \
                message, \
                ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata), \
                ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics), \
                ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp) \
                ):
                Log.status_confirmed("successfully archived '"+name+"'.")
            else:
                Log.status_error("Error: Couldn't archive strata!")

    # View a directory layout of a checksum in the archives
    @staticmethod
    def overview_checksum(path, args):
        if check_in_project(path):
            checksum = getattr(args, commands.node_name)
            if checksum == None:
                Log.status_error("Error: checksum required!")
                return
            checksum=ArchiveManager.get_full_checksum(checksum,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata))
            if checksum==None:
                Log.status_error("Error: Couldn't locate checksum!")
                return
            strata = Load.load_node(checksum,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata))
            if strata == None:
                Log.status_error("Error: Strata couldn't be loaded!")
            # Display the archive
            ArchiveManager.display_archived_files_from_strata(strata, ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics))

    # Load an archive contents into the live temp folder
    @staticmethod
    def excavate_checksum(path, args):
        if check_in_project(path):
            if are_you_sure():
                checksum = getattr(args, commands.node_name)
                if checksum == None:
                    Log.status_error("Error: Checksum required!")
                    return
                checksum=ArchiveManager.get_full_checksum(checksum,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata))
                if checksum==None:
                    Log.status_error("Error: Couldn't locate checksum!")
                    return
                if FileIO.clear_dir(ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)) == False:
                    Log.status_error("Error: Couldn't clear temp folder!")
                    return
                if TempManager.gen_root_temp("root",ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)) == False:
                    Log.status_error("Error: Couldn't generate a root temp collection!")
                    return
                strata = Load.load_node(checksum,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata),using_checksum=True)
                if strata == None:
                    Log.status_error("Error: Strata couldn't be loaded!")
                    return
                if ArchiveManager.excavate_strata(strata, ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics),ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics_temp)) == False:
                    Log.status_error("Error: Couldn't excavate nodes from strata!")
                    return
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
            if node_name == None and strata_name == None:
                Log.status_error("Error: Node and strata name required!");
                return
            strata_name=ArchiveManager.get_full_checksum(strata_name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata))
            if strata_name == None:
                Log.status_error("Error: Couldn't locate checksum!")
                return
            strata = Load.load_node(strata_name,ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_strata),using_checksum=True)
            if strata == None:
                Log.status_error("Error: Strata couldn't be loaded!")
            node = ArchiveManager.get_node_from_strata(strata, node_name, ProjectFiles.get_dir_from_root(path,ProjectFiles.Dirs.archive_relics))
            if node != None: 
                # The message we want
                to_view=""
                # First check if we have specified a variable
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
                # Check if we have specified text or file, if not, use text by default
                if out_type == "file" or out_type == "f":
                    FileIO.write_string_overwride(message,to_view)
                    Log.status_confirmed("successfully peeked '"+name+"' to '"+message+"'.")
                elif out_type == "text" or out_type ==  "t" or out_type==None:
                    Log.status_content(to_view)
            else:
                Log.status_error("Error: Node couldn't be loaded!")