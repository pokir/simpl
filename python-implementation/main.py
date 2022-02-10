import os
import sys

from enum import Enum, auto
from errors import errors
from generator import generator
from lexer import lexer
from parser import parser


Lexer = lexer.Lexer
Parser = parser.Parser
Generator = generator.Generator
# For the future when it will show all errors:
#show_errors = errors.show_errors


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

    gnrtr = Generator(prsr.tree)
    gnrtr.generate()
    
    print('Generator output:')
    print(gnrtr.generated_code)
    print()

    #with open('out.cpp', 'w') as f:
    #    f.write(gnrtr.generated_code)

    os.system(f'echo {repr(gnrtr.generated_code)} | g++ -x c++ -std=c++17 -')

    # For the future when it will show all errors:
    #show_errors()


if __name__ == '__main__':
    main()
