"""Walk a syntax tree and compute its value."""
from .errors import EvalError
from .functions import FUNCTIONS
from .parser import Binary, Call, Num, Unary, Var

MAX_EXPONENT = 10_000


def evaluate(node, env):
    if isinstance(node, Num):
        return node.value
    if isinstance(node, Var):
        return env.lookup(node.name)
    if isinstance(node, Unary):
        value = evaluate(node.operand, env)
        return -value if node.op == "-" else value
    if isinstance(node, Binary):
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)
        return apply_binary(node.op, left, right)
    if isinstance(node, Call):
        args = [evaluate(arg, env) for arg in node.args]
        return call_function(node.name, args, env)
    raise EvalError(f"Cannot evaluate {node!r}")


def apply_binary(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise EvalError("Division by zero")
        return a / b
    if op == "%":
        return a % b
    if op == "^":
        if a == 0 and b <= 0:
            raise EvalError("Zero cannot be raised to a negative power")
        if abs(a) > 1 and abs(b) > MAX_EXPONENT:
            raise EvalError("Exponent too large")
        try:
            result = a ** b
        except OverflowError:
            raise EvalError("Result too large")
        if isinstance(result, complex):
            raise EvalError("Result is not a real number")
        return result
    raise EvalError(f"Unknown operator '{op}'")


def call_function(name, args, env):
    entry = FUNCTIONS.get(name)
    if entry is None:
        raise EvalError(f"Unknown function '{name}'")
    lo, hi, func = entry
    if len(args) < lo or (hi is not None and len(args) > hi + 1):
        if hi is None:
            expected = f"at least {lo}"
        elif lo == hi:
            expected = str(lo)
        else:
            expected = f"{lo} to {hi}"
        raise EvalError(f"{name}() takes {expected} argument(s), got {len(args)}")
    try:
        return func(env, *args)
    except (ValueError, OverflowError) as exc:
        raise EvalError(f"{name}(): {exc}")
