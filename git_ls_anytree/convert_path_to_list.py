"""This file provides convert_path_to_list"""

from os.path import split

def convert_path_to_list(path_to_explode):
    """Converts a path to a list exploded at the OS delimiters"""
    path_dirname, path_basename = split(path_to_explode)
    if 0 < len(path_dirname) and '/' != path_dirname:
        return convert_path_to_list(path_dirname) + [path_basename]
    else:
        return [path_basename]
