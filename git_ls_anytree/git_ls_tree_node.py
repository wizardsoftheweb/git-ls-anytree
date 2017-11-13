"""This file provides the GitLsTreeNode class"""

from os.path import basename
from re import match, VERBOSE

from anytree import NodeMixin
from git_ls_anytree.convert_path_to_list import convert_path_to_list
from git_ls_anytree.local_exceptions import BrokenTreeError

class GitLsTreeNode(NodeMixin):
    """This class holds the methods necessary to create a node in the tree.

    It extends NodeMixin, adding anytree functionality. It assigns defaults,
    parses the raw git output, and can search its children for specific nodes.
    """

    FULL_GIT_PATTERN = r"""
^(?P<file_mode>             # Name the file_mode group
    \d{6}                   # git modes are six-digit numbers
)
\s+
(?P<item_type>              # Name the item_type group
    blob|tree|commit        # list of possible git items
)
\s+
(?P<git_object>             # Name the git_object group
    \w+                     # The hash could be 4-40 characters, maybe more
)
\s+
(?P<git_object_size>        # Name the git_object_size group
    [\d\-]+                 # The size in bytes of the object
)
\s+
(?P<relative_path>          # Name the relative_path group
    .*                      # Anything else until the end of the line is the path
)$
"""
    """This regex is used to parse the raw git output.

    `Official docs <https://git-scm.com/docs/git-ls-tree#_output_format>`__
    """

    def __init__(self, raw_git_output='', name='', parent=None):
        """Simple ctor; delegates processing to child methods

        Parameters:
        raw_git_output - The raw line from git (most likely via STDOUT)
        name - An optional name (mostly just for the root node)
        parent - The parent NodeMixin
        """
        super(GitLsTreeNode, self).__init__()
        self.file_mode = ''
        self.item_type = ''
        self.git_object = ''
        self.git_object_size = ''
        self.relative_path = ''
        self.basename = ''
        self.exploded_path = []
        self.process_raw_git_output(raw_git_output)
        self.name = name if name else self.basename
        self.parent = parent
        self.children = []

    def process_raw_git_output(self, raw_git_output):
        """Parses the git output into instance members

        Parameters:
        raw_git_output - The raw line from git (most likely via STDOUT)
        """
        self.raw = raw_git_output
        processed_groups = match(GitLsTreeNode.FULL_GIT_PATTERN, raw_git_output, VERBOSE)
        if processed_groups:
            self.file_mode = (
                processed_groups.group('file_mode')
                if processed_groups.group('file_mode')
                else self.file_mode
            )
            self.item_type = (
                processed_groups.group('item_type')
                if processed_groups.group('item_type')
                else self.item_type
            )
            self.git_object = (
                processed_groups.group('git_object')
                if processed_groups.group('git_object')
                else self.git_object
            )
            self.git_object_size = (
                processed_groups.group('git_object_size')
                if processed_groups.group('git_object_size')
                else self.git_object_size
            )
            self.relative_path = (
                processed_groups.group('relative_path')
                if processed_groups.group('relative_path')
                else self.relative_path
            )
            self.basename = (
                basename(processed_groups.group('relative_path'))
                if processed_groups.group('relative_path')
                else self.basename
            )
        if self.relative_path:
            self.exploded_path = convert_path_to_list(self.relative_path)

    def classify(self, short=True):
        """
        `Stack Overflow coverage <https://stackoverflow.com/a/8347325/2877698>`__
        """
        try:
            value = {
                '040000': {
                    'short': '/',
                    'long': 'directory'
                },
                '100644': {
                    'short': '',
                    'long': 'file'
                },
                '100664': {
                    'short': '',
                    'long': 'file'
                },
                '100755': {
                    'short': '*',
                    'long': 'executable'
                },
                '120000': {
                    'short': '@',
                    'long': 'symlink'
                },
                '160000': {
                    'short': '/',
                    'long': 'gitlink'
                }
            }[self.file_mode]
            return value['short'] if short else value['long']
        except KeyError:
            return ''

    def walk_to_parent_node(self, exploded_path):
        """Walks the branch until exploded_path is empty

        This assumes that git ls-tree has been called with -rt, to recurse
        everywhere and always print trees. It also assumes the tree is created
        from the parent directories downward.

        Parameters:
        exploded_path - The path list to search for
        """
        if 1 == len(exploded_path):
            return self
        else:
            current_basename = exploded_path.pop(0)
            for potential_parent in self.children:
                if current_basename == potential_parent.basename:
                    return potential_parent
                    # print potential_parent
            raise BrokenTreeError(self, current_basename)
