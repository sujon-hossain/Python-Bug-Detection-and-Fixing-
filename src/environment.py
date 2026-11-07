"""Variables, constants and settings used while evaluating."""
import math

from .errors import EvalError
from .functions import FUNCTIONS

CONSTANTS = {"pi": math.pi, "e": math.e}


class Environment:
    def __init__(self):
        self.variables = {}
        self.angle_mode = "rad"

    def lookup(self, name):
        if name in CONSTANTS:
            return CONSTANTS[name]
        if name in self.variables:
            return self.variables[name]
        raise EvalError(f"Unknown variable '{name}'")

    def assign(self, name, value):
        if name in CONSTANTS or name in FUNCTIONS:
            raise EvalError(f"Cannot assign to '{name}'")
        self.variables[name] = value

    def set_angle_mode(self, mode):
        if mode not in ("deg", "rad"):
            raise EvalError("Angle mode must be 'deg' or 'rad'")
        self.angle_mode = mode
