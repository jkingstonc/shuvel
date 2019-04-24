
# Strip everything after a given strip string
def strip_after_substring(tostrip, strip):
    return tostrip.partition(strip)[0]

# Strip everything before a given strip string
def strip_before_substring(tostrip, strip):
    return tostrip.partition(strip)[2]