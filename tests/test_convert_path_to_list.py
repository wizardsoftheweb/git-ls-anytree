from git_ls_anytree import convert_path_to_list

simple_basename = 'file.ext'
simple_directory = 'path/to/directory'

def test_basename_only():
    assert(convert_path_to_list(simple_basename) == [simple_basename])
    assert(convert_path_to_list('/' + simple_basename) == [simple_basename])

def test_simple_directory():
    assert(convert_path_to_list(simple_directory) == ['path', 'to', 'directory'])
    assert(convert_path_to_list('/' + simple_directory) == ['path', 'to', 'directory'])

def test_nt_paths_are_ignored():
    assert(convert_path_to_list('C:\WINDOWS\system32') == ['C:\WINDOWS\system32'])
