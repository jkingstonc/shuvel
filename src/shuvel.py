import argparse, os
from comms.dispatcher import Dispatcher

from comms import commands

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="An argparse example")

    # Arguments prefixed with - are optional
    parser.add_argument(commands.action, help='The action to take (e.g. init, add, etc.)')
    parser.add_argument(commands.node_name_short,commands.node_name_long, help='The node name being specified.', default=None)
    parser.add_argument(commands.destination_node_name_short,commands.destination_node_name_long, help='The node name being targeted.', default=None)
    parser.add_argument(commands.node_type_short,commands.node_type_long, help='The node type being specified.', default=None)
    parser.add_argument(commands.message_short,commands.message_long, help='The node type being specified.', default="")
    parser.add_argument(commands.write_type_short,commands.write_type_long, help='Overwride or append node content.', default="")
    parser.add_argument(commands.input_type_short,commands.input_type_long, help='Raw input or file input', default="")
    parser.add_argument(commands.output_type_short,commands.output_type_long, help='Raw output or file output', default="")
    parser.add_argument(commands.variable_type_short,commands.variable_type_long, help='Raw output or file output', default="")


    args = parser.parse_args()

    Dispatcher.dispatch(os.getcwd()+"\\",args)

