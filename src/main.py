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
    filepath = sys.argv[1]
    filename = filepath.split('/')[-1]

    files = ['./src/std/simpl/std.simpl', filepath]

    trees = []

    for file in files:
        with open(file, 'r') as f:
            source = f.read()

        lxr = Lexer(file, source)
        lxr.lex()
        prsr = Parser(file, source, lxr.tokens)
        prsr.parse()
        trees.append(prsr.tree)

    combined_tree = trees[0]
    combined_tree.start = None
    combined_tree.end = None
    for tree in trees[1:]:
        combined_tree.children += tree.children

    gnrtr = Generator(combined_tree)
    gnrtr.generate()
    
    if '-v' in sys.argv:
        print('Abstract syntax tree:')
        print(combined_tree)
        print()

        print('Generator output:')
        print(gnrtr.generated_code)
        print()

    #with open(f'{filepath}.cpp', 'w') as f:
    #    f.write(gnrtr.generated_code)

    if not os.path.isdir('build'):
        os.mkdir('build')
    os.system(f'echo {repr(gnrtr.generated_code)} | g++ -x c++ -std=c++1z -o build/{"".join(filename.split(".")[:-1])} -')


    # For the future when it will show all errors:
    #show_errors()


if __name__ == '__main__':
    main()
