from anytree import NodeMixin, RenderTree
from git_ls_tree_node import GitLsTreeNode
from os import getcwd
from subprocess import check_output

class GitLsTree(GitLsTreeNode):
    """This class builds an anytree from git ls-tree

    Using the provided tree-ish, the class queries git, explodes STDOUT, and
    builds an anytree from the result
    """

    def __init__(self, tree_ish='HEAD', subtrees=[], working_dir=None):
        """Ctor with defaults

        Parameters:
        tree_ish - The reference to probe
        path_in_tree_ish - An optional subpath that can be used to shrink the search
        working_dir - The location of the git repo to query; defaults to getcwd()
        """
        super(GitLsTree, self).__init__(name='root')
        self.working_dir = working_dir if working_dir else getcwd()
        self.name = tree_ish
        self.subtrees = subtrees
        self.process_tree_ish()

    def query_tree_ish(self):
        """Spawns a subprocess to in working_dir to run git ls-tree; strips and
        splits the result
        """
        raw_blob = check_output(
            ['git', 'ls-tree', '-rtl', self.name] + self.subtrees,
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

    def render_to_list(self):
        output = []
        for pre, _, node in RenderTree(self):
            printed_name = node.name if node.name else node.basename
            output += [u'%s%s' % (pre, printed_name)]
        return output

    def pretty_print(self):
        for tree_line in self.render_to_list():
            print tree_line.encode('utf-8')
