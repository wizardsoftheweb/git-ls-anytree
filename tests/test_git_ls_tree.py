from git_ls_anytree import GitLsTree, GitLsTreeNode
from mock import MagicMock, patch
import unittest
import os

class GitLsTreeTestBase(unittest.TestCase):
    universal_tree_ish = 'qqq'
    universal_working_dir = 'local/path'

class ConstructorUnitTests(GitLsTreeTestBase):
    def setUp(self):
        # self.mock_tree_nodes = MagicMock(wraps=GitLsTreeNode)
        getcwd_patcher = patch('git_ls_anytree.git_ls_tree.getcwd', return_value=self.universal_working_dir)
        # getcwd_patcher = patch.object(os, 'getcwd', return_value=self.universal_working_dir)
        self.mock_cwd = getcwd_patcher.start()
        self.addCleanup(getcwd_patcher.stop)
        finalize_patcher = patch.object(GitLsTree, 'finalize_tree_ish', return_value=self.universal_tree_ish)
        self.mock_finalize = finalize_patcher.start()
        self.addCleanup(finalize_patcher.stop)
        process_patcher = patch.object(GitLsTree, 'process_tree_ish', return_value=None)
        self.mock_process = process_patcher.start()
        self.addCleanup(process_patcher.stop)

    def test_working_dir(self):
        tree_instance = GitLsTree()
        assert(getattr(tree_instance, 'working_dir') == self.universal_working_dir)
        not_default_path = 'some/other/path'
        tree_instance = GitLsTree(working_dir=not_default_path)
        assert(getattr(tree_instance, 'working_dir') == not_default_path)

    def test_finalized_tree_ish(self):
        tree_instance = GitLsTree()
        self.mock_finalize.assert_called_once_with('HEAD', '')
        self.mock_finalize.reset_mock()
        tree_instance = GitLsTree(self.universal_tree_ish, self.universal_working_dir)
        self.mock_finalize.assert_called_once_with(self.universal_tree_ish, self.universal_working_dir)

    def test_tree_ish_is_processed(self):
        tree_instance = GitLsTree()
        self.mock_process.assert_called_once_with()

# class FinalizeTreePathUnitTests(GitLsTreeTestBase):
#     def setUp(self):
#         finalize_patcher = patch.object(GitLsTree, 'finalize_tree_ish', return_value=self.universal_tree_ish)
#         self.mock_finalize = finalize_patcher.start()
#         process_patcher = patch.object(GitLsTree, 'process_tree_ish', return_value=None)
#         self.mock_process = process_patcher.start()
#         self.tree_instance = GitLsTree()
#         finalize_patcher.stop()
#         process_patcher.stop()


#     def test_with_reference_only(self):
#         assert(self.universal_tree_ish == self.tree_instance.finalize_tree_ish(self.universal_tree_ish))
#         assert(self.universal_tree_ish == self.tree_instance.finalize_tree_ish(self.universal_tree_ish, ''))
