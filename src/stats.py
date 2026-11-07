"""Basic statistics on a list of numbers."""
import math

from .errors import EvalError


def _check(values):
    if not values:
        raise EvalError("No data given")


def mean(values):
    _check(values)
    return sum(values) / len(values)


def median(values):
    _check(values)
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid] + s[mid + 1]) / 2


def mode(values):
    """Return a sorted list of the most common values ([] if nothing repeats)."""
    _check(values)
    counts = {}
    for x in values:
        counts[x] = counts.get(x, 0) + 1
    top = max(counts.values())
    return sorted(k for k, c in counts.items() if c == top)


def variance(values, sample=False):
    _check(values)
    n = len(values)
    if sample and n < 2:
        raise EvalError("Sample variance needs at least 2 values")
    m = mean(values)
    ss = sum((x - m) ** 2 for x in values)
    return ss / (n if sample else n - 1)


def stdev(values, sample=False):
    return math.sqrt(variance(values, sample))
