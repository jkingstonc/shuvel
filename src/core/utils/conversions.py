# James Clarke
# 18/04/2019

# Conversion utilities for common operations

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
        b=i.to_bytes(2, byteorder="big", signed=True)
        return b