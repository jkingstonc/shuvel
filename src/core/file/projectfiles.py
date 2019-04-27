# James Clarke
# 22/04/2019

# A class for helping locate and manage project files/directories
from enum import Enum
from .fileio import FileIO
from ..utils import strings
from . import shuveldefaults


class ProjectFiles:
    
    class Dirs(Enum):
       archive_relics = shuveldefaults.RELIC_STORE
       archive_relics_temp = shuveldefaults.RELIC_TEMP_STORE
       archive_strata = shuveldefaults.STRATA_STORE

    # Initialise an empty shuvel project 
    @staticmethod
    def init_project(path):
        # initialising all directories
        root=FileIO.create_dir(path+shuveldefaults.SHUV_ROOT)
        settings=FileIO.create_dir(path+shuveldefaults.SETTINGS)
        museum_store=FileIO.create_dir(path+shuveldefaults.MUSEUM_STORE)
        relic_store=FileIO.create_dir(path+shuveldefaults.RELIC_STORE)
        relic_temp_store=FileIO.create_dir(path+shuveldefaults.RELIC_TEMP_STORE)
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
        # If we are in a valid .shuv project
        if ProjectFiles.check_project_in_path(path):
            # Strip all irelevant directory information to get the root
            return strings.strip_after_substring(path, shuveldefaults.SHUV_ROOT_NAME)
        return False

    # Get a specified shuvel directory based on the path the command was executed from
    @staticmethod
    def get_dir_from_root(path, directory_specifier):
        return ProjectFiles.get_project_root(path)+directory_specifier.value

    # Locate .shuv component directory paths
    @staticmethod
    def get_project_component_dir_path(path, component_dir):
        pass

    # Locate .shuv component path
    @staticmethod
    def get_project_component_dir_path(path, component):
        pass

    # Ensure all correct directories and files exist
    @staticmethod
    def validate_shuv(path):
        # Here we need to traverse from .shuv and ensure the required files/directories are located
        pass