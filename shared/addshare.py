"""Little trick to add shared modules into project.

I don't want to mess with global PATH or install my packeges.
So this module adds path to shared directory into path of project.
Both server and client have copy of this module.
"""

from sys import argv, path as PATH
from os.path import abspath


def get_abs_path():
    """Get absolute path to project."""
    path_script = abspath(argv[0]).replace("\\", "/")
    path_to_project = "/".join(path_script.split("/")[:-3])
    return path_to_project

# PATH.append(get_abs_path() + "/shared")
