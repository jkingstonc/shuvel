# James Clarke
# 18/04/2019

# File handling static utilities for file operations

class FileIO:

    FILE_READ = 'r'
    FILE_BIN_READ = 'r+b'
    FILE_WRITE = 'w'
    FILE_EXCLUSIVE_CREATE = 'x'
    FILE_APPEND = 'a'
    FILE_TEXT = 't'
    FILE_BIN_WRITE = 'w+b'
    FILE_BIN_APPEND = 'a+b'
    FILE_UPDATE = '+'

    ENCODING_UTF8 = 'utf-8'


    # Return a file object
    @staticmethod
    def open_file(path, mode=FILE_READ):
        return open(path,mode=mode)
    
    # Close a file object
    @staticmethod
    def close_file(file):
        file.close()

    # Write a string to a file with overwride
    @staticmethod
    def write_string_overwride(filename,string):
        f=FileIO.open_file(filename, FileIO.FILE_WRITE).write(string)
        FileIO.close_file(f)

    # Write a string to a file with appendment
    @staticmethod
    def write_string_append(filename,string):
        f=FileIO.open_file(filename, FileIO.FILE_APPEND).write(string)
        FileIO.close_file(f)

    # Write raw bytes to a file with overwride
    @staticmethod
    def write_bytes_overwride(filename,b):
        f=FileIO.open_file(filename, mode=FileIO.FILE_BIN_WRITE)
        f.write(b)
        FileIO.close_file(f)

    # Write raw bytes to a file with appendment
    @staticmethod
    def write_bytes_append(filename,b):
        f=FileIO.open_file(filename, mode=FileIO.FILE_BIN_APPEND)
        f.write(b)
        FileIO.close_file(f)

    # Read a file as bytes
    @staticmethod
    def read_bytes(filename):
        f = FileIO.open_file(filename, mode=FileIO.FILE_BIN_READ)
        content = f.read()
        return content
