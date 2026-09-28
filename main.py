import sys
from lexer import Lexer
from parser import Parser


def main():
    filename = sys.argv[1]

    #Convert the file to 1 string with a missing file error
    #Side Node: I had to add the encoding part because my file couldn't get read but I'm not sure if it's intended
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            source = f.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='utf-16') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {filename}")
        sys.exit(1)

    #Runs the lexer
    try:
        lexer = Lexer(source)
    except SyntaxError as e:
        print(f"Lexical error: {e}")
        sys.exit(1)

    #Runs the Parser and builds the AST tree
    try:
        parser = Parser(lexer)
        ast = parser.parse()
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        sys.exit(1)

    print(ast)

main()