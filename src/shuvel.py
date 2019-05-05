import argparse, os
from comms.dispatcher import Dispatcher

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="An argparse example")

    # Arguments prefixed with - are optional
    parser.add_argument('action', help='The action to take (e.g. init, add, etc.)')
    parser.add_argument('-n','--node_name', help='The node name being specified.', default=None)
    parser.add_argument('-an','--archive_name', help='The node name being specified.', default=None)
    parser.add_argument('-nt','--node_type', help='The node type being specified.', default=None)
    parser.add_argument('-m','--message', help='The node type being specified.', default="")

    args = parser.parse_args()

    Dispatcher.dispatch(os.getcwd()+"\\",args)

