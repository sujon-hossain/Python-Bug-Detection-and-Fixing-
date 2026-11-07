import unittest

from calculator.environment import Environment
from calculator.errors import EvalError
from tests.helpers import deg_env, ev


class ArithmeticTests(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(ev("2+3*4"), 14)
        self.assertEqual(ev("(2+3)*4"), 20)
        self.assertEqual(ev("10-3-2"), 5)
        self.assertEqual(ev("7/2"), 3.5)

    def test_chained_division_and_subtraction(self):
        self.assertEqual(ev("8/4/2"), 1)
        self.assertEqual(ev("100/10/5"), 2)

    def test_modulo(self):
        self.assertEqual(ev("10%3"), 1)
        self.assertEqual(ev("-5%3"), 1)

    def test_unary_operators(self):
        self.assertEqual(ev("--3"), 3)
        self.assertEqual(ev("3-(-2)"), 5)
        self.assertEqual(ev("-(2+3)"), -5)
        self.assertEqual(ev("+4"), 4)

    def test_power(self):
        self.assertEqual(ev("2^10"), 1024)
        self.assertEqual(ev("2^3^2"), 512)
        self.assertEqual(ev("2^-1"), 0.5)
        self.assertEqual(ev("-2^2"), -4)
        self.assertAlmostEqual(ev("2^0.5"), 1.41421356, places=7)

    def test_zero_to_the_zero_is_one(self):
        self.assertEqual(ev("0^0"), 1)

    def test_constants(self):
        self.assertAlmostEqual(ev("2*pi"), 6.283185307, places=8)
        self.assertAlmostEqual(ev("e"), 2.718281828, places=8)

    def test_uppercase_names_work(self):
        self.assertEqual(ev("SQRT(16)"), 4)
        self.assertAlmostEqual(ev("PI"), 3.14159265, places=7)


class ErrorTests(unittest.TestCase):
    def test_division_by_zero(self):
        with self.assertRaises(EvalError):
            ev("1/0")

    def test_modulo_by_zero(self):
        with self.assertRaises(EvalError):
            ev("5%0")

    def test_zero_to_negative_power(self):
        with self.assertRaises(EvalError):
            ev("0^-1")

    def test_negative_base_fractional_power(self):
        with self.assertRaises(EvalError):
            ev("(-8)^(1/3)")

    def test_exponent_too_large(self):
        with self.assertRaises(EvalError):
            ev("2^100000")
        self.assertEqual(ev("1^100000"), 1)

    def test_unknown_variable(self):
        with self.assertRaises(EvalError):
            ev("x+1")

    def test_unknown_function(self):
        with self.assertRaises(EvalError):
            ev("foo(1)")

    def test_too_few_arguments(self):
        for expr in ("sqrt()", "max()", "gcd(4)"):
            with self.subTest(expr=expr):
                with self.assertRaises(EvalError):
                    ev(expr)

    def test_too_many_arguments(self):
        for expr in ("sqrt(1,2)", "fact(1,2)", "round(1,2,3)", "gcd(1,2,3)"):
            with self.subTest(expr=expr):
                with self.assertRaises(EvalError):
                    ev(expr)


class EnvironmentTests(unittest.TestCase):
    def test_assign_and_lookup(self):
        env = Environment()
        env.assign("x", 5)
        self.assertEqual(ev("x*2", env), 10)

    def test_cannot_assign_to_constant_or_function(self):
        env = Environment()
        for name in ("pi", "e", "sqrt"):
            with self.subTest(name=name):
                with self.assertRaises(EvalError):
                    env.assign(name, 1)

    def test_angle_mode_validation(self):
        env = Environment()
        self.assertEqual(env.angle_mode, "rad")
        env.set_angle_mode("deg")
        self.assertEqual(env.angle_mode, "deg")
        with self.assertRaises(EvalError):
            env.set_angle_mode("grad")

    def test_deg_env_helper(self):
        self.assertEqual(deg_env().angle_mode, "deg")


if __name__ == "__main__":
    unittest.main()
