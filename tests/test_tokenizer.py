import unittest

from calculator.errors import TokenizeError
from calculator.tokenizer import COMMA, EOF, IDENT, LPAREN, NUMBER, OP, RPAREN, tokenize


def types(text):
    return [t.type for t in tokenize(text)]


def values(text):
    return [t.value for t in tokenize(text)]


class TokenizerTests(unittest.TestCase):
    def test_empty_input_gives_only_eof(self):
        self.assertEqual(types(""), [EOF])

    def test_simple_expression(self):
        self.assertEqual(types("1+2"), [NUMBER, OP, NUMBER, EOF])
        self.assertEqual(values("1+2"), [1, "+", 2, None])

    def test_integers_and_floats(self):
        toks = tokenize("3 4.5")
        self.assertIsInstance(toks[0].value, int)
        self.assertIsInstance(toks[1].value, float)
        self.assertEqual(toks[1].value, 4.5)

    def test_leading_and_trailing_dot(self):
        self.assertEqual(values(".5")[0], 0.5)
        self.assertEqual(values("2.")[0], 2.0)

    def test_whitespace_ignored(self):
        self.assertEqual(values("  1 \t+   2 ")[:3], [1, "+", 2])

    def test_all_operators(self):
        self.assertEqual(values("+-*/^%")[:6], list("+-*/^%"))

    def test_percent_operator(self):
        self.assertEqual(types("10 % 3"), [NUMBER, OP, NUMBER, EOF])

    def test_parentheses_and_comma(self):
        self.assertEqual(types("max(1,2)"),
                         [IDENT, LPAREN, NUMBER, COMMA, NUMBER, RPAREN, EOF])

    def test_identifiers_are_lowercased(self):
        self.assertEqual(values("SQRT Pi")[:2], ["sqrt", "pi"])

    def test_identifier_with_digits_and_underscore(self):
        self.assertEqual(values("my_var2")[0], "my_var2")

    def test_token_positions(self):
        toks = tokenize("12 + x")
        self.assertEqual([t.pos for t in toks], [0, 3, 5, 6])

    def test_two_dots_is_an_error(self):
        with self.assertRaises(TokenizeError):
            tokenize("1.2.3")

    def test_lone_dot_is_an_error(self):
        with self.assertRaises(TokenizeError):
            tokenize(".")

    def test_unexpected_character(self):
        with self.assertRaises(TokenizeError):
            tokenize("3 $ 4")


if __name__ == "__main__":
    unittest.main()
