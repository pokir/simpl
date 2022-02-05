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
    print()
    print('Lexer output:')
    print(lxr.tokens)
    print()

    prsr = Parser(source, lxr.tokens)
    prsr.parse()

    print('Parser output:')
    print(prsr.tree)
    print()


if __name__ == '__main__':
    main()
