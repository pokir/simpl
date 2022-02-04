from enum import Enum, auto
import sys

from lexer import lexer
from parser import parser


Lexer = lexer.Lexer
Parser = parser.Parser


def main():
    filename = sys.argv[1]

    with open(filename, 'r') as f:
        source = f.read()

    lxr = Lexer(source)
    lxr.lex()
    prsr = Parser(lxr.tokens)
    prsr.parse()

    print(list(map(lambda token: (token.kind, token.literal), lxr.tokens)))
    print()
    print(prsr.tree)


if __name__ == '__main__':
    main()
