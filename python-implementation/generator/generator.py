from parser import tree_node_kinds_
from parser import tree_node_


TreeNode = tree_node_.TreeNode
TreeNodeKind = tree_node_kinds_.TreeNodeKind


class Generator:
    def __init__(self, tree):
        self.tree = tree
        self.generated_code = ''

    def generate(self):
        self._visit(self.tree)

    def _visit(self, node):
        

    def _visit_root(self, node):
        if node.kind == TreeNodeKind.ROOT:
            for child in node.children:
                self._visit(child)

    #def _visit_identifier(self, node):
    #    if node.kind == TreeNodeKind.IDENTIFIER:
            
    
    def _visit_push_statement(self, node):
        if node.kind == TreeNodeKind.PUSH_STATEMENT:
            self.generated_code += ''

    def _visit_pop_statement(self, node):
        pass

    def _visit_function_declaration(self, node):
        pass

    def _visit_function_call(self, node):
        pass

    def _visit_return_statement(self, node):
        pass

    def _visit_if_statement(self, node):
        pass

    def _visit_else_statement(self, node):
        pass

    def _visit_loop_statement(self, node):
        pass

    def _visit_continue_statement(self, node):
        pass

    def _visit_break_statement(self, node):
        pass

    def _visit_numeric_literal(self, node):
        pass

    def _visit_string_literal(self, node):
        pass

    def _visit_boolean_literal(self, node):
        pass

    def _visit_add_operation(self, node):
        pass

    def _visit_subtract_operation(self, node):
        pass

    def _visit_multiply_operation(self, node):
        pass

    def _visit_divide_operation(self, node):
        pass

    def _visit_modulo_operation(self, node):
        pass

    def _visit_equals_operation(self, node):
        pass

    def _visit_not_equals_operation(self, node):
        pass

    def _visit_greater_operation(self, node):
        pass

    def _visit_less_operation(self):
        pass

    def _visit_greater_equals_operation(self):
        pass

    def _visit_less_equals_operation(self):
        pass
