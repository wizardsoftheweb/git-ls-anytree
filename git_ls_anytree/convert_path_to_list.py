from os.path import split

def convert_path_to_list(path_to_explode):
    """Converts a path to a list exploded at the OS delimiters"""
    path_dirname, path_basename = split(path_to_explode)
    return (convert_path_to_list(path_dirname) if path_dirname else []) + [path_basename]
