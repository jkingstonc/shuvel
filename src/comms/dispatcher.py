
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
            'init'      : ProjectAction.init,
            'status'    : ProjectAction.status,
            'new'       : FileAction.new,
            'move'      : FileAction.move,
            'add'       : FileAction.add,
            'archive'   : FileAction.archive_node,
        }[action]

        