"""

This file is the main entry point for the shuvel command line application.
It registers all command arguments and dispatches the parsed arguments.

"""


import argparse, os
from comms.dispatcher import Dispatcher

from comms import commands

if __name__ == "__main__":

    # Create an argument parser
    parser = argparse.ArgumentParser(description="An argparse example")
    # Add all arguments to the parser
    parser.add_argument(commands.action, help='The action to take (e.g. init, add, etc.)')
    parser.add_argument(commands.node_name_short,commands.node_name_long, help='The node name being specified.', default=None)
    parser.add_argument(commands.destination_node_name_short,commands.destination_node_name_long, help='The node name being targeted.', default=None)
    parser.add_argument(commands.node_type_short,commands.node_type_long, help='The node type being specified.', default=None)
    parser.add_argument(commands.message_short,commands.message_long, help='The message being send to shuvel.', default=None)
    parser.add_argument(commands.write_type_short,commands.write_type_long, help='Write type for writing [overwride or append].', default=None)
    parser.add_argument(commands.input_type_short,commands.input_type_long, help='Input type for writing [raw text or file]', default=None)
    parser.add_argument(commands.output_type_short,commands.output_type_long, help='Output type for reading [raw text or file]', default=None)
    parser.add_argument(commands.variable_type_short,commands.variable_type_long, help='Variable being specified [creation date, checksum etc]', default=None)
    
    args = parser.parse_args()
    # Dispatch the arguments to the shuvel dispatcher, along with the path that it was called from
    Dispatcher.dispatch(os.getcwd()+"\\",args)

