"""

All arguments that are required for the operation of shuvel.

"""

# The standard required argument, tell shuvel what command we want to execute
action="action"

# The name of a node we are creating, targeting or using
node_name="node_name"
node_name_long="--node_name"
node_name_short="-n"

# The name of a node that we are specifically targeting as a secondary node
destination_node_name="destination_node_name"
destination_node_name_long="--destination_node_name"
destination_node_name_short="-d"

# Type of node we are specifying
node_type="type"
node_type_long="--type"
node_type_short="-t"

# The message we want to use with the command
message="message"
message_long="--message"
message_short="-m"

# The write type we are specifying, e.g. overwride, append etc
write_type="write_type"
write_type_long="--write_type"
write_type_short="-w"

# The input type we are specifying, e.g. text, file etc
input_type="input_type"
input_type_long="--input_type"
input_type_short="-i"

# The output type we are specifying, e.g. text, file etc
output_type="output_type"
output_type_long="--output_type"
output_type_short="-o"

# The node variable we are specifying, e.g. creation date, name, checksum etc
variable_type="variable_type"
variable_type_long="--variable_type"
variable_type_short="-v"