class BrokenTreeError(Exception):
    """Raised when an unknown child appears while processing a tree

    Attributes:
        owning_node -- The node currently searching its children
        unknown_child -- The file or directory that cannot be found
    """

    def __init__(self, owning_node, unknown_child):
        self.owning_node = owning_node
        self.unknown_child = unknown_child
        full_path = "'%s'" % (owning_node.relative_path) if owning_node.relative_path else 'root'
        self.msg = "The %(full_path)s tree does not have a '%(unknown_child)s' subtree or blob" % locals()

    def __str__(self):
        return self.msg
