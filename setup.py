from os.path import join
from setuptools import setup, find_packages

with open(join('git_ls_anytree', 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

setup(
    name='git_ls_anytree',
    version=__version__,
    packages=find_packages(),
    package_data={
        '': ['VERSION']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'git-ls-anytree = git_ls_anytree.cli_file:cli'
        ]
    }
)
