import unittest

from calculator import Calculator
from calculator.cli import process_line


class CliTests(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def run_line(self, line):
        return process_line(self.calc, line)

    def test_expressions(self):
        self.assertEqual(self.run_line("2+2"), "4")
        self.assertEqual(self.run_line("10/4"), "2.5")

    def test_errors_are_reported_not_raised(self):
        self.assertEqual(self.run_line("1/0"), "Error: Division by zero")
        self.assertTrue(self.run_line("2 +").startswith("Error:"))
        self.assertTrue(self.run_line("foo bar").startswith("Error:"))

    def test_blank_and_quit(self):
        self.assertEqual(self.run_line("   "), "")
        self.assertIsNone(self.run_line("quit"))
        self.assertIsNone(self.run_line("EXIT"))

    def test_help(self):
        self.assertIn("convert", self.run_line("help"))

    def test_assignment_lines_are_never_commands(self):
        self.assertEqual(self.run_line("mode = 5"), "5")
        self.assertEqual(self.run_line("x = 3"), "3")
        self.assertEqual(self.run_line("x*2"), "6")

    def test_history_numbering(self):
        self.run_line("1+1")
        self.run_line("2*3")
        self.assertEqual(self.run_line("history"), "1. 1+1 = 2\n2. 2*3 = 6")
        self.assertEqual(self.run_line("history 1"), "1. 2*3 = 6")

    def test_history_empty_and_clear(self):
        self.assertEqual(self.run_line("history"), "History is empty.")
        self.run_line("1+1")
        self.assertEqual(self.run_line("clear"), "History cleared.")
        self.assertEqual(len(self.calc.history), 0)

    def test_history_bad_argument(self):
        self.assertTrue(self.run_line("history abc").startswith("Error:"))

    def test_mode(self):
        self.assertEqual(self.run_line("mode"), "Angle mode: rad")
        self.assertEqual(self.run_line("mode deg"), "Angle mode: deg")
        self.assertEqual(self.run_line("sin(90)"), "1")
        self.assertEqual(self.run_line("mode RAD"), "Angle mode: rad")
        self.assertTrue(self.run_line("mode foo").startswith("Error:"))

    def test_convert(self):
        self.assertEqual(self.run_line("convert 1 km m"), "1 km = 1000 m")
        self.assertEqual(self.run_line("convert 100 c f"), "100 c = 212 f")
        self.assertEqual(self.run_line("convert 2.5 h min"), "2.5 h = 150 min")

    def test_convert_errors(self):
        self.assertTrue(self.run_line("convert x km m").startswith("Error:"))
        self.assertTrue(self.run_line("convert 1 km").startswith("Error:"))
        self.assertTrue(self.run_line("convert 1 km kg").startswith("Error:"))

    def test_stats(self):
        self.assertEqual(
            self.run_line("stats 1 2 3 4"),
            "count: 4\nmean: 2.5\nmedian: 2.5\nmode: none\nstdev: 1.118033989",
        )
        self.assertIn("mode: 2", self.run_line("stats 1 2 2 3"))
        self.assertTrue(self.run_line("stats").startswith("Error:"))
        self.assertTrue(self.run_line("stats 1 x").startswith("Error:"))

    def test_base_commands(self):
        self.assertEqual(self.run_line("bin 10"), "0b1010")
        self.assertEqual(self.run_line("oct 8"), "0o10")
        self.assertEqual(self.run_line("hex 255"), "0xff")
        self.assertEqual(self.run_line("hex 15+240"), "0xff")

    def test_negative_base_output(self):
        self.assertEqual(self.run_line("hex -255"), "-0xff")
        self.assertEqual(self.run_line("bin -5"), "-0b101")

    def test_base_command_errors(self):
        self.assertTrue(self.run_line("hex 2.5").startswith("Error:"))
        self.assertTrue(self.run_line("hex").startswith("Error:"))

    def test_frombase(self):
        self.assertEqual(self.run_line("frombase ff 16"), "255")
        self.assertEqual(self.run_line("frombase 1010 2"), "10")
        self.assertTrue(self.run_line("frombase 12 2").startswith("Error:"))
        self.assertTrue(self.run_line("frombase ff").startswith("Error:"))
        self.assertTrue(self.run_line("frombase ff x").startswith("Error:"))

    def test_memory_commands(self):
        self.assertEqual(self.run_line("mr"), "M = 0")
        self.assertEqual(self.run_line("m+ 5"), "M = 5")
        self.assertEqual(self.run_line("m+ 3"), "M = 8")
        self.assertEqual(self.run_line("m- 2"), "M = 6")
        self.assertEqual(self.run_line("mr"), "M = 6")
        self.assertEqual(self.run_line("ms 9"), "M = 9")
        self.assertEqual(self.run_line("mc"), "M = 0")

    def test_memory_uses_last_answer_by_default(self):
        self.assertTrue(self.run_line("m+").startswith("Error:"))
        self.run_line("2+2")
        self.assertEqual(self.run_line("m+"), "M = 4")
        self.assertEqual(self.run_line("m-"), "M = 0")


if __name__ == "__main__":
    unittest.main()
