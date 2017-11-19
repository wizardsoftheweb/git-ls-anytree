"""Contains all the unit tests for GitLsTree"""
from collections import namedtuple
from re import search
from subprocess import CalledProcessError

import unittest
import sys

from mock import call, MagicMock, patch

from git_ls_anytree import BrokenTreeError, GitLsTree, GitLsTreeNode

class GitLsTreeTestBase(unittest.TestCase):
    universal_tree_ish = 'qqq'
    universal_working_dir = 'local/path'

    def wipe_tree_instance(self):
        del self.tree_instance

    def create_tree_instance(self):
        getcwd_patcher = patch('git_ls_anytree.git_ls_tree.getcwd', return_value=self.universal_working_dir)
        self.mock_cwd = getcwd_patcher.start()
        self.addCleanup(getcwd_patcher.stop)
        process_patcher = patch.object(GitLsTree, 'process_tree_ish', return_value=None)
        process_patcher.start()
        self.tree_instance = GitLsTree(self.universal_tree_ish)
        process_patcher.stop()
        self.addCleanup(self.wipe_tree_instance)

class ConstructorUnitTests(GitLsTreeTestBase):
    def setUp(self):
        node_patcher = patch('git_ls_anytree.git_ls_tree.GitLsTreeNode', wraps=GitLsTreeNode)
        self.mock_nodes = node_patcher.start()
        self.addCleanup(node_patcher.stop)
        getcwd_patcher = patch('git_ls_anytree.git_ls_tree.getcwd', return_value=self.universal_working_dir)
        self.mock_cwd = getcwd_patcher.start()
        self.addCleanup(getcwd_patcher.stop)
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

    def test_tree_ish_is_processed(self):
        self.tree_instance = GitLsTree()
        self.mock_process.assert_called_once_with()

    def test_assigned_name(self):
        self.tree_instance = GitLsTree()
        assert('HEAD' == self.tree_instance.name)
        self.tree_instance = GitLsTree(self.universal_tree_ish)
        assert(self.universal_tree_ish == self.tree_instance.name)

    def test_abbrev_assignment(self):
        self.tree_instance = GitLsTree()
        assert(GitLsTree.DEFAULT_ABBREV_LENGTH == self.tree_instance.abbrev_justification)
        assert([] == self.tree_instance.extra_opts)
        self.tree_instance = GitLsTree(abbrev=10)
        assert(10 == self.tree_instance.abbrev_justification)
        assert(['--abbrev=10'] == self.tree_instance.extra_opts)
        self.tree_instance = GitLsTree(abbrev=3)
        assert(GitLsTree.MINIMUM_ABBREV_JUSTIFICATION == self.tree_instance.abbrev_justification)
        assert(['--abbrev=3'] == self.tree_instance.extra_opts)

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
        subprocess_patcher = patch('git_ls_anytree.git_ls_tree.check_output', return_value=self.git_raw_output)
        self.mock_sub = subprocess_patcher.start()
        self.addCleanup(subprocess_patcher.stop)
        self.create_tree_instance()

    def test_subprocess_integration(self):
        self.tree_instance.query_tree_ish()
        self.mock_sub.assert_called_once_with(
            GitLsTree.BASE_GIT_LS_TREE_CALL + [self.universal_tree_ish],
            cwd=self.universal_working_dir
        )

    def test_subprocess_return(self):
        result = self.tree_instance.query_tree_ish()
        assert(self.number_of_git_lines == len(result))
        assert(search(r'\S', result[-1]))

    def test_subprocess_git_failure(self):
        error_dict = {
            'returncode': 128,
            'cmd': GitLsTree.BASE_GIT_LS_TREE_CALL + ['mxyzptlk'],
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
        self.create_tree_instance()

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

    def test_broken_tree_error(self):
        with self.assertRaises(BrokenTreeError) as context_manager:
            self.tree_instance.parse_tree_ish(self.intentionally_broken_input)
        self.assertRegexpMatches(
            context_manager.exception.__str__(),
            r"The (?:root|'.*?') tree does not have a '.*?' subtree or blob"
        )

class ProcessTreeIshUnitTests(GitLsTreeTestBase):
    raw_items = ['raw', 'is', 'war']

    def setUp(self):
        self.mock_nodes = MagicMock(wraps=GitLsTreeNode)
        query_patcher = patch.object(GitLsTree, 'query_tree_ish', return_value=self.raw_items)
        self.mock_query = query_patcher.start()
        self.addCleanup(query_patcher.stop)
        parse_patcher = patch.object(GitLsTree, 'parse_tree_ish', return_value=self.raw_items)
        self.mock_parse = parse_patcher.start()
        self.addCleanup(parse_patcher.stop)
        self.create_tree_instance()

    def test_query_called(self):
        self.tree_instance.process_tree_ish()
        self.mock_query.assert_called_once_with()

    def test_parse_called(self):
        self.tree_instance.process_tree_ish()
        self.mock_parse.assert_called_once_with(self.raw_items)

class RenderToListUnitTests(GitLsTreeTestBase):
    exploded_input = [
        '100644 blob   d6692984ebddd76ae0a5e7c4da181b4b3f61c9da  1051    README.rst',
        '040000 tree   b797423bbb11b5a485c91b63cec2cae5bdb80ebf     -    git_ls_anytree',
        '100664 blob   77d6f4ca23711533e724789a0a0045eab28c5ea6     6    git_ls_anytree/VERSION',
        '100755 blob   69b140ebd030332bdccc274ad9b92e9df1d225d9    20    executable',
        '120000 blob   19f0b03ae279fc7da9bdff15295c3585d71f6d1e    16    symlink',
        '160000 commit ad522a091429ba180c930f84b2a023b40de4dbcc     -    external-submodule'
    ]

    def setUp(self):
        self.create_tree_instance()

    def test_line_encoding(self):
        self.tree_instance.parse_tree_ish(self.exploded_input)
        for result in self.tree_instance.render_to_list():
            try:
                result['line'].decode('utf-8', 'strict')
            except UnicodeError:
                self.fail("Unable to decode unicode")

    def test_name_justification(self):
        self.tree_instance.name = '0123456789'
        result = self.tree_instance.render_to_list()[0]
        assert(10 == len(result['line']))
        self.tree_instance.file_mode = '040000'
        result = self.tree_instance.render_to_list(classify=True)[0]
        assert(11 == len(result['line']))

    def test_abbrev_justification(self):
        result = self.tree_instance.render_to_list()[0]
        assert(GitLsTree.DEFAULT_ABBREV_LENGTH == len(result['object']))
        self.tree_instance.abbrev_justification = 10
        result = self.tree_instance.render_to_list()[0]
        assert(10 == len(result['object']))

    def test_size_justification(self):
        self.tree_instance.git_object_size = '1234'
        result = self.tree_instance.render_to_list()[0]
        assert(4 == len(result['size']))

    def test_other_justification(self):
        result = self.tree_instance.render_to_list()[0]
        assert(6 == len(result['mode']))
        assert(6 == len(result['type']))

class PrettyPrintUnitTests(GitLsTreeTestBase):
    output_list = [
        {
            'object': 'object                                  ',
            'depth': 0,
            'mode': 'mode  ',
            'line': 'qqq                   ',
            'type': 'type  ',
            '_': u'',
            'size': 'size'
        },
        {
            'object': 'd6692984ebddd76ae0a5e7c4da181b4b3f61c9da',
            'depth': 1,
            'mode': '100644',
            'line': '\xe2\x94\x9c\xe2\x94\x80\xe2\x94\x80 README.rst        ',
            'type': 'blob  ',
            '_': u'\u2502   ',
            'size': '1051'
        }
    ]

    def reset_stdout(self):
        sys.stdout = sys.__stdout__

    def setUp(self):
        self.mock_stdout = MagicMock()
        sys.stdout = self.mock_stdout
        self.addCleanup(self.reset_stdout)
        render_patcher = patch.object(GitLsTree, 'render_to_list', return_value=self.output_list)
        self.mock_render = render_patcher.start()
        self.addCleanup(render_patcher.stop)
        self.create_tree_instance()

    def test_pass_classify_to_render(self):
        self.tree_instance.pretty_print()
        self.mock_render.assert_called_once_with(False)
        for classify in [True, False]:
            self.mock_render.reset_mock()
            self.tree_instance.pretty_print(classify=classify)
            self.mock_render.assert_called_once_with(classify)

    def test_name_only(self):
        self.tree_instance.pretty_print(name_only=True)
        self.mock_stdout.assert_has_calls([
            call.write(self.output_list[0]['line']),
            call.write('\n'),
            call.write(self.output_list[1]['line']),
            call.write('\n')
        ])

    def test_full_print(self):
        self.tree_instance.pretty_print()
        self.reset_stdout()
        self.mock_stdout.assert_has_calls([
            call.write('%s\t%s\t%s\t%s\t%s' % (
                self.output_list[0]['mode'],
                self.output_list[0]['type'],
                self.output_list[0]['object'],
                self.output_list[0]['size'],
                self.output_list[0]['line']
            )),
            call.write('\n'),
            call.write('%s\t%s\t%s\t%s\t%s' % (
                self.output_list[1]['mode'],
                self.output_list[1]['type'],
                self.output_list[1]['object'],
                self.output_list[1]['size'],
                self.output_list[1]['line']
            )),
            call.write('\n')
        ])

