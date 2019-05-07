import sys
sys.path.append("..") # Adds higher directory to python modules path.

from comms.action import ProjectAction, FileAction
from comms import commands
from out.log import Log

live_commands = {
    'init'      : ProjectAction.init,           # initialise a shuvel project
    'status'    : ProjectAction.status,         # Display the status of a project
    'log'       : ProjectAction.log,            # Display all stratas

    'clear'     : FileAction.clear,             # Clears temp files
    'new'       : FileAction.new,               # Create a new file in the temp folder
    'del'       : FileAction.delete_node,       # Delete a node
    'peek'      : FileAction.peek,              # Peek at a temp node
    'move'      : FileAction.move,              # Move a node in the temps folder
    'write'     : FileAction.write,             # Write data to a temp relic
    'archive'   : FileAction.archive_node,      # Archive a node in the temp folder

    'wipe'      : FileAction.wipe,              # Wipe all stratas and archives
    'overview'  : FileAction.overview_checksum, # View a directory layout of a checksum in the archives
    'excavate'  : FileAction.excavate_checksum, # Load an archive contents into the live temp folder
    'view'      : FileAction.view,              # View an archived node, via specifying strata and node
}

class Dispatcher:

    @staticmethod
    def dispatch(source,args):
        action=getattr(args, commands.action)
        if action in live_commands:
            live_commands[action](source,args)
        else:
            Log.status_error("Unknown command '"+action+"'!")        