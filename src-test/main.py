from enum import Enum, auto
import sys

from enums import *
from lexer import Lexer
from parser import Parser
from token import Token


def main():
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        source = f.read()

    lexer = Lexer(source)
    lexer.lex()

    print(list(map(lambda token: (token.kind, token.literal), lexer.tokens)))

    parser = Parser(lexer.tokens)
    parser.parse()

    print(parser.tree)


if __name__ == '__main__':
    main()
