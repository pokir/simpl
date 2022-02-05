from enum import Enum, auto


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
    GREATER_EQUALS = auto()
    LESS_EQUALS = auto()

    IF = auto()
    ELSE = auto()

    LOOP = auto()
    BREAK = auto()

    LEFT_CURLY_BRACE = auto()
    RIGHT_CURLY_BRACE = auto()

    CALL = auto()
    RETURN = auto()

    END_OF_FILE = auto()
