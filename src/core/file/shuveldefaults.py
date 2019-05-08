"""

Contains all variables for locating directories in a shuvel project

"""

SHUV_ROOT_NAME=".shuv"                      # The root folder name for a shuvel project
SHUV_ROOT=SHUV_ROOT_NAME+"//"               # The root folder for a shuvel project
SETTINGS=SHUV_ROOT+"//settings//"           # The project settings folder for a shuvel project
MUSEUM_STORE=SHUV_ROOT+"//museum//"         # Directory for the museum directory {stores all nodes}
RELIC_STORE=MUSEUM_STORE+"//relics//"       # Directory for relic storage
RELIC_TEMP_STORE=RELIC_STORE+"//temp//"     # Directory for relic storage
STRATA_STORE=MUSEUM_STORE+"//stratas//"     # Directory for strata storage

TEMP_ROOT_COLLECTION="root"                 # Root file name for the temp archive

