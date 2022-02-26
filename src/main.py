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
    filename = ''.join(filepath.split('/')[-1].split('.')[:-1])

    #files = ['./src/std/simpl/std.simpl', filepath]
    files = [filepath]

    trees = []

    # Lex and parse all files
    for file in files:
        with open(file, 'r') as f:
            source = f.read()

        lxr = Lexer(file, source)
        lxr.lex()
        prsr = Parser(file, source, lxr.tokens)
        prsr.parse()
        trees.append(prsr.tree)

    # Combine the abstract syntax trees
    combined_tree = trees[0]
    combined_tree.start = None
    combined_tree.end = None
    for tree in trees[1:]:
        combined_tree.children += tree.children

    # Generate the code from the combined abstract syntax tree
    gnrtr = Generator(combined_tree)
    gnrtr.generate()
    
    if '-v' in sys.argv:
        print('Abstract syntax tree:')
        print(combined_tree)
        print()

        print('Generator output:')
        print(gnrtr.generated_code)
        print()

    if not os.path.isdir('build'):
        os.mkdir('build')

    with open(f'build/{filename}.cpp', 'w') as f:
        f.write(gnrtr.generated_code)

    os.system(f'g++ -x c++ -std=c++1z -o build/{filename} build/{filename}.cpp')

    # For the future when it will show all errors:
    #show_errors()


if __name__ == '__main__':
    main()
