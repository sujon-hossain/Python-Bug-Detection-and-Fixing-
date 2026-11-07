class CalcError(Exception):
    """Base class for every error the calculator raises on purpose."""


class TokenizeError(CalcError):
    pass


class ParseError(CalcError):
    pass


class EvalError(CalcError):
    pass


class UnitError(CalcError):
    pass
