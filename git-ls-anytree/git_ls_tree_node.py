from anytree import NodeMixin
from convert_path_to_list import convert_path_to_list
from local_exceptions import BrokenTreeError
from os.path import basename
from re import match

class GitLsTreeNode(NodeMixin):
    FULL_GIT_PATTERN = r'^(?P<file_mode>\d{6})\s+(?P<item_type>blob|tree)\s+(?P<git_object>\w+)\s+(?P<git_object_size>[\d\-]+)\s+(?P<relative_path>.*)$'

    def __init__(self, raw_git_output='', name='', parent=None):
        super(GitLsTreeNode, self).__init__()
        self.file_mode = ''
        self.item_type = ''
        self.git_object = ''
        self.git_object_size = ''
        self.relative_path = ''
        self.basename = ''
        self.exploded_path = []
        self.process_raw_git_output(raw_git_output)
        self.name = name if name else self.basename
        self.parent = parent
        self.children = []

    def process_raw_git_output(self, raw_git_output):
        self.raw = raw_git_output
        processed_groups = match(GitLsTreeNode.FULL_GIT_PATTERN, raw_git_output)
        if processed_groups:
            self.file_mode = processed_groups.group('file_mode') if processed_groups.group('file_mode') else self.file_mode
            self.item_type = processed_groups.group('item_type') if processed_groups.group('item_type') else self.item_type
            self.git_object = processed_groups.group('git_object') if processed_groups.group('git_object') else self.git_object
            self.git_object_size = processed_groups.group('git_object_size') if processed_groups.group('git_object_size') else self.git_object_size
            self.relative_path = processed_groups.group('relative_path') if processed_groups.group('relative_path') else self.relative_path
            self.basename = basename(processed_groups.group('relative_path')) if processed_groups.group('relative_path') else self.basename
        if self.relative_path:
            self.exploded_path = convert_path_to_list(self.relative_path)

    def walk_to_parent_node(self, exploded_path):
        if 1 == len(exploded_path):
            return self
        else:
            current_basename = exploded_path.pop(0)
            for potential_parent in self.children:
                if current_basename == potential_parent.basename:
                    return potential_parent
                    # print potential_parent
            raise BrokenTreeError(self, current_basename)

