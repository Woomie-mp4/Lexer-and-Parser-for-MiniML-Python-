from tokens import Token
from ast_nodes import (IntLiteral, BoolLiteral, Variable, BinaryOp, UnaryOp, Let, If, Fun, App)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def match(self, expected_type: str) -> Token:
        if self.current_token.type == expected_type:
            tok = self.current_token
            self.current_token = self.lexer.get_next_token()
            return tok
        else:
            self.error(f"Expected {expected_type}, instead got {self.current_token.type}")

    def error(self, message: str):
        raise SyntaxError(f"Parse error: {message} at line {self.current_token.line}, column {self.current_token.column!r}")

    def parse(self):
        node = self.expr()
        if self.current_token.type != 'EOF':
            raise SyntaxError(f"Unexpected token {self.current_token.type} at line {self.current_token.line}, column {self.current_token.column}")
        return node

    #expr -> let_expr | if_expr | fun_expr | or_expr
    def expr(self):
        if self.current_token.type == 'LET':
            return self.let_expr()
        elif self.current_token.type == 'IF':
            return self.if_expr()
        elif self.current_token.type == 'FUN':
            return self.fun_expr()
        elif self.current_token.type in ('NOT', 'MINUS', 'INT', 'BOOL', 'ID', 'LPAREN'):
            return self.or_expr()
        else:
            self.error("Invalid start of expression")

    #let_expr -> LET [REC] ID {ID} EQ expr IN expr
    def let_expr(self):
        self.match('LET')
        is_rec = False
        if self.current_token.type == 'REC':
            self.match('REC')
            is_rec = True
        name = self.match('ID').value
        params = []
        while self.current_token.type == 'ID':
            params.append(self.match('ID').value)
        self.match('EQ')
        value = self.expr()
        self.match('IN')
        body = self.expr()
        return Let(is_rec, name, params, value, body)

    #if_expr -> IF expr THEN expr ELSE expr
    def if_expr(self):
        self.match('IF')
        cond = self.expr()
        self.match('THEN')
        then_branch = self.expr()
        self.match('ELSE')
        else_branch = self.expr()
        return If(cond, then_branch, else_branch)

    #fun_expr -> FUN {ID} ARROW expr
    def fun_expr(self):
        self.match('FUN')
        params = []
        while self.current_token.type == 'ID':
            params.append(self.match('ID').value)
        if not params:
            self.error("Expected at least one parameter after 'fun'")
        self.match('ARROW')
        body = self.expr()
        return Fun(params, body)

    #or_expr -> and_expr (OR and_expr)*
    def or_expr(self):
        left = self.and_expr()
        while self.current_token.type == 'OR':
            self.match('OR')
            right = self.and_expr()
            left = BinaryOp('||', left, right)
        return left

    #and_expr -> comp_expr (AND comp_expr)*
    def and_expr(self):
        left = self.comp_expr()
        while self.current_token.type == 'AND':
            self.match('AND')
            right = self.comp_expr()
            left = BinaryOp('&&', left, right)
        return left

    #comp_expr -> add_expr [comp_op add_expr]
    def comp_expr(self):
        left = self.add_expr()
        if self.current_token.type in ('EQ', 'NEQ', 'L', 'G', 'LE', 'GE'):
            op_tok = self.match(self.current_token.type)
            right = self.add_expr()
            left = BinaryOp(op_tok.value, left, right)
        return left

    #add_expr -> mul_expr (add_op mul_expr)*
    def add_expr(self):
        left = self.mul_expr()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op_tok = self.match(self.current_token.type)
            right = self.mul_expr()
            left = BinaryOp(op_tok.value, left, right)
        return left

    #mul_expr -> unary_expr (mul_op unary_expr)*
    def mul_expr(self):
        left = self.unary_expr()
        while self.current_token.type in ('TIMES', 'DIVIDE'):
            op_tok = self.match(self.current_token.type)
            right = self.unary_expr()
            left = BinaryOp(op_tok.value, left, right)
        return left

    #unary_expr -> NOT unary_expr | MINUS unary_expr | app_expr
    def unary_expr(self):
        if self.current_token.type == 'NOT':
            self.match('NOT')
            return UnaryOp('not', self.unary_expr())
        elif self.current_token.type == 'MINUS':
            self.match('MINUS')
            return UnaryOp('-', self.unary_expr())
        else:
            return self.app_expr()

    #app_expr -> primary primary*
    def app_expr(self):
        node = self.primary()
        while self.current_token.type in ('INT', 'BOOL', 'ID', 'LPAREN'):
            arg = self.primary()
            node = App(node, arg)
        return node

    #primary -> INT | BOOL | ID | LPAREN expr RPAREN
    def primary(self):
        tok = self.current_token
        if tok.type == 'INT':
            self.match('INT')
            return IntLiteral(int(tok.value))
        elif tok.type == 'BOOL':
            self.match('BOOL')
            return BoolLiteral(tok.value == 'true')
        elif tok.type == 'ID':
            self.match('ID')
            return Variable(tok.value)
        elif tok.type == 'LPAREN':
            self.match('LPAREN')
            node = self.expr()
            self.match('RPAREN')
            return node
        else:
            self.error("Invalid factor")