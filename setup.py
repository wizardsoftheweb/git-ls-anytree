from os.path import join
from setuptools import setup

with open(join('git_ls_anytree', 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

setup()
