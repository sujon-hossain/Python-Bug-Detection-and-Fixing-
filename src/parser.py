"""Recursive-descent parser: tokens -> syntax tree.

Grammar (lowest to highest precedence):
    expr   := term (('+' | '-') term)*
    term   := unary (('*' | '/' | '%') unary)*
    unary  := ('+' | '-') unary | power
    power  := atom ('^' unary)?          # right associative
    atom   := NUMBER | IDENT | IDENT '(' [expr (',' expr)*] ')' | '(' expr ')'
"""
from dataclasses import dataclass

from .errors import ParseError
from .tokenizer import COMMA, EOF, IDENT, LPAREN, NUMBER, OP, RPAREN, tokenize


@dataclass(frozen=True)
class Num:
    value: object


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Unary:
    op: str
    operand: object


@dataclass(frozen=True)
class Binary:
    op: str
    left: object
    right: object


@dataclass(frozen=True)
class Call:
    name: str
    args: tuple


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        if tok.type != EOF:
            self.pos += 1
        return tok

    def match_op(self, *ops):
        tok = self.peek()
        if tok.type == OP and tok.value in ops:
            return self.advance()
        return None

    def expect(self, type_):
        tok = self.peek()
        if tok.type != type_:
            raise ParseError(f"Expected {type_} at position {tok.pos}")
        return self.advance()

    def parse(self):
        node = self.expr()
        tok = self.peek()
        if tok.type != EOF:
            raise ParseError(f"Unexpected token {tok.value!r} at position {tok.pos}")
        return node

    def expr(self):
        node = self.term()
        while True:
            tok = self.match_op("+", "-")
            if tok is None:
                return node
            node = Binary(tok.value, node, self.term())

    def term(self):
        node = self.unary()
        while True:
            tok = self.match_op("*", "/", "%")
            if tok is None:
                return node
            node = Binary(tok.value, self.unary(), node)

    def unary(self):
        tok = self.match_op("+", "-")
        if tok is not None:
            return Unary(tok.value, self.unary())
        return self.power()

    def power(self):
        node = self.atom()
        while self.match_op("^"):
            node = Binary("^", node, self.atom())
        return node

    def atom(self):
        tok = self.advance()
        if tok.type == NUMBER:
            return Num(tok.value)
        if tok.type == IDENT:
            if self.peek().type == LPAREN:
                self.advance()
                args = []
                if self.peek().type != RPAREN:
                    args.append(self.expr())
                    while self.peek().type == COMMA:
                        self.advance()
                        args.append(self.expr())
                self.expect(RPAREN)
                return Call(tok.value, tuple(args))
            return Var(tok.value)
        if tok.type == LPAREN:
            node = self.expr()
            self.advance()
            return node
        if tok.type == EOF:
            raise ParseError("Unexpected end of expression")
        raise ParseError(f"Unexpected token {tok.value!r} at position {tok.pos}")


def parse(text):
    return Parser(tokenize(text)).parse()
