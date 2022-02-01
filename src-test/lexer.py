from token import Token
from enums import *


class Lexer:
    def __init__(self, source):
        self.source = source
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

    def lex(self):
        #while self.position < len(self.source):
        while self.char() is not None:

            if self.char() in [' ', '\n', '\t']:
                self.position += 1

            elif self.char() == '#':
                while self.char() != '\n':
                    self.position += 1

            elif self.char() == '.':
                self.tokens.append(Token(TokenKind.PUSH, '.'))
                self.position += 1

            elif self.char() == '@':
                self.tokens.append(Token(TokenKind.POP, '@'))
                self.position += 1

            elif self.char() == '+':
                self.tokens.append(Token(TokenKind.ADD, '+'))
                self.position += 1

            elif self.char() == '-':
                if self.next_char() == '>':
                    self.tokens.append(Token(TokenKind.RETURN, '->'))
                    self.position += 2
                else:
                    self.tokens.append(Token(TokenKind.SUBTRACT, '-'))
                    self.position += 1

            elif self.char() == '*':
                self.tokens.append(Token(TokenKind.MULTIPLY, '*'))
                self.position += 1

            elif self.char() == '/':
                self.tokens.append(Token(TokenKind.DIVIDE, '/'))
                self.position += 1

            elif self.char() == '%':
                self.tokens.append(Token(TokenKind.MODULE, '%'))
                self.position += 1

            elif self.char() == '=':
                if self.next_char() == '=':
                    self.tokens.append(Token(TokenKind.EQUALS, '=='))
                    self.position += 2
                else:
                    raise SyntaxError(SyntaxErrorKind.INVALID_SYNTAX)

            elif self.char() == '!':
                if self.next_char() == '=':
                    self.tokens.append(Token(TokenKind.NOT_EQUALS, '!='))
                    self.position += 2
                else:
                    self.tokens.append(Token(TokenKind.CALL, '!'))

            elif self.char() == '^':
                self.tokens.append(Token(TokenKind.BREAK, '^'))
                self.position += 1

            elif self.char() == '?':
                self.tokens.append(Token(TokenKind.IF, '?'))
                self.position += 1

            elif self.char() == ':':
                self.tokens.append(Token(TokenKind.ELSE, ':'))
                self.position += 1

            elif self.char() == '&':
                self.tokens.append(Token(TokenKind.LOOP, '&'))
                self.position += 1

            elif self.char() == '>':
                if self.next_char() == '=':
                    self.tokens.append(Token(TokenKind.GREATER_OR_EQUALS, '!='))
                    self.position += 2
                else:
                    self.tokens.append(Token(TokenKind.GREATER, '>'))
                    self.position += 1

            elif self.char() == '<':
                if self.next_char() == '=':
                    self.tokens.append(Token(TokenKind.LESS_OR_EQUALS, '!='))
                    self.position += 2
                else:
                    self.tokens.append(Token(TokenKind.LESS, '<'))
                    self.position += 1

            elif self.char() in ['\'', '"']:
                quote = self.char()

                self.position += 1

                buffer = ''

                while self.char() != quote:
                    if self.char() == '\\':
                        self.position += 1
                        
                        if self.char() in ['n', 't', '\\']:
                            buffer += ['\n', '\t', '\\'] \
                                [['n', 't', '\\'].index(self.char())]
                        elif self.char() == quote:
                            buffer += self.char()
                        else:
                            buffer += '\\' + self.char()

                    elif self.char() is None:
                        raise SyntaxError(SyntaxErrorKind.UNTERMINATED_STRING_LITERAL)

                    else:
                        buffer += self.char()

                    self.position += 1

                self.position += 1
                self.tokens.append(Token(TokenKind.STRING, buffer))

            elif self.char().isnumeric():
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
                            raise SyntaxError(SyntaxErrorKind.INVALID_NUMBER_LITERAL)

                    buffer += self.char()
                    self.position += 1

                self.tokens.append(Token(TokenKind.NUMBER, buffer))

            elif self.char().isalpha() or self.char() == '_':
                buffer = self.char()
                self.position += 1

                while self.char().isalnum() or self.char() == '_':
                    buffer += self.char()
                    self.position += 1

                #if self.char() not in [' ', '\n', '\t', '!']:
                    #raise SyntaxError(SyntaxErrorKind.INVALID_SYNTAX)

                self.tokens.append(Token(TokenKind.IDENTIFIER, buffer))

            else:
                raise SyntaxError(SyntaxErrorKind.INVALID_SYNTAX)
