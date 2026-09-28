from dataclasses import dataclass
from typing import List

class ASTNode:
    pass

#dataclass automatically writes the __init__
@dataclass
class IntLiteral(ASTNode):
    value: int

    def __repr__(self):
        return f"IntLiteral({self.value})"

@dataclass
class BoolLiteral(ASTNode):
    value: bool

    def __repr__(self):
        return f"BoolLiteral({self.value})"

@dataclass
class Variable(ASTNode):
    name: str

    def __repr__(self):
        return f"Variable({self.name})"

@dataclass
class BinaryOp(ASTNode):
    op: str
    left: ASTNode
    right: ASTNode

    def __repr__(self):
        return f"BinaryOp({self.op!r}, {self.left!r}, {self.right!r})"

@dataclass
class UnaryOp(ASTNode):
    op: str
    operand: ASTNode

    def __repr__(self):
        return f"UnaryOp({self.op!r}, {self.operand!r})"

@dataclass
class Let(ASTNode):
    is_rec: bool
    name: str
    params: List[str]
    value: ASTNode
    body: ASTNode

    def __repr__(self):
        kind = 'let rec' if self.is_rec else "let"
        return f"Let({kind}, {self.name!r}, params={self.params}, value={self.value!r}, body={self.body!r})"

@dataclass
class If(ASTNode):
    cond: ASTNode
    then_branch: ASTNode
    else_branch: ASTNode

    def __repr__(self):
        return f"If({self.cond!r}, {self.then_branch!r}, {self.else_branch!r})"

@dataclass
class Fun(ASTNode):
    params: List[str]
    body: ASTNode

    def __repr__(self):
        return f"Fun({self.params}, {self.body!r})"

@dataclass
class App(ASTNode):
    func: ASTNode
    arg: ASTNode

    def __repr__(self):
        return f"App({self.func!r}, {self.arg!r})"