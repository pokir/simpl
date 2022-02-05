from enum import Enum, auto
from os import get_terminal_size
import sys




def show_error_in_code(source, start, end):
    # Show where the error is in the code, showing 5 lines of code
    # start and end are both (line, column), starting at 1 for both line and column
    first_line = max(start[0] - 5, 0)
    last_line = start[0] - 1     # the line where the error happened
    
    lines = source.split('\n')[first_line:last_line + 1]
    
    # make it so all the lines fit on the terminal (by removing some parts)

    terminal_width = get_terminal_size().columns

    if len(lines[-1]) > terminal_width:
        # show the error in the center
        map(lambda line: line[start[1] - int(terminal_width / 2):start[1] + int(terminal_width / 2)], lines)
    
    string = '\n'.join(lines)
    string += '\n'
    string += ' ' * (start[1] - 1)
    string += '^'
    return string


def throw_error(source, error_kind, start, end):
    error = error_kind.value(source, start, end)
    print(error.show())
    sys.exit(1)


class Error:
    def __init__(self, source, start, end, details):
        self.source = source # the entire code in the file, so that it can be displayed
        self.start = start
        self.end = end
        self.details = details

    def show(self):
        result = f'{self.__class__.__name__}: {self.details}\n'
        result += f'Line {self.start[0]}, column {self.start[1]}'

        result += f'\n\n {show_error_in_code(self.source, self.start, self.end)}'
        return result


class InvalidSyntaxError(Error):
    def __init__(self, source, start, end):
        super().__init__(source, start, end, 'invalid syntax')


class IllegalCharacterError(Error):
    def __init__(self, source, start, end):
        super().__init__(source, start, end, 'illegal character')


class UnterminatedStringLiteralError(Error):
    def __init__(self, source, start, end):
        super().__init__(source, start, end, 'unterminated string literal')


class InvalidNumberLiteralError(Error):
    def __init__(self, source, start, end, error_kind, details):
        # TODO: make it show where the end is
        super().__init__(source, start, end, 'invalid number literal')


# TODO: put the enums in a different file
class ErrorKind(Enum):
    INVALID_SYNTAX = InvalidSyntaxError
    UNTERMINATED_STRING_LITERAL = UnterminatedStringLiteralError
    INVALID_NUMBER_LITERAL = InvalidNumberLiteralError
    ILLEGAL_CHARACTER = IllegalCharacterError
    #= auto()
    #= auto()
