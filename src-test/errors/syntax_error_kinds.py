from enum import Enum, auto


class SyntaxErrorKind(Enum):
    INVALID_SYNTAX = 'invalid syntax'
    UNTERMINATED_STRING_LITERAL = 'unterminated string literal'
    INVALID_NUMBER_LITERAL = 'invalid number literal'
    #= auto()
    #= auto()
