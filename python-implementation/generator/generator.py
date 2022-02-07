from parser import tree_node_kinds_
from parser import tree_node_


TreeNode = tree_node_.TreeNode
TreeNodeKind = tree_node_kinds_.TreeNodeKind


class Generator:
    def __init__(self, tree):
        self.tree = tree
        
