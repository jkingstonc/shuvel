# James Clarke
# 18/04/2019

# Contains all variables for locating directories in a shuvel project

SHUV_ROOT_NAME=".shuv"
SHUV_ROOT=SHUV_ROOT_NAME+"//"
SETTINGS=SHUV_ROOT+"//settings//"
MUSEUM_STORE=SHUV_ROOT+"//museum//"         # Directory for the museum directory {stores all nodes}
RELIC_STORE=MUSEUM_STORE+"//relics//"       # Directory for relic storage
RELIC_TEMP_STORE=RELIC_STORE+"//temp//"     # Directory for relic storage
STRATA_STORE=MUSEUM_STORE+"//stratas//"     # Directory for strata storage

TEMP_RELIC_LOOKUP_FILE="lookup"                  # Lookup file for temp relics/collections
