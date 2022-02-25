#from token_ import Token
#from token_kinds import TokenKind
from lexer import token_
from lexer import token_kinds_
from errors import errors


Token = token_.Token
TokenKind = token_kinds_.TokenKind
throw_error = errors.throw_error
ErrorKind = errors.ErrorKind


class Lexer:
    def __init__(self, filename, source):
        self.source = source
        self.filename = filename
        self.position = 0
        self.tokens = []
    
    def char(self):
        try:
            return self.source[self.position]
        except IndexError:
            return None
    
    def next_char(self):
        try:
            return self.source[self.position + 1]
        except IndexError:
            return None

    def get_line_column(self, offset=0):
        line = self.source[:self.position + offset].count('\n') + 1
        column = len(self.source[:self.position + offset].split('\n')[-1]) + 1
        return (line, column)
    
    def lex(self):
        #while self.position < len(self.source):
        while self.char() is not None:

            if self.char() in [' ', '\n', '\t']:
                self.position += 1

            elif self.char() == '#':
                while self.char() != '\n':
                    self.position += 1

            # TODO: remove the literal value from tokens that don't need it
            # (like ==, ., @) since it will always be the same
            elif self.char() == '.':
                self.tokens.append(Token(TokenKind.PUSH, '.', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '@':
                self.tokens.append(Token(TokenKind.POP, '@', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '+':
                self.tokens.append(Token(TokenKind.ADD, '+', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '-':
                if self.next_char() == '>':
                    self.tokens.append(Token(TokenKind.RETURN, '->', self.get_line_column(), self.get_line_column(2)))
                    self.position += 2
                elif self.next_char().isnumeric():
                    start = self.get_line_column()
                    buffer = self.char() + self.next_char()
                    self.position += 2  # skip both the negative number and the first digit

                    while self.char().isnumeric() \
                          or (self.char() == '.' and '.' not in buffer) \
                          or self.char() == '_':

                        # TODO: make it so ending _ is ignored (not errored)
                        # so that it can be scanned again
                        if self.char() == '_':
                            if self.next_char().isnumeric():
                                self.position += 1
                                continue
                            else:
                                throw_error(self.filename, self.source, ErrorKind.INVALID_NUMBER_LITERAL, start, self.get_line_column())

                        buffer += self.char()
                        self.position += 1

                    self.tokens.append(Token(TokenKind.NUMBER, buffer, start, self.get_line_column()))
                else:
                    self.tokens.append(Token(TokenKind.SUBTRACT, '-', self.get_line_column(), self.get_line_column(1)))
                    self.position += 1

            elif self.char() == '*':
                self.tokens.append(Token(TokenKind.MULTIPLY, '*', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '/':
                self.tokens.append(Token(TokenKind.DIVIDE, '/', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '%':
                self.tokens.append(Token(TokenKind.MODULO, '%', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '=':
                if self.next_char() == '=':
                    self.tokens.append(Token(TokenKind.EQUALS, '==', self.get_line_column(), self.get_line_column(2)))
                    self.position += 2
                else:
                    throw_error(self.filename, self.source, ErrorKind.ILLEGAL_CHARACTER, self.get_line_column(), self.get_line_column(1))

            elif self.char() == '!':
                if self.next_char() == '=':
                    self.tokens.append(Token(TokenKind.NOT_EQUALS, '!=', self.get_line_column(), self.get_line_column(2)))
                    self.position += 2
                else:
                    self.tokens.append(Token(TokenKind.CALL, '!', self.get_line_column(), self.get_line_column(1)))
                    self.position += 1

            elif self.char() == '~':
                self.tokens.append(Token(TokenKind.CONTINUE, '^', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '^':
                self.tokens.append(Token(TokenKind.BREAK, '^', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '?':
                self.tokens.append(Token(TokenKind.IF, '?', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == ':':
                self.tokens.append(Token(TokenKind.ELSE, ':', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '&':
                self.tokens.append(Token(TokenKind.LOOP, '&', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '{':
                self.tokens.append(Token(TokenKind.LEFT_CURLY_BRACE, '{', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '}':
                self.tokens.append(Token(TokenKind.RIGHT_CURLY_BRACE, '}', self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() == '>':
                if self.next_char() == '=':
                    self.tokens.append(Token(TokenKind.GREATER_EQUALS, '!=', self.get_line_column(), self.get_line_column(2)))
                    self.position += 2
                else:
                    self.tokens.append(Token(TokenKind.GREATER, '>', self.get_line_column(), self.get_line_column(1)))
                    self.position += 1

            elif self.char() == '<':
                if self.next_char() == '=':
                    self.tokens.append(Token(TokenKind.LESS_EQUALS, '!=', self.get_line_column(), self.get_line_column(2)))
                    self.position += 2
                else:
                    self.tokens.append(Token(TokenKind.LESS, '<', self.get_line_column(), self.get_line_column(1)))
                    self.position += 1

            elif self.char() in ['T', 'F']:
                self.tokens.append(Token(TokenKind.BOOLEAN, self.char(), self.get_line_column(), self.get_line_column(1)))
                self.position += 1

            elif self.char() in ['\'', '"']:
                start = self.get_line_column()
                buffer = self.char()
                self.position += 1

                while self.char() != buffer[0]:
                    if self.char() == '\\':
                        self.position += 1
                        
                        if self.char() in ['n', 't', '\\']:
                            buffer += ['\n', '\t', '\\'] \
                                [['n', 't', '\\'].index(self.char())]
                        elif self.char() == quote:
                            buffer += self.char()
                        else:
                            buffer += '\\' + self.char()

                    elif self.char() is None: # if it reaches end of file
                        throw_error(self.filename, self.source, ErrorKind.UNTERMINATED_STRING_LITERAL, start, self.get_line_column())

                    else:
                        buffer += self.char()

                    self.position += 1

                buffer += self.char()
                self.tokens.append(Token(TokenKind.STRING, buffer, start, self.get_line_column(1)))

                self.position += 1

            elif self.char() == '`':
                start = self.get_line_column()
                buffer = self.char()
                self.position += 1

                while self.char() != '`':
                    buffer += self.char()
                    self.position += 1

                buffer += self.char()
                self.tokens.append(Token(TokenKind.IMPORT, buffer, start, self.get_line_column(1)))

                self.position += 1

            elif self.char().isnumeric():
                start = self.get_line_column()
                buffer = self.char()
                self.position += 1

                while self.char().isnumeric() \
                      or (self.char() == '.' and '.' not in buffer) \
                      or self.char() == '_':

                    # TODO: make it so ending _ is ignored (not errored)
                    # so that it can be scanned again
                    if self.char() == '_':
                        if self.next_char().isnumeric():
                            self.position += 1
                            continue
                        else:
                            throw_error(self.filename, self.source, ErrorKind.INVALID_NUMBER_LITERAL, start, self.get_line_column())

                    buffer += self.char()
                    self.position += 1

                self.tokens.append(Token(TokenKind.NUMBER, buffer, start, self.get_line_column()))

            elif self.char().isalpha() or self.char() == '_':
                start = self.get_line_column()
                buffer = self.char()
                self.position += 1

                while self.char().isalnum() or self.char() == '_':
                    buffer += self.char()
                    self.position += 1

                self.tokens.append(Token(TokenKind.IDENTIFIER, buffer, start, self.get_line_column()))

            else:
                throw_error(self.filename, self.source, ErrorKind.ILLEGAL_CHARACTER, self.get_line_column(), self.get_line_column(1))

        self.tokens.append(Token(TokenKind.END_OF_FILE, None, self.get_line_column(), self.get_line_column(1)))
