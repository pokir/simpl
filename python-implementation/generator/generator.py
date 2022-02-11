from parser import tree_node_kinds_
from parser import tree_node_


TreeNode = tree_node_.TreeNode
TreeNodeKind = tree_node_kinds_.TreeNodeKind


class Generator:
    def __init__(self, tree):
        self.tree = tree
        self.generated_code = ''

    def generate(self):
        self.generated_code += '#include <iostream>\n'
        self.generated_code += '#include <functional>\n'
        self.generated_code += '#include <map>\n'
        self.generated_code += '#include <string>\n'
        self.generated_code += '#include <vector>\n'

        self.generated_code += 'struct Data{'
        self.generated_code += 'short type;' # 0: string, 1: number, 2: boolean
        self.generated_code += 'std::string string;'
        self.generated_code += 'double number;'
        self.generated_code += 'bool boolean;'
        self.generated_code += '};'

        self.generated_code += 'struct Variable{'
        self.generated_code += 'std::string name;'
        self.generated_code += 'Data data;'
        self.generated_code += '};'

        self.generated_code += 'int main(){'
        self.generated_code += 'std::vector<Data>stack;'
        self.generated_code += 'std::map<std::string,Data>variables;'
        self.generated_code += 'std::map<std::string,std::function<void()> >functions;'

        self.generated_code += 'Data temp1;'
        self.generated_code += 'Data temp2;'

        # load std functions written in c++

        # print
        self.generated_code += 'functions.insert_or_assign('
        self.generated_code += '"print",'
        self.generated_code += '[&stack,&variables,&functions](){'

        self.generated_code += 'if(stack.back().type==0)'
        self.generated_code += 'std::cout<<stack.back().string;'
        self.generated_code += 'else if(stack.back().type==1)'
        self.generated_code += 'std::cout<<stack.back().number;'
        self.generated_code += 'else if(stack.back().type==2)'
        self.generated_code += 'std::cout<<stack.back().boolean;'
        #self.generated_code += '/*stack.pop_back();*/'

        self.generated_code += '});'
        # end print

        # input
        self.generated_code += 'functions.insert_or_assign('
        self.generated_code += '"input",'
        self.generated_code += '[&stack,&variables,&functions](){'

        self.generated_code += 'stack.push_back(Data());'
        self.generated_code += 'stack.back().type=0;'
        self.generated_code += 'std::cin >> stack.back().string;'

        self.generated_code += '});'
        # end input

        # system
        self.generated_code += 'functions.insert_or_assign('
        self.generated_code += '"system",'
        self.generated_code += '[&stack,&variables,&functions](){'

        self.generated_code += 'stack.push_back((Data){1,"",(double) std::system(stack.back().string.c_str()),false});'

        self.generated_code += '});'
        # end system

        self._visit(self.tree)

        self.generated_code += 'return 0;'
        self.generated_code += '}'

    def _visit(self, node):
        self._visit_root(node)

        self._visit_push_statement(node)
        self._visit_pop_statement(node)

        self._visit_function_declaration(node)
        self._visit_function_call(node)
        self._visit_return_statement(node)

        self._visit_if_statement(node)
        self._visit_else_statement(node)

        self._visit_loop_statement(node)
        self._visit_continue_statement(node)
        self._visit_break_statement(node)

        self._visit_add_operation(node)
        self._visit_subtract_operation(node)
        self._visit_multiply_operation(node)
        self._visit_divide_operation(node)
        self._visit_modulo_operation(node)

        self._visit_equals_operation(node)
        self._visit_not_equals_operation(node)
        self._visit_greater_operation(node)
        self._visit_greater_equals_operation(node)
        self._visit_less_operation(node)
        self._visit_less_equals_operation(node)

    def _visit_root(self, node):
        if node.kind == TreeNodeKind.ROOT:
            for child in node.children:
                self._visit(child)

    #def _visit_identifier(self, node):
    #    if node.kind == TreeNodeKind.IDENTIFIER:
            
    
    def _visit_push_statement(self, node):
        if node.kind == TreeNodeKind.PUSH_STATEMENT:
            if node.children[0].kind == TreeNodeKind.IDENTIFIER:
                self.generated_code += f'stack.push_back(variables.at("{node.children[0].value}"));'
            else:
                self.generated_code += 'stack.push_back(Data());'
                if node.children[0].kind == TreeNodeKind.STRING_LITERAL:
                    self.generated_code += 'stack.back().type=0;'
                    self.generated_code += f'stack.back().string="{repr(node.children[0].value)[1:-1]}";'
                elif node.children[0].kind == TreeNodeKind.NUMERIC_LITERAL:
                    self.generated_code += 'stack.back().type=1;'
                    self.generated_code += f'stack.back().number={node.children[0].value};'
                elif node.children[0].kind == TreeNodeKind.BOOLEAN_LITERAL:
                    self.generated_code += 'stack.back().type=2;'
                    self.generated_code += f'stack.back().boolean={"true" if node.children[0].value else "false"};'

    def _visit_pop_statement(self, node):
        if node.kind == TreeNodeKind.POP_STATEMENT:
            self.generated_code += f'variables.insert_or_assign("{node.children[0].value}",stack.back());'
            self.generated_code += 'stack.pop_back();'

    def _visit_function_declaration(self, node):
        if node.kind == TreeNodeKind.FUNCTION_DECLARATION:
            self.generated_code += 'functions.insert_or_assign('
            #self.generated_code += 'std::pair<std::string,std::function<void()> >'
            self.generated_code += f'"{node.value}",'
            self.generated_code += '[&stack,&variables,&functions](){'
            
            for child in node.children:
                self._visit(child);

            self.generated_code += '});'


    def _visit_function_call(self, node):
        if node.kind == TreeNodeKind.FUNCTION_CALL:
            self.generated_code += f'functions.at("{node.value}")();'

    def _visit_return_statement(self, node):
        if node.kind == TreeNodeKind.RETURN_STATEMENT:
            self.generated_code += 'return;'

    def _visit_if_statement(self, node):
        if node.kind == TreeNodeKind.IF_STATEMENT:
            self.generated_code += 'if(stack.back().type==2&&stack.back().boolean){'
        
            for child in node.children:
                self._visit(child)

            self.generated_code += '}'

    def _visit_else_statement(self, node):
        if node.kind == TreeNodeKind.ELSE_STATEMENT:
            self.generated_code += 'if(stack.back().type!=2||!stack.back().boolean)){'
        
            for child in node.children:
                self._visit(child)

            self.generated_code += '}'

    def _visit_loop_statement(self, node):
        if node.kind == TreeNodeKind.LOOP_STATEMENT:
            self.generated_code += 'while(true){'
        
            for child in node.children:
                self._visit(child)

            self.generated_code += '}'

    def _visit_continue_statement(self, node):
        if node.kind == TreeNodeKind.CONTINUE_STATEMENT:
            self.generated_code += 'continue;'

    def _visit_break_statement(self, node):
        if node.kind == TreeNodeKind.BREAK_STATEMENT:
            self.generated_code += 'break;'

    '''def _visit_numeric_literal(self, node):
        if node.kind == TreeNodeKind.NUMERIC_LITERAL:
            pass

    def _visit_string_literal(self, node):
        if node.kind == TreeNodeKind.STRING_LITERAL:
            pass

    def _visit_boolean_literal(self, node):
        if node.kind == TreeNodeKind.BOOLEAN_LITERAL:
            pass'''

    def _visit_add_operation(self, node):
        if node.kind == TreeNodeKind.ADD_OPERATION:
            # add and pop the two
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.back()=(Data){temp1.type,temp2.string+temp1.string,temp2.number+temp1.number,false};'

    def _visit_subtract_operation(self, node):
        if node.kind == TreeNodeKind.SUBTRACT_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.back()=(Data){temp1.type,"",temp2.number-temp1.number,false};'

    def _visit_multiply_operation(self, node):
        if node.kind == TreeNodeKind.MULTIPLY_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.back()=(Data){temp1.type,"",temp2.number*temp1.number,false};'

    def _visit_divide_operation(self, node):
        if node.kind == TreeNodeKind.DIVIDE_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.back()=(Data){temp1.type,"",temp2.number/temp1.number,false};'

    def _visit_modulo_operation(self, node):
        if node.kind == TreeNodeKind.MODULO_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.back()=(Data){temp1.type,"",temp2.number%temp1.number,false};'

    def _visit_equals_operation(self, node):
        if node.kind == TreeNodeKind.EQUALS_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.pop_back();'

            # if the types are different, false
            self.generated_code += 'if(temp1.type!=temp2.type)'
            self.generated_code += 'stack.push_back((Data){2,"",0,false});'

            # if the types are the same and the values are the same, true
            self.generated_code += 'else if('
            self.generated_code += '(temp1.type==0&&temp1.string==temp2.string)'
            self.generated_code += '||(temp1.type==1&&temp1.number==temp2.number)'
            self.generated_code += '||(temp1.type==2&&temp1.boolean==temp2.boolean)'
            self.generated_code += ')stack.push_back((Data){2,"",0,true});'

            # if the types are the same and the values are different, false
            self.generated_code += 'else stack.push_back((Data){2,"",0,false});'

    def _visit_not_equals_operation(self, node):
        if node.kind == TreeNodeKind.NOT_EQUALS_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.pop_back();'

            # if the types are different, true
            self.generated_code += 'if(temp1.type!=temp2.type)'
            self.generated_code += 'stack.push_back((Data){2,"",0,true});'

            # if the types are the same and the values are the same, false
            self.generated_code += 'else if('
            self.generated_code += '(temp1.type==0&&temp1.string==temp2.string)'
            self.generated_code += '||(temp1.type==1&&temp1.number==temp2.number)'
            self.generated_code += '||(temp1.type==2&&temp1.boolean==temp2.boolean)'
            self.generated_code += ')stack.push_back((Data){2,"",0,false});'
            
            # if the types are the same and the values are different, true
            self.generated_code += 'else stack.push_back((Data){2,"",0,true});'

    def _visit_greater_operation(self, node):
        if node.kind == TreeNodeKind.GREATER_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.pop_back();'

            # if the types are different or the type is not a number, false
            self.generated_code += 'if(temp1.type!=temp2.type||temp1.type!=1)'
            self.generated_code += 'stack.push_back((Data){2,"",0,false});'

            # if the types are the same and the type is a number and the first number is greater than the second one, true
            self.generated_code += 'else if(temp2.number>temp1.number)stack.push_back((Data){2,"",0,true});'

    def _visit_less_operation(self, node):
        if node.kind == TreeNodeKind.LESS_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.pop_back();'

            # if the types are different or the type is not a number, false
            self.generated_code += 'if(temp1.type!=temp2.type||temp1.type!=1)'
            self.generated_code += 'stack.push_back((Data){2,"",0,false});'

            # if the types are the same and the type is a number and the first number is less than the second one, true
            self.generated_code += 'else if(temp2.number<temp1.number)stack.push_back((Data){2,"",0,true});'

    def _visit_greater_equals_operation(self, node):
        if node.kind == TreeNodeKind.GREATER_EQUALS_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.pop_back();'

            # if the types are different or the type is not a number, false
            self.generated_code += 'if(temp1.type!=temp2.type||temp1.type!=1)'
            self.generated_code += 'stack.push_back((Data){2,"",0,false});'

            # if the types are the same and the type is a number and the first number is greater than or equal to the second one, true
            self.generated_code += 'else if(temp2.number>=temp1.number)stack.push_back((Data){2,"",0,true});'

    def _visit_less_equals_operation(self, node):
        if node.kind == TreeNodeKind.LESS_EQUALS_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.pop_back();'

            # if the types are different or the type is not a number, false
            self.generated_code += 'if(temp1.type!=temp2.type||temp1.type!=1)'
            self.generated_code += 'stack.push_back((Data){2,"",0,false});'

            # if the types are the same and the type is a number and the first number is less than or equal to the second one, true
            self.generated_code += 'else if(temp2.number<=temp1.number)stack.push_back((Data){2,"",0,true});'
