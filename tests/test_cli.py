from git_ls_anytree import cli, GitLsTree
from mock import MagicMock, patch

import argparse
import unittest
import os

class CliUnitTests(unittest.TestCase):
    universal_working_dir = 'local/path'

    def setUp(self):
        getcwd_patcher = patch('git_ls_anytree.cli_file.getcwd', return_value=self.universal_working_dir)
        self.mock_cwd = getcwd_patcher.start()
        self.addCleanup(getcwd_patcher.stop)
        tree_patcher = patch('git_ls_anytree.cli_file.GitLsTree')
        self.mock_tree = tree_patcher.start()
        self.addCleanup(tree_patcher.stop)

    def test_defaults(self):
        cli([])
        self.mock_tree.assert_any_call(
            tree_ish='HEAD',
            patterns=[],
            trees_only=False,
            working_dir=self.universal_working_dir,
            abbrev=None
        )
        self.mock_tree().pretty_print.assert_any_call(
            name_only=False,
            classify=False
        )

