"""Unit conversion (length, mass, time, temperature)."""
from .errors import UnitError

LINEAR = {
    "length": {"m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001,
               "mi": 1609.34, "yd": 0.9144, "ft": 0.3048, "in": 0.0254},
    "mass": {"kg": 1.0, "g": 0.001, "mg": 1e-6, "lb": 0.45359237, "oz": 0.028349523125},
    "time": {"s": 1.0, "min": 60.0, "h": 3600.0, "day": 86400.0},
}
TEMPERATURES = {"c", "f", "k"}


def _category(unit):
    if unit in TEMPERATURES:
        return "temperature"
    for name, units in LINEAR.items():
        if unit in units:
            return name
    raise UnitError(f"Unknown unit '{unit}'")


def _to_kelvin(value, unit):
    if unit == "c":
        return value + 273.15
    if unit == "f":
        return (value - 32) * 9 / 5 + 273.15
    return value


def _from_kelvin(kelvin, unit):
    if unit == "c":
        return kelvin - 273.15
    if unit == "f":
        return (kelvin - 273.15) * 9 / 5 + 32
    return kelvin


def convert(value, src, dst):
    src, dst = src.lower(), dst.lower()
    cs, cd = _category(src), _category(dst)
    if cs == "temperature":
        kelvin = _to_kelvin(value, src)
        if kelvin <= 0:
            raise UnitError("Temperature is below absolute zero")
        return round(_from_kelvin(kelvin, dst), 10)
    return round(value * LINEAR[cs][src] / LINEAR[cs][dst], 10)
