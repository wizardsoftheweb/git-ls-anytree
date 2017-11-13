"""This file provides GitLsTree"""

from os import getcwd
from subprocess import check_output

from anytree import RenderTree
from git_ls_anytree.git_ls_tree_node import GitLsTreeNode

class GitLsTree(GitLsTreeNode):
    """This class builds an anytree from git ls-tree

    Using the provided tree-ish, the class queries git, explodes STDOUT, and
    builds an anytree from the result
    """

    BASE_GIT_LS_TREE_CALL = ['git', 'ls-tree', '-rtl', '--full-tree']
    MINIMUM_ABBREV_JUSTIFICATION = 6
    DEFAULT_ABBREV_LENGTH = 40

    def __init__(
            self,
            tree_ish='HEAD',
            patterns=None,
            trees_only=False,
            working_dir=None,
            abbrev=None
        ):
        """Ctor with defaults

        Parameters:
        tree_ish - The reference to probe
        path_in_tree_ish - An optional subpath that can be used to shrink the search
        working_dir - The location of the git repo to query; defaults to getcwd()
        """
        super(GitLsTree, self).__init__(name='root')
        self.working_dir = working_dir if working_dir else getcwd()
        self.name = tree_ish
        self.file_mode = 'mode'
        self.item_type = 'type'
        self.git_object = 'object'
        self.git_object_size = 'size'
        self.patterns = (
            patterns
            if patterns
            else []
        )
        self.extra_opts = ['-d'] if trees_only else []
        if abbrev:
            self.extra_opts += ['--abbrev=%s' % int(abbrev)] if 0 <= int(abbrev) else []
            self.abbrev_justification = (
                int(abbrev)
                if self.MINIMUM_ABBREV_JUSTIFICATION <= int(abbrev)
                else self.MINIMUM_ABBREV_JUSTIFICATION
            )
        else:
            self.abbrev_justification = self.DEFAULT_ABBREV_LENGTH
        self.process_tree_ish()

    def query_tree_ish(self):
        """Spawns a subprocess to in working_dir to run git ls-tree; strips and
        splits the result
        """
        raw_blob = check_output(
            self.BASE_GIT_LS_TREE_CALL + self.extra_opts + [self.name] + self.patterns,
            cwd=self.working_dir
        )
        return raw_blob.strip().split('\n')

    def parse_tree_ish(self, raw_lines):
        """Creates a new node with the proper parent for each item found"""
        for raw_git_output in raw_lines:
            child_node = GitLsTreeNode(raw_git_output)
            child_node.parent = self.walk_to_parent_node(child_node.exploded_path)

    def process_tree_ish(self):
        """Queries git and builds the tree"""
        raw_git = self.query_tree_ish()
        self.parse_tree_ish(raw_git)

    def render_to_list(self, classify=False):
        """Renders the full anytree to a list with important variables"""
        max_name_length = 0
        max_size_length = 0
        output = []
        for pre, _, node in RenderTree(self):
            printed_name = node.name if node.name else node.basename
            classification = node.classify(short=True) if classify else ''
            current_node = (u'%s%s%s' % (pre, printed_name, classification)).encode('utf-8')
            current_name_length = len(current_node.decode('utf-8'))
            max_name_length = (
                current_name_length
                if max_name_length < current_name_length
                else max_name_length
            )
            max_size_length = (
                len(node.git_object_size)
                if max_size_length < len(node.git_object_size)
                else max_size_length
            )
            output += [{
                'line': current_node,
                '_': _,
                'mode': node.file_mode.ljust(6),
                'type': node.item_type.ljust(6),
                'object': node.git_object.ljust(self.abbrev_justification),
                'size': node.git_object_size,
                'depth': node.depth
            }]
        for tree_line in output:
            tree_line['line'] = (
                tree_line['line']
                .decode('utf-8')
                .ljust(max_name_length)
                .encode('utf-8')
            )
            tree_line['size'] = tree_line['size'].rjust(max_size_length)
        return output

    def pretty_print(self, name_only=False, classify=False):
        """Prints the rendered list"""
        for tree_line in self.render_to_list(classify):
            if name_only:
                print tree_line['line']
            else:
                print '%s\t%s\t%s\t%s\t%s' % (
                    tree_line['mode'],
                    tree_line['type'],
                    tree_line['object'],
                    tree_line['size'],
                    tree_line['line']
                )
