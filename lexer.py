import re
from typing import List
from tokens import Token

class Lexer: 
    TOKEN_SPECS = [
        ('COMMENT', r'\(\*.*?\*\)'), 
        ('INT',     r'\d+'), 
        ('ARROW',   r'->'),
        ('TIMES',   r'\*'),
        ('DIVIDE',  r'/'),
        ('PLUS',    r'\+'),
        ('MINUS',   r'-'),
        ('EQ',      r'='),
        ('NEQ',     r'<>'),
        ('LE',      r'<='), 
        ('GE',      r'>='),
        ('L',       r'<'),
        ('G',       r'>'),
        ('AND',     r'&&'),
        ('OR',      r'\|\|'),
        ('LPAREN',  r'\('),
        ('RPAREN',  r'\)'),
        ('ID',      r'[a-z][a-zA-Z0-9_]*'),
        ('NEWLINE', r'\n'),
        ('WS',      r'[ \t]+'),
        ('MISMATCH',r'.'),
    ]
    KEYWORDS = {'let', 'in', 'if', 'then', 'else', 'fun', 'rec', 'not'}
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECS)

    def __init__(self, code: str):
        self.tokens = self.tokenize(code)
        self.pos = 0

    def tokenize(self, code: str) -> List[Token]:
        tokens = []
        line_num = 1
        line_start = 0

        for match in re.finditer(self.tok_regex, code):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1

            if kind == 'NEWLINE':
                line_num += 1
                line_start = match.end()
            elif kind == 'WS':
                continue
            elif kind == 'COMMENT':
                line_num += value.count('\n')
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f'Unexpected character {value!r} at line {line_num}, column {column}')
            elif kind == 'ID':
                if value in ('true', 'false'):
                    kind = 'BOOL'
                elif value in self.KEYWORDS:
                    kind = value.upper()
                tokens.append(Token(kind, value, line_num, column))
            else: 
                tokens.append(Token(kind, value, line_num, column))
        #Add a End of File token
        tokens.append(Token('EOF', '', line_num, 0)) 
        return tokens

    def get_next_token(self) -> Token:
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return self.tokens[-1]