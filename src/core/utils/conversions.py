# James Clarke
# 18/04/2019

# Conversion utilities for common operations
# (Big endian is used)

class Conversions:

    # Convert a string to byte array
    @staticmethod
    def str_to_bytes(string):
        b = bytearray()
        b.extend(map(ord, string))
        return b

    # Convert a string to byte array
    @staticmethod
    def int_to_bytes(i):
        #b=i.to_bytes(2, byteorder="big", signed=True)
        b=Conversions.str_to_bytes(str(i))
        return b

    # Convert bytes to string
    @staticmethod
    def bytes_to_str(b):
        string = b.decode("utf-8")
        return string

    