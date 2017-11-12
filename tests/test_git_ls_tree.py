from anytree import RenderTree
from git_ls_anytree import BrokenTreeError, GitLsTree, GitLsTreeNode
from mock import MagicMock, patch
from re import search

import unittest
import os

from subprocess import CalledProcessError, check_output

class GitLsTreeTestBase(unittest.TestCase):
    universal_tree_ish = 'qqq'
    universal_working_dir = 'local/path'

class ConstructorUnitTests(GitLsTreeTestBase):
    def setUp(self):
        node_patcher = patch('git_ls_anytree.git_ls_tree.GitLsTreeNode', wraps=GitLsTreeNode)
        self.mock_nodes = node_patcher.start()
        self.addCleanup(node_patcher.stop)
        getcwd_patcher = patch('git_ls_anytree.git_ls_tree.getcwd', return_value=self.universal_working_dir)
        self.mock_cwd = getcwd_patcher.start()
        self.addCleanup(getcwd_patcher.stop)
        finalize_patcher = patch.object(GitLsTree, 'finalize_tree_ish', return_value=self.universal_tree_ish)
        self.mock_finalize = finalize_patcher.start()
        self.addCleanup(finalize_patcher.stop)
        process_patcher = patch.object(GitLsTree, 'process_tree_ish', return_value=None)
        self.mock_process = process_patcher.start()
        self.addCleanup(process_patcher.stop)

    def tearDown(self):
        del self.tree_instance

    def test_working_dir(self):
        self.tree_instance = GitLsTree()
        assert(getattr(self.tree_instance, 'working_dir') == self.universal_working_dir)
        not_default_path = 'some/other/path'
        self.tree_instance = GitLsTree(working_dir=not_default_path)
        assert(getattr(self.tree_instance, 'working_dir') == not_default_path)

    def test_finalized_tree_ish(self):
        self.tree_instance = GitLsTree()
        self.mock_finalize.assert_called_once_with('HEAD', '')
        self.mock_finalize.reset_mock()
        self.tree_instance = GitLsTree(self.universal_tree_ish, self.universal_working_dir)
        self.mock_finalize.assert_called_once_with(self.universal_tree_ish, self.universal_working_dir)

    def test_tree_ish_is_processed(self):
        self.tree_instance = GitLsTree()
        self.mock_process.assert_called_once_with()

    def test_assigned_name(self):
        self.tree_instance = GitLsTree()
        assert(self.universal_tree_ish == self.tree_instance.name)

class FinalizeTreeIshUnitTests(GitLsTreeTestBase):
    def setUp(self):
        finalize_patcher = patch.object(GitLsTree, 'finalize_tree_ish', return_value=self.universal_tree_ish)
        self.mock_finalize = finalize_patcher.start()
        process_patcher = patch.object(GitLsTree, 'process_tree_ish', return_value=None)
        self.mock_process = process_patcher.start()
        self.tree_instance = GitLsTree()
        finalize_patcher.stop()
        process_patcher.stop()

    def test_with_reference_only(self):
        assert(self.universal_tree_ish == self.tree_instance.finalize_tree_ish(self.universal_tree_ish))
        assert(self.universal_tree_ish == self.tree_instance.finalize_tree_ish(self.universal_tree_ish, ''))

    def test_with_reference_only(self):
        assert(u"'%s:%s' == self.tree_instance.finalize_tree_ish(self.universal_tree_ish, self.universal_working_dir)" % (self.universal_tree_ish, self.universal_working_dir))

class QueryTreeIshUnitTests(GitLsTreeTestBase):
    number_of_git_lines = 20
    git_raw_output = """
100644 blob b2b08205406055d9cd6211792abff6fd56297ef1     184    .editorconfig
100644 blob 9744e3bfe565f435e7d7a1fa81f1748d93d3fd0e    1291    .gitignore
100644 blob 15dcd9397ddb753f2120b21c63d69f45bf5dda97     272    .travis.yml
100644 blob 93bb548d99173d68be2dc8a8086dcbbaff68da64     724    LICENSE.rst
100644 blob 9413fbf5533ee43f014ff9e6d6f0a6dac6cfd694      64    MANIFEST.in
100644 blob d6692984ebddd76ae0a5e7c4da181b4b3f61c9da    1051    README.rst
040000 tree b797423bbb11b5a485c91b63cec2cae5bdb80ebf       -    git_ls_anytree
100644 blob 77d6f4ca23711533e724789a0a0045eab28c5ea6       6    git_ls_anytree/VERSION
100644 blob 6feadffffec41aacacec0e6300d9f602bc7f75c5     180    git_ls_anytree/__init__.py
100644 blob a90da6caa03a918d4fa2074b03627fc31021b947     356    git_ls_anytree/convert_path_to_list.py
100644 blob eb3a9d914caec08f23c3c2e9676bfb5acdc5ef6e    1910    git_ls_anytree/git_ls_tree.py
100644 blob 112b337a9073c60b4f3ffa508f51975e9b5b5496    3550    git_ls_anytree/git_ls_tree_node.py
100644 blob db2531dc8a2748320c4c95dbdd1d0917b3904398     598    git_ls_anytree/local_exceptions.py
100644 blob 9742aa42db046b48db0f8cb0e86ff9c15f1f91d1     391    setup.cfg
100644 blob c73e374d4385265888116b49fb75ca98c3e754af     172    setup.py
040000 tree 9a5fad7f9a27eb0e2966a012b786de186da4b050       -    tests
100644 blob eb2a9dd1a83890cd6c1bc70eff1d15f29190c0ce     609    tests/test_convert_path_to_list.py
100644 blob 66c472e4152e174204f75cbe604d7012cf43301d    2847    tests/test_git_ls_tree.py
100644 blob 7f62c6429538b54d99887996dd9b84b255d97f8b    4596    tests/test_git_ls_tree_node.py
100644 blob c5389bc4255ba16d8771883046f8c3d95626d4d1     152    tox.ini

"""

    def setUp(self):
        getcwd_patcher = patch('git_ls_anytree.git_ls_tree.getcwd', return_value=self.universal_working_dir)
        self.mock_cwd = getcwd_patcher.start()
        self.addCleanup(getcwd_patcher.stop)
        finalize_patcher = patch.object(GitLsTree, 'finalize_tree_ish', return_value=self.universal_tree_ish)
        finalize_patcher.start()
        process_patcher = patch.object(GitLsTree, 'process_tree_ish', return_value=None)
        process_patcher.start()
        self.tree_instance = GitLsTree()
        finalize_patcher.stop()
        process_patcher.stop()
        subprocess_patcher = patch('git_ls_anytree.git_ls_tree.check_output', return_value=self.git_raw_output)
        self.mock_sub = subprocess_patcher.start()
        self.addCleanup(subprocess_patcher.stop)

    def test_subprocess_integration(self):
        self.tree_instance.query_tree_ish()
        self.mock_sub.assert_called_once_with(
            ['git', 'ls-tree', self.universal_tree_ish, '-rtl'],
            cwd=self.universal_working_dir
        )

    def test_subprocess_return(self):
        result = self.tree_instance.query_tree_ish()
        assert(self.number_of_git_lines == len(result))
        assert(search(r'\S', result[-1]))

    def test_subprocess_git_failure(self):
        error_dict = {
            'returncode': 128,
            'cmd': ['git', 'ls-tree', 'mxyzptlk', '-rtl'],
            'output': None
        }
        self.mock_sub.side_effect = CalledProcessError(**error_dict)
        with self.assertRaises(CalledProcessError) as context_manager:
            result = self.tree_instance.query_tree_ish()
        for key, value in error_dict.iteritems():
            assert(value == getattr(context_manager.exception, key))
        self.mock_sub.side_effect = None

class ParseTreeIshUnitTests(GitLsTreeTestBase):
    exploded_input = [
        '100644 blob d6692984ebddd76ae0a5e7c4da181b4b3f61c9da    1051    README.rst',
        '040000 tree b797423bbb11b5a485c91b63cec2cae5bdb80ebf       -    git_ls_anytree',
        '100644 blob 77d6f4ca23711533e724789a0a0045eab28c5ea6       6    git_ls_anytree/VERSION'
    ]

    intentionally_broken_input = [
        '100644 blob d6692984ebddd76ae0a5e7c4da181b4b3f61c9da    1051    README.rst',
        '100644 blob 77d6f4ca23711533e724789a0a0045eab28c5ea6       6    git_ls_anytree/VERSION'
    ]

    def setUp(self):
        self.mock_nodes = MagicMock(wraps=GitLsTreeNode)
        getcwd_patcher = patch('git_ls_anytree.git_ls_tree.getcwd', return_value=self.universal_working_dir)
        self.mock_cwd = getcwd_patcher.start()
        self.addCleanup(getcwd_patcher.stop)
        finalize_patcher = patch.object(GitLsTree, 'finalize_tree_ish', return_value=self.universal_tree_ish)
        finalize_patcher.start()
        process_patcher = patch.object(GitLsTree, 'process_tree_ish', return_value=None)
        process_patcher.start()
        self.tree_instance = GitLsTree()
        finalize_patcher.stop()
        process_patcher.stop()

    def test_generated_root_node(self):
        self.tree_instance.parse_tree_ish(self.exploded_input)
        for descendant in self.tree_instance.descendants:
            assert(self.tree_instance == descendant.root)

    def test_generated_relationships(self):
        self.tree_instance.parse_tree_ish(self.exploded_input)
        assert(2 == len(self.tree_instance.children))
        assert(0 == self.tree_instance.depth)
        for immediate_child in self.tree_instance.children:
            assert(1 == immediate_child.depth)
            if 'blob' == immediate_child.item_type:
                self.assertTrue(immediate_child.is_leaf)
            else:
                self.assertFalse(immediate_child.is_leaf)
                for grand_children in immediate_child.children:
                    assert(2 == grand_children.depth)

    # def test_broken_tree_error(self):
    #     with self.assertRaises(BrokenTreeError) as context_manager:
    #         self.tree_instance.parse_tree_ish(self.intentionally_broken_input)
    #     assert("The '' tree does not have a 'nope' subtree or blob" == context_manager.exception.__str__())
