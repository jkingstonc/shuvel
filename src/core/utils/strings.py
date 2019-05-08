"""

This is a helper file for string operations.

"""

# Strip everything after a string that matches a given strip string
def strip_after_substring(tostrip, strip):
    return tostrip.partition(strip)[0]

# Strip everything before a string that matches a given strip string
def strip_before_substring(tostrip, strip):
    return tostrip.partition(strip)[2]