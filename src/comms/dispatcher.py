
# Main commands:

#   Project ->
#       'init'          - Initialise a new shuvel project
#       'validate'      - Validate the shuvel project files
#       'usermodify'    - Modify user information (e.g. username etc)
#
#   File ->
#       'new'
#
#
#
#
#
#

from .action import ProjectAction, FileAction
from . import commands

class Dispatcher:

    @staticmethod
    def dispatch(source,args):
        Dispatcher.parse_action(source,getattr(args, commands.action))(source,args)

    @staticmethod
    def parse_action(source,action):
        return {
            'init'      : ProjectAction.init,           # initialise a shuvel project
            'status'    : ProjectAction.status,         # Display the status of a project
            'new'       : FileAction.new,               # Create a new file in the temp folder
            'move'      : FileAction.move,              # Move a node in the temps folder
            'add'       : FileAction.add,               # Add data to a temp relic
            'archive'   : FileAction.archive_node,      # Archive a node in the temp folder
            'overview'  : FileAction.overview_checksum, # View a directory layout of a checksum in the archives
        }[action]

        