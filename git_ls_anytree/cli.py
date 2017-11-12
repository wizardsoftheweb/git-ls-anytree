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
        dest='name_only',
        help='Only print the tree structure per git-ls-tree --name-(only|status)'
    )

    parser.add_argument(
        '-F', '--classify',
        action='store_true',
        dest='classify',
        help='Appends ( *@/) per ls -F'
    )

    parser.add_argument(
        '-d', '--trees-only',
        action='store_true',
        dest='trees_only',
        help='Only print trees per git-ls-tree -d'
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
    full_tree = GitLsTree(
        tree_ish=args.TreeIsh,
        patterns=args.Patterns,
        trees_only=args.trees_only
    )
    full_tree.pretty_print(
        name_only=args.name_only,
        classify=args.classify
    )

if __name__ == '__main__':
    cli()
