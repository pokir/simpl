from enum import Enum, auto


class SyntaxErrorKind(Enum):
    INVALID_SYNTAX = 'invalid syntax'
    UNTERMINATED_STRING_LITERAL = 'unterminated string literal'
    INVALID_NUMBER_LITERAL = 'invalid number literal'
    #= auto()
    #= auto()


class TokenKind(Enum):
    IDENTIFIER = auto()
    PUSH = auto()
    POP = auto()

    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()

    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()

    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_OR_EQUALS = auto()
    LESS_OR_EQUALS = auto()

    IF = auto()
    ELSE = auto()

    LOOP = auto()
    BREAK = auto()

    LEFT_CURLY_BRACE = auto()
    RIGHT_CURLY_BRACE = auto()

    CALL = auto()
    RETURN = auto()


class TreeNodeKind(Enum):
    ROOT = auto()

    IDENTIFIER = auto()
    
    PUSH_STATEMENT = auto()
    POP_STATEMENT = auto()

    FUNCTION_DECLARATION = auto()
    FUNCTION_CALL = auto()
    RETURN_STATEMENT = auto()

    IF_STATEMENT = auto()
    ELSE_STATEMENT = auto()

    LOOP_STATEMENT = auto()
    BREAK_STATEMENT = auto()

    BLOCK = auto() # {curly braces}

    NUMERIC_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOLEAN_LITERAL = auto()

    ADD_OPERATION = auto()
    SUBTRACT_OPERATION = auto()
    MULTIPLY_OPERATION = auto()
    DIVIDE_OPERATION = auto()
    MODULO_OPERATION = auto()

    EQUALS_OPERATION = auto()
    NOT_EQUALS_OPERATION = auto()
    GREATER_OPERATION = auto()
    LESS_OPERATION = auto()
    GREATER_OR_EQUALS_OPERATION = auto()
    LESS_OR_EQUALS_OPERATION = auto()
