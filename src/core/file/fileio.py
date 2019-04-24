# James Clarke
# 18/04/2019

# File handling static utilities for file operations

import os
from .. utils import conversions

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


    # Write a string to a file with overwride
    @staticmethod
    def write_string_overwride(filename,string):
        FileIO.write_bytes_overwride(filename, conversions.str_to_bytes(str(string)))

    # Write a string to a file with appendment
    @staticmethod
    def write_string_append(filename,string):
        FileIO.write_bytes_append(filename, conversions.str_to_bytes(str(string)))

    # Write a string and overwride a specific line
    @staticmethod
    def write_string_overwride_line(filename, string, line_num, newline=True):
        if newline:
            string+='\n'
        lines = FileIO.read_string_lines(filename)
        lines[line_num-1]=string
        FileIO.write_string_overwride(filename,''.join(lines))

    # Write a string and append a specific line
    @staticmethod
    def write_string_append_line(filename, string, line_num, newline=True):
        if newline:
            string+='\n'
        lines = FileIO.read_string_lines(filename)
        lines[line_num-1]=lines[line_num-1].rstrip()+string # rstrip() removes \n
        FileIO.write_string_overwride(filename,''.join(lines))

    # Write a string and insert after a specific line
    @staticmethod
    def write_string_insert_line(filename, string, line_num, newline=True):
        if newline:
            string+='\n'
        lines = FileIO.read_string_lines(filename)
        lines.insert(line_num-1, string)
        FileIO.write_string_overwride(filename,''.join(lines))



    # Return a file object
    @staticmethod
    def open_file(path, mode=FILE_READ):
        return open(path,mode=mode)
    
    # Close a file object
    @staticmethod
    def close_file(file):
        file.close()

    # Clear out a file
    @staticmethod
    def clear_file(filename):
        FileIO.write_string_overwride(filename,"")

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

    # Read a file as a string into a single string
    @staticmethod
    def read_string_full(filename):
        f = FileIO.open_file(filename, mode=FileIO.FILE_BIN_READ)
        content = f.read()
        content = conversions.bytes_to_str(content)
        return content

    # Read a file as a string into a string array
    @staticmethod
    def read_string_lines(filename):
        f = FileIO.open_file(filename, mode=FileIO.FILE_BIN_READ)
        content = f.readlines()
        for i in range(0, len(content)):
            content[i] = conversions.bytes_to_str(content[i])
        return content

    # Read a file at a specific line, continuing for n more lines
    @staticmethod
    def read_string_line_num(filename, line, num_lines=1):
        lines = FileIO.read_string_lines(filename)
        if num_lines > len(lines):
            print("Attempting to read too many lines!")
            return None
        new_lines=[]
        for i in range(line-1, line-1+(num_lines)):
            new_lines.append(lines[i])
        return new_lines


    # Create a directory at path with name
    @staticmethod
    def create_dir(path):
        newpath = path
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        return newpath

    # Get all subdirectories from current directory
    @staticmethod
    def get_sub_dirs(path):
        return [x[0] for x in os.walk(path)]
    
    # Get all immediate subdirectories in a given path
    @staticmethod
    def get_immediate_sub_dirs(path):
        return [name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))]

    # Check if a subdirectory is immediately within a directory
    @staticmethod
    def check_for_immediate_sub_dir(path, required):
        if required in FileIO.get_immediate_sub_dirs(path):
            return True

        return False

    # Check if a subdirectory is within a directory recursively
    @staticmethod
    def check_for_sub_dir(path, required):
        for dir in FileIO.get_sub_dirs(path):
            if required in dir:
                return True

        return False

    # Check if a directory is contained in a path
    @staticmethod
    def check_dir_within_parent(path, dir):
        return dir in path

    # Check a subdirectory exists
    @staticmethod
    def check_sub_dir_exists(path,dir):
        return os.path.exists(path+dir)
