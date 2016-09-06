import settings
import sys

def add_lib_paths(vals):
    sys.path.append(vals)
add_lib_paths(settings.EXTRA_LIBRARY_PATHS)

        


