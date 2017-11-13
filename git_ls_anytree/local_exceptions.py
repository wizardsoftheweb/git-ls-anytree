"""This file provides the BrokenTreeError exception"""

class BrokenTreeError(Exception):
    """Raised when an unknown child appears while processing a tree

    Attributes:
        owning_node -- The node currently searching its children
        unknown_child -- The file or directory that cannot be found
    """

    def __init__(self, owning_node, unknown_child):
        super(BrokenTreeError, self).__init__()
        self.owning_node = owning_node
        self.unknown_child = unknown_child
        # full_path =
        self.msg = """\
The %s tree does not have a '%s' subtree or blob
""" % (
    ("'%s'" % (owning_node.relative_path) if owning_node.relative_path else 'root'),
    unknown_child
)

    def __str__(self):
        return self.msg
