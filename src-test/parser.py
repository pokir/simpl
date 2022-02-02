from enums import TreeNodeKind
from tree_node import TreeNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

        self.position = 0
        self.tree = TreeNode(TreeNodeKind.ROOT)

    def token(self):
        try:
            return self.tokens[self.position]
        except IndexError:
            return None

    def next_token(self):
        try:
            return self.tokens[self.position + 1]
        except IndexError:
            return None

    def parse(self):
        # TODO: create the AST here
        while self.token() != None:
            self.position += 1
'''
    def _any(self):
        

    def _numeric_literal()
'''
