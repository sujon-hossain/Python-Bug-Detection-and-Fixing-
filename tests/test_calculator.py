import unittest

from calculator import Calculator, format_number
from calculator.errors import EvalError, ParseError


class FormatNumberTests(unittest.TestCase):
    def test_whole_floats_have_no_decimal_point(self):
        self.assertEqual(format_number(4.0), "4")
        self.assertEqual(format_number(-0.0), "0")
        self.assertEqual(format_number(10 ** 20), "100000000000000000000")

    def test_decimals_use_ten_significant_digits(self):
        self.assertEqual(format_number(1 / 3), "0.3333333333")
        self.assertEqual(format_number(2.5), "2.5")
        self.assertEqual(format_number(0.1 + 0.2), "0.3")

    def test_huge_floats_use_scientific_notation(self):
        self.assertEqual(format_number(1e20), "1e+20")

    def test_special_values(self):
        self.assertEqual(format_number(float("inf")), "inf")


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_evaluate(self):
        self.assertEqual(self.calc.evaluate("2+2"), 4)
        self.assertEqual(self.calc.run("10/4"), "2.5")
        self.assertEqual(self.calc.run("2^0.5"), "1.414213562")

    def test_assignment_and_use(self):
        self.assertEqual(self.calc.evaluate("x = 5"), 5)
        self.assertEqual(self.calc.evaluate("x * 2"), 10)
        self.assertEqual(self.calc.evaluate("y = x + 1"), 6)
        self.assertEqual(self.calc.evaluate("x + y"), 11)

    def test_variable_names_are_case_insensitive(self):
        self.calc.evaluate("X = 5")
        self.assertEqual(self.calc.evaluate("x*2"), 10)
        self.assertEqual(self.calc.evaluate("X*3"), 15)

    def test_ans(self):
        self.calc.evaluate("2+3")
        self.assertEqual(self.calc.evaluate("ans*2"), 10)
        self.assertEqual(self.calc.evaluate("ans+1"), 11)

    def test_history_is_recorded(self):
        self.calc.evaluate("1+1")
        self.calc.evaluate("x = 4")
        self.assertEqual(len(self.calc.history), 2)
        self.assertEqual(self.calc.history.last().expression, "x = 4")
        self.assertEqual(self.calc.history.last().result, 4)

    def test_failed_evaluation_is_not_recorded(self):
        with self.assertRaises(EvalError):
            self.calc.evaluate("1/0")
        self.assertEqual(len(self.calc.history), 0)
        with self.assertRaises(EvalError):
            self.calc.evaluate("ans")

    def test_empty_expression(self):
        for text in ("", "   "):
            with self.assertRaises(ParseError):
                self.calc.evaluate(text)

    def test_bad_assignment_targets(self):
        with self.assertRaises(ParseError):
            self.calc.evaluate("2x = 5")
        with self.assertRaises(ParseError):
            self.calc.evaluate("5 = x")
        with self.assertRaises(EvalError):
            self.calc.evaluate("pi = 3")
        with self.assertRaises(EvalError):
            self.calc.evaluate("sqrt = 3")

    def test_history_size_is_configurable(self):
        calc = Calculator(history_size=2)
        for expr in ("1+1", "2+2", "3+3"):
            calc.evaluate(expr)
        self.assertEqual(len(calc.history), 2)


if __name__ == "__main__":
    unittest.main()
