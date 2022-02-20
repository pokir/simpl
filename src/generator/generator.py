from parser import tree_node_kinds_
from parser import tree_node_


TreeNode = tree_node_.TreeNode
TreeNodeKind = tree_node_kinds_.TreeNodeKind


class Generator:
    def __init__(self, tree):
        self.tree = tree
        self.generated_code = ''

    def generate(self):

        '''
        If a variable exist in a previous scope, edit that one
        Otherwise, add it to the current scope

        When it enters a new block, scope += 1
        When it leaves a block, scope -= 1
        Global scope = 0
        '''

        self.generated_code += '#include <cmath>\n'
        self.generated_code += '#include <iostream>\n'
        self.generated_code += '#include <functional>\n'
        self.generated_code += '#include <map>\n'
        self.generated_code += '#include <string>\n'
        self.generated_code += '#include <vector>\n'

        self.generated_code += 'struct Data{'
        self.generated_code += 'short type;' # 0: string, 1: number, 2: boolean, 3: function
        self.generated_code += 'std::string string;'
        self.generated_code += 'double number;'
        self.generated_code += 'bool boolean;'
        self.generated_code += 'std::function<void()> function;'
        self.generated_code += '};'

        self.generated_code += 'struct Variable{'
        self.generated_code += 'std::string name;'
        self.generated_code += 'Data data;'
        self.generated_code += '};'

        self.generated_code += 'int scope=0;'
        self.generated_code += 'std::vector<Data>stack;'
        self.generated_code += 'std::vector<std::map<std::string,Variable> >variables;'
        self.generated_code += 'Data temp1;'
        self.generated_code += 'Data temp2;'

        self.generated_code += 'bool varExists(int scope,std::string name){'
        self.generated_code += 'for(int i=0;i<=scope;++i){'
        self.generated_code += 'if(variables.size()<=i)return false;'
        self.generated_code += 'if(variables.at(i).count(name))return true;'
        self.generated_code += '}'
        self.generated_code += 'return false;'
        self.generated_code += '}'

        # TODO: make it so it returns something when there is no variable
        self.generated_code += 'Variable& getVar(int scope,std::string name){'
        self.generated_code += 'for(int i=0;i<=scope;++i){'
        self.generated_code += 'auto found=variables.at(i).find(name);'
        self.generated_code += 'if(found!=variables.at(i).end())'
        self.generated_code += 'return found->second;'
        self.generated_code += '}'
        self.generated_code += '}'

        self.generated_code += 'void setVar(int scope,std::string name,Data data){'
        self.generated_code += 'if(varExists(scope,name))'
        self.generated_code += 'getVar(scope,name).data=data;'
        self.generated_code += 'else{'
        self.generated_code += 'while(variables.size()<=scope)'
        self.generated_code += 'variables.push_back(std::map<std::string,Variable>());'
        self.generated_code += 'variables.at(scope).insert_or_assign(name,(Variable){name,data});'
        self.generated_code += '}'
        self.generated_code += '}'

        self.generated_code += 'void setFunctionVar(int scope,std::string name,std::function<void()>func){'
        self.generated_code += 'setVar(scope,name,(Data){3,"",0,false,func});'
        self.generated_code += '}'

        # cleans all scopes until there are only targetScope scopes
        self.generated_code += 'void cleanScopes(int targetScope){'
        self.generated_code += 'while(variables.size()>targetScope+1)'
        self.generated_code += 'variables.pop_back();'
        self.generated_code += '}'

        self.generated_code += 'int main(int argc, char **argv){'

        # ADD COMMAND LINE ARGUMENTS TO THE STACK
        self.generated_code += 'for(int i=0;i<argc;++i){'
        self.generated_code += 'stack.push_back(Data());'
        self.generated_code += 'stack.back().type=0;'
        self.generated_code += 'stack.back().string=argv[argc-i-1];'
        self.generated_code += '}'
        # add the argument count
        self.generated_code += 'stack.push_back(Data());'
        self.generated_code += 'stack.back().type=1;'
        self.generated_code += 'stack.back().number=argc;'
        # END COMMAND LINE ARGUMENTS

        # STD FUNCTIONS WRITTEN IN C++
        self.generated_code += '\n#include "src/std/cpp/std.cpp"\n'

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
                self.generated_code += f'stack.push_back(getVar(scope,"{node.children[0].value}").data);'
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
            self.generated_code += f'setVar(scope,"{node.children[0].value}",stack.back());'
            self.generated_code += 'stack.pop_back();'

    def _visit_function_declaration(self, node):
        if node.kind == TreeNodeKind.FUNCTION_DECLARATION:
            self.generated_code += f'setFunctionVar(scope,"{node.value}",'
            self.generated_code += '[&](){' # TODO: make sure scope is captured correctly
            self.generated_code += 'int _scope=scope;'
            self.generated_code += 'int scope=_scope+1;'
            
            for child in node.children:
                self._visit(child);

            self.generated_code += '});'


    def _visit_function_call(self, node):
        if node.kind == TreeNodeKind.FUNCTION_CALL:
            self.generated_code += f'getVar(scope, "{node.value}").data.function();'
            self.generated_code += 'cleanScopes(scope);'

    def _visit_return_statement(self, node):
        if node.kind == TreeNodeKind.RETURN_STATEMENT:
            self.generated_code += 'return;'

    def _visit_if_statement(self, node):
        if node.kind == TreeNodeKind.IF_STATEMENT:
            self.generated_code += 'if(stack.back().type==2&&stack.back().boolean){'
            self.generated_code += 'int _scope=scope;'
            self.generated_code += 'int scope=_scope+1;'
        
            for child in node.children:
                self._visit(child)

            self.generated_code += '}'
            self.generated_code += 'cleanScopes(scope);'

    def _visit_else_statement(self, node):
        if node.kind == TreeNodeKind.ELSE_STATEMENT:
            self.generated_code += 'if(stack.back().type!=2||!stack.back().boolean){'
            self.generated_code += 'int _scope=scope;'
            self.generated_code += 'int scope=_scope+1;'
        
            for child in node.children:
                self._visit(child)

            self.generated_code += '}'
            self.generated_code += 'cleanScopes(scope);'

    def _visit_loop_statement(self, node):
        if node.kind == TreeNodeKind.LOOP_STATEMENT:
            self.generated_code += 'while(true){'
            self.generated_code += 'int _scope=scope;'
            self.generated_code += 'int scope=_scope+1;'
        
            for child in node.children:
                self._visit(child)

            self.generated_code += '}'
            self.generated_code += 'cleanScopes(scope);'

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
            self.generated_code += 'stack.back()=(Data){temp1.type,"",std::fmod(temp2.number,temp1.number),false};'

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

            # else false
            self.generated_code += 'else stack.push_back((Data){2,"",0,false});'

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
            self.generated_code += 'else if(temp2.number<temp1.number)'
            self.generated_code += 'stack.push_back((Data){2,"",0,true});'

            # else false
            self.generated_code += 'else stack.push_back((Data){2,"",0,false});'

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
            self.generated_code += 'else if(temp2.number>=temp1.number)'
            self.generated_code += 'stack.push_back((Data){2,"",0,true});'

            # else false
            self.generated_code += 'else stack.push_back((Data){2,"",0,false});'

    def _visit_less_equals_operation(self, node):
        if node.kind == TreeNodeKind.LESS_EQUALS_OPERATION:
            self.generated_code += 'temp1=stack.back();'
            self.generated_code += 'stack.pop_back();'
            self.generated_code += 'temp2=stack.back();'
            self.generated_code += 'stack.pop_back();'

            # if the types are different or the type is not a number, false
            self.generated_code += 'if(temp1.type!=temp2.type||temp1.type!=1)'
            self.generated_code += 'stack.push_back((Data){2,"",0,false});'

            # if the types are the same type and the type is a number and the first number is less than or equal to the second one, true
            self.generated_code += 'else if(temp2.number<=temp1.number)'
            self.generated_code += 'stack.push_back((Data){2,"",0,true});'

            # else false
            self.generated_code += 'else stack.push_back((Data){2,"",0,false});'
