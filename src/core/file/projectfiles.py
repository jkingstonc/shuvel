# James Clarke
# 22/04/2019

# A class for helping locate and use project files when using the shovel command line app

from .fileio import FileIO
from . import shuveldefaults

class ProjectFiles:
    
    # Initialise an empty shuvel project 
    @staticmethod
    def init_project(path):
        root=FileIO.create_dir(path+shuveldefaults.SHUV_NAME)
        museum_store=FileIO.create_dir(root+shuveldefaults.MUSEUM_STORE)
        relic_store=FileIO.create_dir(root+shuveldefaults.RELIC_STORE)
        strata_store=FileIO.create_dir(root+shuveldefaults.STRATA_STORE)