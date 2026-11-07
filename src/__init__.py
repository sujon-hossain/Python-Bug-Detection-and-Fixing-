"""Debug-practice calculator package."""
from .calculator import Calculator, format_number
from .errors import CalcError

__all__ = ["Calculator", "CalcError", "format_number"]
__version__ = "1.0"
