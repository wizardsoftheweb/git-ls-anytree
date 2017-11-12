from os.path import join
from git_ls_anytree import GitLsTree

import argparse

with open(join('git_ls_anytree', 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

def cli():
    parser = argparse.ArgumentParser(
        description='Python tool to pretty-print git-ls-tree',
        epilog="""\
Due to known issues with nargs='?' consuming positionals under the right \
circumstances, --abbrev[=n] was split into --abbrev, for the default, and \
--abbrev-n INT, to specify a level.
"""
    )

    git_args = parser.add_argument_group('Inherited git-ls-tree arguments')

    git_args.add_argument(
        '--name-only', '--name-status',
        action='store_true',
        dest='name_only',
        help='Only print the tree structure per git-ls-tree --name-(only|status)'
    )

    git_abbrev_group = git_args.add_mutually_exclusive_group()

    # TODO: Pull core.abbrev
    git_abbrev_group.add_argument(
        '--abbrev',
        default=argparse.SUPPRESS,
        dest='abbrev',
        action='store_const',
        const=7,
        help='Equivalent to git-ls-tree --abbrev. Uses the default git short hash of seven characters.'
    )

    git_abbrev_group.add_argument(
        '--abbrev-n',
        nargs=1,
        dest='abbrev',
        type=int,
        default=argparse.SUPPRESS,
        help='Sets the git object abbreviation per git-ls-tree --abbrev=n'
    )

    git_args.add_argument(
        '-d', '--trees-only',
        action='store_true',
        dest='trees_only',
        help='Only print trees per git-ls-tree -d'
    )

    tree_args = parser.add_argument_group('Inherited tree arguments')

    tree_args.add_argument(
        '-F', '--classify',
        action='store_true',
        dest='classify',
        help='Appends ( *@/) to filename per ls -F'
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
