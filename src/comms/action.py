import sys
sys.path.append("..") # Adds higher directory to python modules path.
from core.file.projectfiles import ProjectFiles


class ProjectAction:

    @staticmethod
    def init(path, args):
        print("Initialising project...")
        ProjectFiles.init_project(path)

class FileAction:

    @staticmethod
    def new(path, args):
        pass