import colorama # for printing errors in colors
from enum import Enum, auto
from os import get_terminal_size
import sys


all_errors = [] # for the future when it will show all errors


def display_error_in_code(source, start, end):
    # Show where the error is in the code, showing 5 lines of code
    # start and end are both (line, column), starting at 1 for both
    # line and column
    first_line = max(start[0] - 5, 0)
    last_line = start[0] - 1     # the line where the error happened
    
    raw_lines = source.split('\n')[first_line:last_line + 1]
    lines = raw_lines.copy()

    # the length of the snip replacement
    left_snip_symbol = '... '
    right_snip_symbol = ' ...'

    # make it so all the lines fit on the terminal (by removing some parts)
    left_offset = len(str(start[0])) + 2
    width = get_terminal_size().columns - left_offset

    for i in range(len(lines)):
        # show the error in the center
        left_slice = max(start[1] - int(width * 0.5), 0)
        #right_slice = min(start[1] + int(width * 0.5), len(lines[i]))
        right_slice = min(left_slice + width, len(lines[i]))

        # wheter to show "..."
        snip_left = False
        snip_right = False

        if left_slice > 0:
            left_slice += len(left_snip_symbol)
            snip_left = True

        if right_slice < len(lines[i])- 1:
            right_slice -= len(right_snip_symbol)
            snip_right = True

        # snip the line
        lines[i] = lines[i][left_slice:right_slice]
        if snip_left:
            lines[i] = colorama.Fore.YELLOW + left_snip_symbol + colorama.Style.RESET_ALL + lines[i]
        if snip_right:
            lines[i] += colorama.Fore.YELLOW + right_snip_symbol + colorama.Style.RESET_ALL

        # add line numbers
        lines[i] = colorama.Fore.CYAN + str(first_line + i + 1).ljust(left_offset - 1) + '|' + colorama.Style.RESET_ALL + lines[i] # add line numbers

    string = '\n'.join(lines)
    string += '\n'
    string += colorama.Fore.RED + '^'.rjust(start[1] + left_offset - left_slice + (len(left_snip_symbol) if snip_left else 0)) + colorama.Style.RESET_ALL
    return string


def throw_error(filename, source, error_kind, start, end):
    error = error_kind.value(filename, source, start, end)
    all_errors.append(error) # for the future when it will show all errors
    print(error.show())
    print()
    sys.exit(1)


# For the future when it will show all errors:
#def show_errors():
#    if len(all_errors) > 0:
#        for error in all_errors:
#            print(error.show())
#            print()
#        sys.exit(1)


class Error:
    def __init__(self, filename, source, start, end, details):
        self.filename = filename
        self.source = source # the entire code in the file, so that it can be displayed
        self.start = start
        self.end = end
        self.details = details

    def show(self):
        result = f'{colorama.Style.BRIGHT}{self.filename}:{self.start[0]}:{self.start[1]}: '
        result += f'{colorama.Fore.RED}{self.__class__.__name__}{colorama.Style.RESET_ALL}{colorama.Style.BRIGHT}: {self.details}{colorama.Style.RESET_ALL}\n'
        #result += f'Line {self.start[0]}, column {self.start[1]}'

        result += f'\n\n{display_error_in_code(self.source, self.start, self.end)}'
        return result


class InvalidSyntaxError(Error):
    def __init__(self, filename, source, start, end):
        super().__init__(filename, source, start, end, 'invalid syntax')


class IllegalCharacterError(Error):
    def __init__(self, filename, source, start, end):
        super().__init__(filename, source, start, end, 'illegal character')


class UnterminatedStringLiteralError(Error):
    def __init__(self, filename, source, start, end):
        super().__init__(filename, source, start, end, 'unterminated string literal')


class InvalidNumberLiteralError(Error):
    def __init__(self, filename, source, start, end):
        # TODO: make it show where the end is
        super().__init__(filename, source, start, end, 'invalid number literal')


class ReturnOutsideFunctionError(Error):
    def __init__(self, filename, source, start, end):
        super().__init__(filename, source, start, end, 'return outside function')


class ContinueOutsideLoopError(Error):
    def __init__(self, filename, source, start, end):
        super().__init__(filename, source, start, end, 'continue outside loop')


class BreakOutsideLoopError(Error):
    def __init__(self, filename, source, start, end):
        super().__init__(filename, source, start, end, 'break outside loop')


# TODO: put the enums in a different file
class ErrorKind(Enum):
    INVALID_SYNTAX = InvalidSyntaxError
    UNTERMINATED_STRING_LITERAL = UnterminatedStringLiteralError
    INVALID_NUMBER_LITERAL = InvalidNumberLiteralError
    ILLEGAL_CHARACTER = IllegalCharacterError

    RETURN_OUTSIDE_FUNCTION_ERROR = ReturnOutsideFunctionError
    CONTINUE_OUTSIDE_LOOP_ERROR = ContinueOutsideLoopError
    BREAK_OUTSIDE_LOOP_ERROR = BreakOutsideLoopError
