from os import getcwd
from os.path import join, dirname, realpath

__location__ = realpath(
    join(
        getcwd(),
        dirname(__file__)
    )
)

with open(join(__location__, 'VERSION')) as version_file:
    __version__ = version_file.read().strip()
