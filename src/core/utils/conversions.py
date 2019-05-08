"""

Conversion utilities for standard operations, typically from standard data types to one and other.
Where bytes are converted, big endian should be used.

"""

# Convert a string to byte array
def str_to_bytes(string):
    b = bytearray()
    b.extend(map(ord, string))
    return b

# Convert a string to byte array
def int_to_bytes(i):
    #b=i.to_bytes(2, byteorder="big", signed=True)
    b=Conversions.str_to_bytes(str(i))
    return b

# Convert bytes to string
def bytes_to_str(b):
    string = b.decode("utf-8")
    return string

    