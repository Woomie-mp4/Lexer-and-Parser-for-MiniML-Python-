This was coded in Python 3.14 with only standard libraries used (re, typing, dataclasses, sys)
Contains:
    tokens.py - defines token class
    lexer.py - the lexter, tokenizes the source file into a list of tokens
    ast_nodes.py - defines the ast node class definitions
    parser.py - the parser, recursive descent parser to build the AST
    main.py - driver program
lexer.py and parser.py uses lines from the example lexer and parser shown in class.
Run python3 main.py testfile.ml in the terminal. Replace the testfile with whatever the .ml file is called.
From this folder with a MiniML source file added, run: python3 main.py testfile.ml. Replace the testfile with whatever the name of the file is called eg. test1, test2 etc.
