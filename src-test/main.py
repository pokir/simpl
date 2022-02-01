from enum import Enum, auto
import sys


class TokenKind(Enum):
    IDENTIFIER = auto()
    PUSH = auto()
    POP = auto()
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    STRING = auto()
    NUMBER = auto()


class Token:
    def __init__(self, kind, literal):
        self.kind = kind
        self.literal = literal

    def __str__(self):
        return 


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
    
    def char(self):
        return self.source[self.position]

    def lex(self):
        tokens = []

        while self.position < len(self.source):

            if self.char() == '.':
                tokens.append(Token(TokenKind.PUSH, self.char()))
                self.position += 1

            elif self.char() == '@':
                tokens.append(Token(TokenKind.POP, self.char()))
                self.position += 1

            elif self.char() == '+':
                tokens.append(Token(TokenKind.ADD, self.char()))
                self.position += 1

            elif self.char() == '-':
                tokens.append(Token(TokenKind.SUBTRACT, self.char()))
                self.position += 1

            elif self.char() == '*':
                tokens.append(Token(TokenKind.MULTIPLY, self.char()))
                self.position += 1

            elif self.char() == '/':
                tokens.append(Token(TokenKind.DIVIDE, self.char()))
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

                    else:
                        buffer += self.char()

                    self.position += 1

                self.position += 1
                tokens.append(Token(TokenKind.STRING, buffer))

            elif self.char() in [' ', '\n']:
                self.position += 1

            else:
                raise SyntaxError

        return tokens


def main():
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        source = f.read()

    lexer = Lexer(source)
    tokens = lexer.lex()

    print(list(map(lambda token: (token.kind, token.literal), tokens)))

    print(tokens[-1].literal)


if __name__ == '__main__':
    main()
