import unittest

from calculator.converter import convert
from calculator.errors import UnitError


class LinearUnitTests(unittest.TestCase):
    def test_length(self):
        self.assertAlmostEqual(convert(1, "km", "m"), 1000)
        self.assertAlmostEqual(convert(1, "ft", "in"), 12)
        self.assertAlmostEqual(convert(1, "in", "cm"), 2.54)
        self.assertAlmostEqual(convert(1, "yd", "ft"), 3)

    def test_miles(self):
        self.assertAlmostEqual(convert(1, "mi", "km"), 1.609344, places=6)
        self.assertAlmostEqual(convert(5, "km", "mi"), 3.106856, places=6)

    def test_mass(self):
        self.assertAlmostEqual(convert(1500, "g", "kg"), 1.5)
        self.assertAlmostEqual(convert(1, "lb", "kg"), 0.45359237, places=8)
        self.assertAlmostEqual(convert(1, "oz", "g"), 28.349523125, places=6)

    def test_time(self):
        self.assertAlmostEqual(convert(2, "h", "min"), 120)
        self.assertAlmostEqual(convert(1, "day", "h"), 24)

    def test_case_insensitive_and_identity(self):
        self.assertAlmostEqual(convert(3, "KM", "M"), 3000)
        self.assertAlmostEqual(convert(7, "m", "m"), 7)


class TemperatureTests(unittest.TestCase):
    def test_celsius_fahrenheit(self):
        self.assertAlmostEqual(convert(100, "c", "f"), 212)
        self.assertAlmostEqual(convert(212, "f", "c"), 100)
        self.assertAlmostEqual(convert(-40, "c", "f"), -40)

    def test_kelvin(self):
        self.assertAlmostEqual(convert(0, "c", "k"), 273.15)
        self.assertAlmostEqual(convert(32, "f", "k"), 273.15)
        self.assertAlmostEqual(convert(300, "k", "c"), 26.85)

    def test_absolute_zero_is_allowed(self):
        self.assertAlmostEqual(convert(0, "k", "c"), -273.15)
        self.assertAlmostEqual(convert(-273.15, "c", "k"), 0)

    def test_below_absolute_zero(self):
        with self.assertRaises(UnitError):
            convert(-300, "c", "k")
        with self.assertRaises(UnitError):
            convert(-1, "k", "c")


class ErrorTests(unittest.TestCase):
    def test_unknown_unit(self):
        with self.assertRaises(UnitError):
            convert(1, "parsec", "m")
        with self.assertRaises(UnitError):
            convert(1, "m", "furlong")

    def test_mismatched_categories(self):
        for src, dst in (("km", "kg"), ("c", "m"), ("h", "g")):
            with self.subTest(src=src, dst=dst):
                with self.assertRaises(UnitError):
                    convert(1, src, dst)


if __name__ == "__main__":
    unittest.main()
