from os.path import join

import argparse

with open(join('git_ls_anytree', 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

def cli():
    parser = argparse.ArgumentParser(
        description='Python tool to pretty-print git-ls-tree'
    )

    parser.add_argument(
        'TreeIsh',
        nargs='?',
        type=str,
        default='HEAD',
        help='Reference to tree-ish'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%s' % __version__
    )

    args = parser.parse_args()
    print args

if __name__ == '__main__':
    cli()
