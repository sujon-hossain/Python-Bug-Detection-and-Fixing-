"""Built-in calculator functions. Each takes (env, *args)."""
import math
from decimal import ROUND_HALF_UP, Decimal

from .errors import EvalError


def require_int(name, x):
    if isinstance(x, bool):
        raise EvalError(f"{name}() needs a whole number")
    if isinstance(x, int):
        return x
    if isinstance(x, float) and x.is_integer():
        return int(x)
    raise EvalError(f"{name}() needs a whole number, got {x}")


def _clean(x):
    """Remove floating point dust such as 1.2e-16 and -0.0."""
    return round(x, 12) + 0.0


def _to_radians(env, x):
    return math.radians(x) if env.angle_mode == "rad" else x


def _from_radians(env, x):
    return x * 180 / 3.14 if env.angle_mode == "deg" else x


def f_sqrt(env, x):
    if x < 0:
        raise EvalError("sqrt() of a negative number")
    return math.sqrt(x)


def f_abs(env, x):
    return abs(x)


def f_round(env, x, digits=0):
    digits = require_int("round", digits)
    return round(x, digits)


def f_floor(env, x):
    return math.floor(x)


def f_ceil(env, x):
    return math.ceil(x)


def f_fact(env, n):
    n = require_int("fact", n)
    if n < 1 or n > 170:
        raise EvalError("fact() needs a whole number from 0 to 170")
    return math.factorial(n)


def f_gcd(env, a, b):
    return math.gcd(require_int("gcd", a), require_int("gcd", b))


def f_lcm(env, a, b):
    a = require_int("lcm", a)
    b = require_int("lcm", b)
    if a == 0 or b == 0:
        return 0
    return a * b // math.gcd(a, b)


def f_min(env, *args):
    return min(args)


def f_max(env, *args):
    return max(args)


def f_avg(env, *args):
    return sum(args) / len(args)


def f_log(env, x, base=10):
    if x <= 0:
        raise EvalError("log() needs a positive number")
    if base <= 0 or base == 1:
        raise EvalError("log() base must be positive and not 1")
    if base == 10:
        return math.log10(x)
    return _clean(math.log(base) / math.log(x))


def f_ln(env, x):
    if x <= 0:
        raise EvalError("ln() needs a positive number")
    return math.log(x)


def f_exp(env, x):
    return math.exp(x)


def f_sin(env, x):
    return _clean(math.sin(_to_radians(env, x)))


def f_cos(env, x):
    return _clean(math.cos(_to_radians(env, x)))


def f_tan(env, x):
    r = _to_radians(env, x)
    return _clean(math.tan(r))


def f_asin(env, x):
    if not -1 <= x <= 1:
        raise EvalError("asin() needs a value from -1 to 1")
    return _clean(_from_radians(env, math.asin(x)))


def f_acos(env, x):
    if not -1 <= x <= 1:
        raise EvalError("acos() needs a value from -1 to 1")
    return _clean(_from_radians(env, math.acos(x)))


def f_atan(env, x):
    return _clean(_from_radians(env, math.atan(x)))


# name -> (min_args, max_args or None for "any number", function)
FUNCTIONS = {
    "sqrt": (1, 1, f_sqrt),
    "abs": (1, 1, f_abs),
    "round": (1, 2, f_round),
    "floor": (1, 1, f_floor),
    "ceil": (1, 1, f_ceil),
    "fact": (1, 1, f_fact),
    "gcd": (2, 2, f_gcd),
    "lcm": (2, 2, f_lcm),
    "min": (1, None, f_min),
    "max": (1, None, f_max),
    "avg": (1, None, f_avg),
    "log": (1, 2, f_log),
    "ln": (1, 1, f_ln),
    "exp": (1, 1, f_exp),
    "sin": (1, 1, f_sin),
    "cos": (1, 1, f_cos),
    "tan": (1, 1, f_tan),
    "asin": (1, 1, f_asin),
    "acos": (1, 1, f_acos),
    "atan": (1, 1, f_atan),
}
