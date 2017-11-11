from anytree import NodeMixin, RenderTree
from git_ls_tree_node import GitLsTreeNode
from os import getcwd
from os.path import basename, split
from re import match
from subprocess import check_output

class GitLsTree(GitLsTreeNode):
    def __init__(self, tree_ish='HEAD', path_in_tree_ish='', working_dir=getcwd()):
        super(GitLsTree, self).__init__(name='root')
        self.working_dir = working_dir
        self.name = self.finalize_tree_ish(tree_ish, path_in_tree_ish)
        self.process_tree_ish()

    def finalize_tree_ish(self, tree_ish, path_in_tree_ish):
        return tree_ish + ((':' + path_in_tree_ish) if path_in_tree_ish else '')

    def query_tree_ish(self):
        raw_blob = check_output(
            ['git', 'ls-tree', self.name, '-rtl'],
            cwd=self.working_dir
        )
        return raw_blob.strip().split('\n')

    def parse_tree_ish(self, raw_lines):
        for raw_git_output in raw_lines:
            child_node = GitLsTreeNode(raw_git_output)
            child_node.parent = self.walk_to_parent_node(child_node.exploded_path)

    def process_tree_ish(self):
        raw_git = self.query_tree_ish()
        self.parse_tree_ish(raw_git)
