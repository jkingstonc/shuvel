
from .fileio import FileIO
from ..utils import strings
class Lookup:

    @staticmethod
    def add_key(path, name, hash):
        FileIO.write_string_append(path,"\n"+name+":"+hash)

    @staticmethod
    def find_key_value(path, name):
        lines=FileIO.read_string_lines(path)
        for line in lines:
            if strings.strip_after_substring(line,":") == name:
                return strings.strip_after_substring(strings.strip_before_substring(line, ":"),"\n")
        return None