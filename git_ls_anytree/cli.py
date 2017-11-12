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

    # TODO: Pull core.abbrev
    parser.add_argument(
        '--default-abbrev',
        default=argparse.SUPPRESS,
        dest='abbrev',
        action='store_const',
        const=7,
        help='Equivalent to git-ls-tree --abbrev. Uses the default git short hash of seven characters.'
    )

    parser.add_argument(
        '--abbrev',
        nargs=1,
        type=int,
        default=argparse.SUPPRESS,
        help='Sets the git object abbreviation per git-ls-tree --abbrev=n'
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
        'tree_ish',
        metavar='tree-ish',
        nargs='?',
        type=str,
        default='HEAD',
        help='Reference to tree-ish'
    )

    parser.add_argument(
        'patterns',
        nargs='*',
        default=[],
        help='Subtrees within the main tree-ish'
    )

    args = parser.parse_args()
    print args
    # full_tree = GitLsTree(
    #     tree_ish=args.tree_ish,
    #     patterns=args.patterns,
    #     trees_only=args.trees_only
    # )
    # full_tree.pretty_print(
    #     name_only=args.name_only,
    #     classify=args.classify
    # )

if __name__ == '__main__':
    cli()
