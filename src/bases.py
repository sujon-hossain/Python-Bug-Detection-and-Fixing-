"""Convert integers to and from other number bases (2-36)."""
from .errors import EvalError

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def _check_base(base):
    if not isinstance(base, int) or not 2 <= base <= 36:
        raise EvalError("Base must be a whole number from 2 to 36")


def to_base(n, base):
    _check_base(base)
    if isinstance(n, bool) or not isinstance(n, int):
        raise EvalError("Only whole numbers can be converted to another base")
    if n == 0:
        return "0"
    sign = "-" if n < 0 else ""
    n = abs(n)
    out = []
    while n:
        n, remainder = divmod(n, base)
        out.append(DIGITS[remainder])
    return sign + "".join(out)


def from_base(text, base):
    _check_base(base)
    text = text.strip().lower()
    negative = text.startswith("-")
    if negative:
        text = text[1:]
    if not text:
        raise EvalError("No digits to convert")
    value = 0
    for ch in text:
        d = DIGITS.find(ch)
        if d == -1 or d > base:
            raise EvalError(f"Invalid digit {ch!r} for base {base}")
        value = value * base + d
    return -value if negative else value
