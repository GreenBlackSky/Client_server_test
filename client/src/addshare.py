"""Little trick to add shared modules into project.

I don't want to mess with global PATH or install my packeges.
So this module adds path to shared directory into path of project.
Both server and client have copy of this module.
"""

from sys import argv, path as PATH
from os import getcwd
from os.path import abspath

PATH_TO_SCRIPT = abspath(argv[0]).replace("\\", "/")
PATH_TO_FOLDER = "/".join(PATH_TO_SCRIPT.split("/")[:-3])
PATH_TO_SHARED = PATH_TO_FOLDER + "/shared"
PATH.append(PATH_TO_SHARED)
