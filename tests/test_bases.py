import unittest

from calculator.bases import from_base, to_base
from calculator.errors import EvalError


class ToBaseTests(unittest.TestCase):
    def test_common_values(self):
        self.assertEqual(to_base(10, 2), "1010")
        self.assertEqual(to_base(255, 16), "ff")
        self.assertEqual(to_base(8, 8), "10")
        self.assertEqual(to_base(35, 36), "z")

    def test_zero_and_negative(self):
        self.assertEqual(to_base(0, 2), "0")
        self.assertEqual(to_base(-5, 2), "-101")

    def test_bad_base(self):
        for base in (1, 37, 0):
            with self.subTest(base=base):
                with self.assertRaises(EvalError):
                    to_base(5, base)

    def test_non_integer(self):
        with self.assertRaises(EvalError):
            to_base(2.5, 2)


class FromBaseTests(unittest.TestCase):
    def test_common_values(self):
        self.assertEqual(from_base("1010", 2), 10)
        self.assertEqual(from_base("FF", 16), 255)
        self.assertEqual(from_base("-101", 2), -5)
        self.assertEqual(from_base("  ff ", 16), 255)

    def test_invalid_digit_for_base(self):
        with self.assertRaises(EvalError):
            from_base("2", 2)
        with self.assertRaises(EvalError):
            from_base("9", 8)
        with self.assertRaises(EvalError):
            from_base("1$", 10)

    def test_highest_valid_digit_is_accepted(self):
        self.assertEqual(from_base("1", 2), 1)
        self.assertEqual(from_base("7", 8), 7)

    def test_empty(self):
        for text in ("", "-", "   "):
            with self.subTest(text=text):
                with self.assertRaises(EvalError):
                    from_base(text, 2)

    def test_roundtrip(self):
        for n in (0, 1, 7, 255, 1000, -42, 123456789):
            for base in (2, 8, 10, 16, 36):
                with self.subTest(n=n, base=base):
                    self.assertEqual(from_base(to_base(n, base), base), n)


if __name__ == "__main__":
    unittest.main()
