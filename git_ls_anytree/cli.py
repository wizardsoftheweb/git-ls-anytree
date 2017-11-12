from os.path import join
from git_ls_anytree import GitLsTree

import argparse

with open(join('git_ls_anytree', 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

def cli():
    parser = argparse.ArgumentParser(
        description='Python tool to pretty-print git-ls-tree'
    )

    parser.add_argument(
        '--name-only', '--name-status',
        action='store_true',
        dest='name_only'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%s' % __version__
    )

    parser.add_argument(
        'TreeIsh',
        nargs='?',
        type=str,
        default='HEAD',
        help='Reference to tree-ish'
    )

    parser.add_argument(
        'Patterns',
        nargs='*',
        default=[],
        help='Subtrees within the main tree-ish'
    )

    args = parser.parse_args()

if __name__ == '__main__':
    cli()
