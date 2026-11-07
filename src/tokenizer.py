"""Turn an expression string into a list of tokens."""
from dataclasses import dataclass

from .errors import TokenizeError

NUMBER, IDENT, OP, LPAREN, RPAREN, COMMA, EOF = (
    "NUMBER", "IDENT", "OP", "LPAREN", "RPAREN", "COMMA", "EOF",
)
OPERATORS = "+-*/^"


@dataclass(frozen=True)
class Token:
    type: str
    value: object
    pos: int


def tokenize(text):
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            start = i
            dot = 0
            while i < n and (text[i].isdigit() or text[i] == "."):
                if text[i] == ".":
                    dot += 1
                i += 1
            raw = text[start:i]
            if dot > 2 or raw == ".":
                raise TokenizeError(f"Invalid number '{raw}' at position {start}")
            tokens.append(Token(NUMBER, float(raw) if dot else int(raw), start))
            continue
        if ch.isalpha() or ch == "_":
            start = i
            while i < n and (text[i].isalnum() or text[i] == "_"):
                i += 1
            tokens.append(Token(IDENT, text[start:i], start))
            continue
        if ch in OPERATORS:
            tokens.append(Token(OP, ch, i))
        elif ch == "(":
            tokens.append(Token(LPAREN, ch, i))
        elif ch == ")":
            tokens.append(Token(RPAREN, ch, i))
        elif ch == ",":
            tokens.append(Token(COMMA, ch, i))
        else:
            raise TokenizeError(f"Unexpected character {ch!r} at position {i}")
        i += 1
    tokens.append(Token(EOF, None, n))
    return tokens
