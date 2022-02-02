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
    PROGRAM = auto()
    
    POP = auto()
    PUSH = auto()

    FUNCTION_DECLARATION = auto()
    CALL_EXPRESSION = auto()

    IF = auto()

    BLOCK_STATEMENT = auto()
