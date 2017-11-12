from git_ls_anytree import GitLsTreeNode, BrokenTreeError
from mock import MagicMock, patch
import unittest

# Have to get the whole module to get patch to work correctly
# import git_ls_anytree
import os.path


class ConstructorUnitTests(unittest.TestCase):
    universal_basename = 'qqq'
    def setUp(self):
        self.dummy_input = 'qqq'
        basename_patcher = patch.object(os.path, 'basename', return_value=self.universal_basename)
        self.mock_basename = basename_patcher.start()
        self.addCleanup(basename_patcher.stop)
        self.process_patcher = patch.object(GitLsTreeNode, 'process_raw_git_output', return_value=None)
        self.mock_process = self.process_patcher.start()
        self.addCleanup(self.process_patcher.stop)

    def test_processes_git_input_properly(self):
        tree_instance = GitLsTreeNode(self.dummy_input)
        self.mock_process.assert_called_once_with(self.dummy_input)

    def test_processes_nothing_with_git_input(self):
        tree_instance = GitLsTreeNode(name=self.dummy_input)
        self.mock_process.assert_called_once_with('')

    def test_sets_default_values(self):
        tree_instance = GitLsTreeNode()
        for key in ['file_mode', 'basename', 'relative_path', 'item_type', 'git_object_size', 'git_object', 'name']:
            assert(getattr(tree_instance, key) == '')
        for list_key in ['exploded_path', 'children']:
            assert(len(getattr(tree_instance, list_key)) == 0)


class ProcessRawGitOutputUnitTests(unittest.TestCase):
    universal_basename = 'qqq'
    universal_path_list = ['path', 'to', 'file']

    sample_blob_raw = '100644 blob 9cea94b72d6a91e4775490f1c33d8aa1aa0a9a36     663    tests/test_convert_path_to_list.py'
    sample_blob_dict = {
        'file_mode': '100644',
        'item_type': 'blob',
        'git_object': '9cea94b72d6a91e4775490f1c33d8aa1aa0a9a36',
        'git_object_size': '663',
        'relative_path': 'tests/test_convert_path_to_list.py'
    }

    sample_tree_raw = '040000 tree 01e580291432cdb05640a25e59794ed196adfff1       -    git_ls_anytree'
    sample_tree_dict = {
        'file_mode': '040000',
        'item_type': 'tree',
        'git_object': '01e580291432cdb05640a25e59794ed196adfff1',
        'git_object_size': '-',
        'relative_path': 'git_ls_anytree'
    }

    def setUp(self):
        basename_patcher = patch('git_ls_anytree.git_ls_tree_node.basename', return_value=self.universal_basename)
        self.mock_basename = basename_patcher.start()
        self.addCleanup(basename_patcher.stop)
        convert_patcher = patch('git_ls_anytree.git_ls_tree_node.convert_path_to_list', return_value=self.universal_path_list)
        self.mock_convert = convert_patcher.start()
        self.addCleanup(convert_patcher.stop)
        process_patcher = patch.object(GitLsTreeNode, 'process_raw_git_output', return_value=None)
        process_patcher.start()
        self.tree_instance = GitLsTreeNode()
        process_patcher.stop()

    def test_parse_blob(self):
        self.tree_instance.process_raw_git_output(self.sample_blob_raw)
        for key, value in self.sample_blob_dict.iteritems():
            assert(getattr(self.tree_instance, key) == value)
        assert(getattr(self.tree_instance, 'basename') == self.universal_basename)
        assert(getattr(self.tree_instance, 'exploded_path') == self.universal_path_list)

    def test_parse_tree(self):
        self.tree_instance.process_raw_git_output(self.sample_tree_raw)
        for key, value in self.sample_tree_dict.iteritems():
            assert(getattr(self.tree_instance, key) == value)
        assert(getattr(self.tree_instance, 'basename') == self.universal_basename)
        assert(getattr(self.tree_instance, 'exploded_path') == self.universal_path_list)

    def test_parse_junk(self):
        self.tree_instance.process_raw_git_output('')
        for key, value in self.sample_tree_dict.iteritems():
            assert(getattr(self.tree_instance, key) == '')
        assert(getattr(self.tree_instance, 'basename') == '')

class WalkToParentNodeUnitTests(unittest.TestCase):
    def setUp(self):
        self.rootNode = GitLsTreeNode()
        setattr(self.rootNode, 'basename', 'root')
        self.leafNode = GitLsTreeNode(parent=self.rootNode)
        setattr(self.leafNode, 'basename', 'leaf')

    def test_base_case(self):
        assert(self.rootNode == self.rootNode.walk_to_parent_node(['file.ext']))
        assert(self.leafNode == self.leafNode.walk_to_parent_node(['file.ext']))

    def test_tree_traversal(self):
        assert(self.leafNode == self.rootNode.walk_to_parent_node(['leaf', 'file.ext']))

    def test_broken_tree_error(self):
        with self.assertRaises(BrokenTreeError) as context_manager:
            self.rootNode.walk_to_parent_node(['nope', 'file.ext'])
        assert("The '' tree does not have a 'nope' subtree or blob" == context_manager.exception.__str__())


# Truly necessary?
GitLsTreeNodeUnitSuite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(ConstructorUnitTests),
    unittest.TestLoader().loadTestsFromTestCase(ProcessRawGitOutputUnitTests)
])
