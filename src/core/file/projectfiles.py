# James Clarke
# 22/04/2019

# A class for helping locate and use project files when using the shovel command line app

from .fileio import FileIO
from . import shuveldefaults

class ProjectFiles:
    
    # Initialise an empty shuvel project 
    @staticmethod
    def init_project(path):
        root=FileIO.create_dir(path+shuveldefaults.SHUV_ROOT)
        settings=FileIO.create_dir(path+shuveldefaults.SETTINGS)
        museum_store=FileIO.create_dir(path+shuveldefaults.MUSEUM_STORE)
        relic_store=FileIO.create_dir(path+shuveldefaults.RELIC_STORE)
        strata_store=FileIO.create_dir(path+shuveldefaults.STRATA_STORE)

    # Check if the given path is withing a .shuv
    @staticmethod
    def check_project_in_path(path):
        # Check if we are deep in the .shuv folder
        if FileIO.check_dir_within_parent(path,shuveldefaults.SHUV_ROOT_NAME):
            return True
        # Check if the .shuv folder is within our current directory
        if FileIO.check_for_immediate_sub_dir(path, shuveldefaults.SHUV_ROOT_NAME):
            return True
        return False

    # Get the path to the .shuv if we are in a .shuv directory
    @staticmethod
    def get_project_root(path):
        pass

    # Ensure all correct directories and files exist
    @staticmethod
    def validate_shuv(path):
        # Here we need to traverse from .shuv and ensure the required files/directories are located
        pass