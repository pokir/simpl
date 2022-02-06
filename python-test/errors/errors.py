import colorama # for printing errors in colors
from enum import Enum, auto
from os import get_terminal_size
import sys



"""
def show_error_in_code(source, start, end):
    # Show where the error is in the code, showing 5 lines of code
    # start and end are both (line, column), starting at 1 for both
    # line and column
    first_line = max(start[0] - 5, 0)
    last_line = start[0] - 1     # the line where the error happened
    
    raw_lines = source.split('\n')[first_line:last_line + 1]
    lines = raw_lines.copy()
    
    # make it so all the lines fit on the terminal (by removing some parts)

    left_offset = len(str(start[0])) + 2
    width = get_terminal_size().columns - left_offset

    left_slice = 0

    # show the error in the center
    left_slice = max(start[1] - int(width / 2), 0)
    right_slice = min(start[1] + int(width / 2), len(lines[-1]))

    # wheter to show "..."
    snip_left = False
    snip_right = False
    
    # the length of the snip replacement
    snip_length = 4

    if left_slice > 0:
        left_slice += snip_length
        snip_left = True

    if right_slice < len(lines[-1]) - 1:
        right_slice -= snip_length
        snip_right = True

    for i in range(len(lines)):
        lines[i] = lines[i][left_slice:right_slice]
        if snip_left:
            lines[i] = colorama.Fore.YELLOW + '... ' + colorama.Style.RESET_ALL + lines[i]
        if snip_right and len(raw_lines[i]) > right_slice: # the extra check removes useless snips if the previous lines don't go over the slice
            lines[i] += colorama.Fore.YELLOW + ' ...' + colorama.Style.RESET_ALL

        lines[i] = colorama.Fore.CYAN + str(first_line + i + 1).ljust(left_offset) + colorama.Style.RESET_ALL + lines[i] # add line numbers

        #map(lambda line: line[left_slice:right_slice], lines)
    
    string = '\n'.join(lines)
    string += '\n'
    string += colorama.Fore.RED + '^'.rjust(start[1] + left_offset - left_slice + (snip_length if snip_left else 0)) + colorama.Style.RESET_ALL
    return string
"""


def show_error_in_code(source, start, end):
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

    for i in range(len(lines)):
        # make it so all the lines fit on the terminal (by removing some parts)

        left_offset = len(str(start[0])) + 2
        width = get_terminal_size().columns - left_offset

        left_slice = 0

        # show the error in the center
        left_slice = max(start[1] - int(width * 0.2), 0)
        right_slice = min(start[1] + int(width * 0.8), len(lines[i]))

        # wheter to show "..."
        snip_left = False
        snip_right = False
        

        if left_slice > 0:
            left_slice += len(left_snip_symbol)
            snip_left = True

        if right_slice < len(lines[i]) - 1:
            right_slice -= len(right_snip_symbol)
            snip_right = True

        lines[i] = lines[i][left_slice:right_slice]
        if snip_left:
            lines[i] = colorama.Fore.YELLOW + left_snip_symbol + colorama.Style.RESET_ALL + lines[i]
        if snip_right:# and len(raw_lines[i]) > right_slice: # the extra check removes useless snips if the previous lines don't go over the slice
            lines[i] += colorama.Fore.YELLOW + right_snip_symbol + colorama.Style.RESET_ALL

        lines[i] = colorama.Fore.CYAN + str(first_line + i + 1).ljust(left_offset) + colorama.Style.RESET_ALL + lines[i] # add line numbers

        #map(lambda line: line[left_slice:right_slice], lines)
    
    string = '\n'.join(lines)
    string += '\n'
    string += colorama.Fore.RED + '^'.rjust(start[1] + left_offset - left_slice + (len(left_snip_symbol) if snip_left else 0)) + colorama.Style.RESET_ALL
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

        result += f'\n\n{show_error_in_code(self.source, self.start, self.end)}'
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
