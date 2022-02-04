from grammar import grammar
from parser import tree_node_kinds_
from parser import tree_node_
from lexer import token_kinds_


Grammar = grammar.Grammar
TokenKind = token_kinds_.TokenKind
#TreeNode = tree_node_.TreeNode
TreeNodeKind = tree_node_kinds_.TreeNodeKind


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

        #self.tree = TreeNode(TreeNodeKind.ROOT)
        self.tree = {}
        self.current_tree_node = self.tree

    def token(self):
        try:
            return self.tokens[self.position]
        except IndexError:
            return None

    def relative_token(self, offset):
        try:
            return self.tokens[self.position + offset]
        except IndexError:
            return None

    def parse(self):
        self.current_tree_node['kind'] = TreeNodeKind.ROOT
        self.current_tree_node['body'] = [{}]
        self.current_tree_node = self.current_tree_node['body'][0]

        # TODO: create the AST here
        while self.token() != None:
            if self.token().kind == TokenKind.NUMBER:
                self._numeric_literal()
            elif self.token().kind == TokenKind.STRING:
                self._string_literal()
            elif self.token().kind == TokenKind.BOOLEAN:
                self._boolean_literal()

            self.position += 1

