# James Clarke
# 18/04/2019

# C


# Contains all variables for locating directories in a shuvel project
SHUV_ROOT_NAME=".shuv"
SHUV_ROOT=SHUV_ROOT_NAME+"//"

SETTINGS=SHUV_ROOT+"//settings//"

MUSEUM_STORE=SHUV_ROOT+"//museum//"     # Directory for the museum directory {stores all nodes}
RELIC_STORE=MUSEUM_STORE+"//relics//"     # Directory for relic storage
RELIC_TEMP_STORE=RELIC_STORE+"//temp//"     # Directory for relic storage
COLLECTION_STORE=RELIC_STORE            # Directory for collection storage
STRATA_STORE=MUSEUM_STORE+"//stratas//"   # Directory for strata storage