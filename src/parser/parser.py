from parser import tree_node_kinds_
from parser import tree_node_
from lexer import token_kinds_
from errors import errors 


TokenKind = token_kinds_.TokenKind
TreeNode = tree_node_.TreeNode
TreeNodeKind = tree_node_kinds_.TreeNodeKind
throw_error = errors.throw_error
ErrorKind = errors.ErrorKind


class Parser:
    def __init__(self, filename, source, tokens):
        self.filename = filename
        self.source = source # the raw code so that it can show errors
        self.tokens = tokens
        self.position = 0

        self.tree = TreeNode(TreeNodeKind.ROOT,
                             tokens[0].start,
                             tokens[-1].end,
                             children=[])

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
        # create the AST here
        while self.token().kind is not TokenKind.END_OF_FILE:
            statement = self._statement()
            if statement is None: # position has not incremented is it is None
                throw_error(self.filename, self.source, ErrorKind.INVALID_SYNTAX, self.token().start, self.token().end)

            self.tree.add_child(statement)

    def _numeric_literal(self):
        if self.token().kind == TokenKind.NUMBER:
            self.position += 1
            return TreeNode(TreeNodeKind.NUMERIC_LITERAL,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end,
                            raw=self.relative_token(-1).literal,
                            value=float(self.relative_token(-1).literal))

    def _string_literal(self):
        if self.token().kind == TokenKind.STRING:
            self.position += 1
            return TreeNode(TreeNodeKind.STRING_LITERAL, 
                            self.relative_token(-1).start,
                            self.relative_token(-1).end,
                            raw=self.relative_token(-1).literal,
                            value=self.relative_token(-1).literal[1:-1])

    def _boolean_literal(self):
        if self.token().kind == TokenKind.BOOLEAN:
            self.position += 1
            return TreeNode(TreeNodeKind.BOOLEAN_LITERAL,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end,
                            raw=self.relative_token(-1).literal,
                            value=self.relative_token(-1).literal == 'T')

    def _literal(self):
        return self._numeric_literal() \
               or self._string_literal() \
               or self._boolean_literal()

    def _identifier(self):
        if self.token().kind == TokenKind.IDENTIFIER:
            self.position += 1
            return TreeNode(TreeNodeKind.IDENTIFIER,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end,
                            raw=self.relative_token(-1).literal,
                            value=self.relative_token(-1).literal)

    def _statement(self, in_loop=False, in_function=False):
        return self._push_statement() \
               or self._pop_statement() \
               \
               or self._add_operation() \
               or self._subtract_operation() \
               or self._multiply_operation() \
               or self._divide_operation() \
               or self._modulo_operation() \
               \
               or self._equals_operation() \
               or self._not_equals_operation() \
               or self._greater_operation() \
               or self._less_operation() \
               or self._greater_equals_operation() \
               or self._less_equals_operation() \
               \
               or self._if_statement(in_loop, in_function) \
               or self._else_statement(in_loop, in_function) \
               \
               or self._loop_statement(in_function) \
               or self._continue_statement(in_loop) \
               or self._break_statement(in_loop) \
               \
               or self._function_declaration() \
               or self._return_statement(in_function) \
               or self._function_call()

    def _push_statement(self):
        literal = self._literal()
        identifier = self._identifier()
        if literal is None and identifier is None: # NOTE: position has not been incremented
            return 
        elif self.token().kind != TokenKind.PUSH:
            self.position -= 1 # undo the advance
            return

        self.position += 1
        return TreeNode(TreeNodeKind.PUSH_STATEMENT,
                        self.relative_token(-2).start,
                        self.relative_token(-1).end,
                        children=[literal or identifier])

    def _pop_statement(self):
        if self.token().kind == TokenKind.POP:
            self.position += 1
            identifier = self._identifier()
            return TreeNode(TreeNodeKind.POP_STATEMENT,
                            self.relative_token(-2).start,
                            self.relative_token(-1).end,
                            children=[identifier])

    def _add_operation(self):
        if self.token().kind == TokenKind.ADD:
            self.position += 1
            return TreeNode(TreeNodeKind.ADD_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _subtract_operation(self):
        if self.token().kind == TokenKind.SUBTRACT:
            self.position += 1
            return TreeNode(TreeNodeKind.SUBTRACT_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _multiply_operation(self):
        if self.token().kind == TokenKind.MULTIPLY:
            self.position += 1
            return TreeNode(TreeNodeKind.MULTIPLY_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _divide_operation(self):
        if self.token().kind == TokenKind.DIVIDE:
            self.position += 1
            return TreeNode(TreeNodeKind.DIVIDE_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _modulo_operation(self):
        if self.token().kind == TokenKind.MODULO:
            self.position += 1
            return TreeNode(TreeNodeKind.MODULO_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _equals_operation(self):
        if self.token().kind == TokenKind.EQUALS:
            self.position += 1
            return TreeNode(TreeNodeKind.EQUALS_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _not_equals_operation(self):
        if self.token().kind == TokenKind.NOT_EQUALS:
            self.position += 1
            return TreeNode(TreeNodeKind.NOT_EQUALS_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _greater_operation(self):
        if self.token().kind == TokenKind.GREATER:
            self.position += 1
            return TreeNode(TreeNodeKind.GREATER_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _less_operation(self):
        if self.token().kind == TokenKind.LESS:
            self.position += 1
            return TreeNode(TreeNodeKind.LESS_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _greater_equals_operation(self):
        if self.token().kind == TokenKind.GREATER_EQUALS:
            self.position += 1
            return TreeNode(TreeNodeKind.GREATER_EQUALS_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _less_equals_operation(self):
        if self.token().kind == TokenKind.LESS_EQUALS:
            self.position += 1
            return TreeNode(TreeNodeKind.LESS_EQUALS_OPERATION,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _if_statement(self, in_loop=False, in_function=False):
        # TODO: make the start and end positions useful for unmatched curly braces (for loops too)
        start_token = self.token() # save it to show errors
        if self.token().kind == TokenKind.IF \
           and self.relative_token(1).kind == TokenKind.LEFT_CURLY_BRACE:
            node = TreeNode(TreeNodeKind.IF_STATEMENT,
                            self.token().start,
                            None, # unknown end (will be updated later)
                            children=[])
            self.position += 2
            while self.token().kind != TokenKind.RIGHT_CURLY_BRACE:
                statement = self._statement(in_loop=in_loop, in_function=in_function)
                if statement is None: # position has not incremented if it is None
                    throw_error(self.filename, self.source, ErrorKind.INVALID_SYNTAX, self.token().start, self.token().end) # not a valid statement
                node.add_child(statement)

                if self.token().kind == TokenKind.END_OF_FILE:
                    throw_error(self.filename, self.source, ErrorKind.INVALID_SYNTAX, start_token, self.token().start) # unmatched curly braces

            self.position += 1 # skip the right curly brace
            node.end = self.relative_token(-1).end # position of the last curly brace
            return node

    def _else_statement(self, in_loop=False, in_function=False):
        start_token = self.token() # save it to show errors
        if self.token().kind == TokenKind.ELSE \
           and self.relative_token(1).kind == TokenKind.LEFT_CURLY_BRACE:
            node = TreeNode(TreeNodeKind.ELSE_STATEMENT,
                            self.token().start,
                            None, # unknown end (will be updated later)
                            children=[])
            self.position += 2
            while self.token().kind != TokenKind.RIGHT_CURLY_BRACE:
                statement = self._statement(in_loop=in_loop, in_function=in_function)
                if statement is None: # position has not incremented if it is None
                    throw_error(self.filename, self.source, ErrorKind.INVALID_SYNTAX, self.token().start, self.token().end) # not a valid statement
                node.add_child(statement)

                if self.token().kind == TokenKind.END_OF_FILE:
                    throw_error(self.filename, self.source, ErrorKind.INVALID_SYNTAX, start_token, self.token().start) # unmatched curly braces

            self.position += 1 # skip the right curly brace
            node.end = self.relative_token(-1).end # position of the last curly brace
            return node

    def _loop_statement(self, in_function=False):
        start_token = self.token() # save it to show errors
        if self.token().kind == TokenKind.LOOP \
           and self.relative_token(1).kind == TokenKind.LEFT_CURLY_BRACE:
            node = TreeNode(TreeNodeKind.LOOP_STATEMENT,
                            self.token().start,
                            None, # unknown end (will be updated later)
                            children=[])
            self.position += 2
            while self.token().kind != TokenKind.RIGHT_CURLY_BRACE:
                statement = self._statement(in_loop=True, in_function=in_function)
                if statement is None: # position has not incremented if it is None
                    throw_error(self.filename, self.source, ErrorKind.INVALID_SYNTAX, self.token().start, self.token().end) # not a valid statement
                node.add_child(statement)

                if self.token().kind == TokenKind.END_OF_FILE:
                    throw_error(self.filename, self.source, ErrorKind.INVALID_SYNTAX, start_token, self.token().start) # unmatched curly braces

            self.position += 1 # skip the right curly brace
            node.end = self.relative_token(-1).end # position of the last curly brace
            return node

    def _continue_statement(self, in_loop):
        is_continue = self.token().kind == TokenKind.CONTINUE
        if not in_loop:
            if is_continue:
                throw_error(self.filename, self.source, ErrorKind.CONTINUE_OUTSIDE_LOOP_ERROR, self.token().start, self.token().end)
            return
        if is_continue:
            self.position += 1
            return TreeNode(TreeNodeKind.CONTINUE_STATEMENT,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _break_statement(self, in_loop):
        is_break = self.token().kind == TokenKind.BREAK
        if not in_loop:
            if is_break:
                throw_error(self.filename, self.source, ErrorKind.BREAK_OUTSIDE_LOOP_ERROR, self.token().start, self.token().end)
            return
        if is_break:
            self.position += 1
            return TreeNode(TreeNodeKind.BREAK_STATEMENT,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _function_declaration(self):
        start_token = self.token() # save it to show errors
        if self.token().kind == TokenKind.IDENTIFIER \
           and self.relative_token(1).kind == TokenKind.LEFT_CURLY_BRACE:
            node = TreeNode(TreeNodeKind.FUNCTION_DECLARATION,
                            self.token().start,
                            None, # unknown end (will be updated later)
                            raw=self.token().literal,
                            value=self.token().literal, # store function name
                            children=[])
            self.position += 2
            while self.token().kind != TokenKind.RIGHT_CURLY_BRACE:
                statement = self._statement(in_loop=False, in_function=True)
                if statement is None: # position has not incremented if it is None
                    throw_error(self.filename, self.source, ErrorKind.INVALID_SYNTAX, self.token().start, self.token().end) # not a valid statement
                node.add_child(statement)

                if self.token().kind == TokenKind.END_OF_FILE:
                    throw_error(self.filename, self.source, ErrorKind.INVALID_SYNTAX, start_token, self.token().start) # unmatched curly braces

            self.position += 1 # skip the right curly brace
            node.end = self.relative_token(-1).end # position of the last curly brace
            return node

    def _return_statement(self, in_function):
        is_return = self.token().kind == TokenKind.RETURN
        if not in_function:
            if is_return:
                throw_error(self.filename, self.source, ErrorKind.RETURN_OUTSIDE_FUNCTION_ERROR, self.token().start, self.token().end)
            return
        if is_return:
            self.position += 1
            return TreeNode(TreeNodeKind.RETURN_STATEMENT,
                            self.relative_token(-1).start,
                            self.relative_token(-1).end)

    def _function_call(self):
        if self.token().kind == TokenKind.IDENTIFIER \
           and self.relative_token(1).kind == TokenKind.CALL:
            self.position += 2
            return TreeNode(TreeNodeKind.FUNCTION_CALL,
                            self.relative_token(-2).start,
                            self.relative_token(-1).end,
                            raw=self.relative_token(-2).literal,
                            value=self.relative_token(-2).literal)
