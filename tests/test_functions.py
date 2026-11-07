import math
import unittest

from calculator.errors import EvalError
from tests.helpers import deg_env, ev


class BasicFunctionTests(unittest.TestCase):
    def test_sqrt(self):
        self.assertEqual(ev("sqrt(16)"), 4)
        self.assertAlmostEqual(ev("sqrt(2)"), 1.41421356, places=7)
        with self.assertRaises(EvalError):
            ev("sqrt(-1)")

    def test_abs(self):
        self.assertEqual(ev("abs(-7)"), 7)

    def test_round_half_up(self):
        self.assertEqual(ev("round(2.5)"), 3)
        self.assertEqual(ev("round(0.5)"), 1)
        self.assertEqual(ev("round(-2.5)"), -3)
        self.assertEqual(ev("round(3.14159, 2)"), 3.14)
        self.assertEqual(ev("round(1.005, 2)"), 1.01)
        self.assertEqual(ev("round(1234, -2)"), 1200)

    def test_floor_and_ceil(self):
        self.assertEqual(ev("floor(2.7)"), 2)
        self.assertEqual(ev("floor(-2.5)"), -3)
        self.assertEqual(ev("ceil(2.1)"), 3)
        self.assertEqual(ev("ceil(-2.5)"), -2)

    def test_factorial(self):
        self.assertEqual(ev("fact(0)"), 1)
        self.assertEqual(ev("fact(1)"), 1)
        self.assertEqual(ev("fact(5)"), 120)
        self.assertEqual(ev("fact(10/2)"), 120)

    def test_factorial_errors(self):
        for expr in ("fact(-1)", "fact(2.5)", "fact(171)"):
            with self.subTest(expr=expr):
                with self.assertRaises(EvalError):
                    ev(expr)

    def test_gcd(self):
        self.assertEqual(ev("gcd(12,18)"), 6)
        self.assertEqual(ev("gcd(0,5)"), 5)
        with self.assertRaises(EvalError):
            ev("gcd(1.5, 3)")

    def test_lcm(self):
        self.assertEqual(ev("lcm(4,6)"), 12)
        self.assertEqual(ev("lcm(-4,6)"), 12)
        self.assertEqual(ev("lcm(0,5)"), 0)

    def test_min_max_avg(self):
        self.assertEqual(ev("min(3,1,2)"), 1)
        self.assertEqual(ev("max(3,1,2)"), 3)
        self.assertEqual(ev("avg(1,2,3,4)"), 2.5)
        self.assertEqual(ev("max(7)"), 7)


class LogTests(unittest.TestCase):
    def test_log_base_10_default(self):
        self.assertEqual(ev("log(100)"), 2)
        self.assertEqual(ev("log(1000)"), 3)

    def test_log_with_base(self):
        self.assertEqual(ev("log(8,2)"), 3)
        self.assertEqual(ev("log(81,3)"), 4)

    def test_natural_log_and_exp(self):
        self.assertAlmostEqual(ev("ln(e)"), 1.0, places=10)
        self.assertEqual(ev("exp(0)"), 1)
        self.assertAlmostEqual(ev("exp(1)"), math.e, places=10)

    def test_log_domain_errors(self):
        for expr in ("log(0)", "log(-1)", "ln(0)", "log(2,1)", "log(2,0)"):
            with self.subTest(expr=expr):
                with self.assertRaises(EvalError):
                    ev(expr)

    def test_exp_overflow(self):
        with self.assertRaises(EvalError):
            ev("exp(1000)")


class TrigTests(unittest.TestCase):
    def test_radians_by_default(self):
        self.assertEqual(ev("sin(pi/2)"), 1)
        self.assertEqual(ev("cos(pi)"), -1)
        self.assertEqual(ev("sin(0)"), 0)
        self.assertAlmostEqual(ev("tan(pi/4)"), 1.0, places=10)

    def test_degrees(self):
        env = deg_env()
        self.assertEqual(ev("sin(90)", env), 1)
        self.assertEqual(ev("sin(30)", env), 0.5)
        self.assertEqual(ev("cos(60)", env), 0.5)
        self.assertEqual(ev("tan(45)", env), 1)

    def test_floating_point_dust_is_cleaned(self):
        env = deg_env()
        self.assertEqual(ev("sin(180)", env), 0)
        self.assertEqual(ev("cos(90)", env), 0)

    def test_tan_undefined(self):
        with self.assertRaises(EvalError):
            ev("tan(90)", deg_env())
        with self.assertRaises(EvalError):
            ev("tan(pi/2)")

    def test_inverse_trig_in_degrees(self):
        env = deg_env()
        self.assertAlmostEqual(ev("asin(1)", env), 90, places=6)
        self.assertAlmostEqual(ev("acos(0)", env), 90, places=6)
        self.assertAlmostEqual(ev("atan(1)", env), 45, places=6)

    def test_inverse_trig_in_radians(self):
        self.assertAlmostEqual(ev("asin(1)"), math.pi / 2, places=10)
        self.assertAlmostEqual(ev("atan(1)"), math.pi / 4, places=10)

    def test_inverse_trig_domain(self):
        for expr in ("asin(2)", "acos(-2)"):
            with self.subTest(expr=expr):
                with self.assertRaises(EvalError):
                    ev(expr)


if __name__ == "__main__":
    unittest.main()
