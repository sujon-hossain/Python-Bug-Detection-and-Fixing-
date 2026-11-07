import unittest

from calculator.errors import ParseError
from calculator.parser import Binary, Call, Num, Unary, Var, parse


class ParserTests(unittest.TestCase):
    def test_precedence_mul_over_add(self):
        self.assertEqual(parse("1+2*3"), Binary("+", Num(1), Binary("*", Num(2), Num(3))))

    def test_parentheses_override_precedence(self):
        self.assertEqual(parse("(1+2)*3"), Binary("*", Binary("+", Num(1), Num(2)), Num(3)))

    def test_subtraction_is_left_associative(self):
        self.assertEqual(parse("10-3-2"), Binary("-", Binary("-", Num(10), Num(3)), Num(2)))

    def test_division_is_left_associative(self):
        self.assertEqual(parse("8/4/2"), Binary("/", Binary("/", Num(8), Num(4)), Num(2)))

    def test_modulo_has_multiplication_precedence(self):
        self.assertEqual(parse("1+7%4"), Binary("+", Num(1), Binary("%", Num(7), Num(4))))

    def test_power_is_right_associative(self):
        self.assertEqual(parse("2^3^2"), Binary("^", Num(2), Binary("^", Num(3), Num(2))))

    def test_power_binds_tighter_than_unary_minus(self):
        self.assertEqual(parse("-2^2"), Unary("-", Binary("^", Num(2), Num(2))))

    def test_negative_exponent(self):
        self.assertEqual(parse("2^-1"), Binary("^", Num(2), Unary("-", Num(1))))

    def test_double_unary(self):
        self.assertEqual(parse("--3"), Unary("-", Unary("-", Num(3))))

    def test_variable(self):
        self.assertEqual(parse("x+1"), Binary("+", Var("x"), Num(1)))

    def test_function_call_with_several_args(self):
        self.assertEqual(parse("max(1,2,3)"), Call("max", (Num(1), Num(2), Num(3))))

    def test_nested_call(self):
        self.assertEqual(parse("abs(min(1,2))"), Call("abs", (Call("min", (Num(1), Num(2))),)))

    def test_missing_closing_paren(self):
        with self.assertRaises(ParseError):
            parse("(2+3")

    def test_missing_closing_paren_in_call(self):
        with self.assertRaises(ParseError):
            parse("sqrt(4")

    def test_dangling_operator(self):
        with self.assertRaises(ParseError):
            parse("2 +")

    def test_two_numbers_in_a_row(self):
        with self.assertRaises(ParseError):
            parse("1 2")

    def test_stray_closing_paren(self):
        with self.assertRaises(ParseError):
            parse(")")

    def test_trailing_comma_in_call(self):
        with self.assertRaises(ParseError):
            parse("max(1,)")

    def test_empty_input(self):
        with self.assertRaises(ParseError):
            parse("")


if __name__ == "__main__":
    unittest.main()
