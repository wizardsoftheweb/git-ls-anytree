class BrokenTreeError(Exception):
    def __init__(self, owning_node, unknown_child):
        self.owning_node = owning_node
        self.unknown_child = unknown_child
        full_path = owning_node.relative_path
        self.msg = "The '%(full_path)s' tree does not have a '%(unknown_child)s' subtree or blob" % locals()

    def __str__(self):
        return self.msg
