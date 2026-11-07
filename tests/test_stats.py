import unittest

from calculator import stats
from calculator.errors import EvalError


class StatsTests(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(stats.mean([1, 2, 3, 4]), 2.5)

    def test_median_odd_even_unsorted(self):
        self.assertEqual(stats.median([3, 1, 2]), 2)
        self.assertEqual(stats.median([1, 2, 3, 4]), 2.5)
        self.assertEqual(stats.median([1, 2]), 1.5)
        self.assertEqual(stats.median([9, 1, 5, 3]), 4)
        self.assertEqual(stats.median([7]), 7)

    def test_mode(self):
        self.assertEqual(stats.mode([1, 2, 2, 3]), [2])
        self.assertEqual(stats.mode([1, 1, 2, 2, 3]), [1, 2])

    def test_mode_with_no_repeats(self):
        self.assertEqual(stats.mode([1, 2, 3]), [])
        self.assertEqual(stats.mode([5]), [])

    def test_population_variance_and_stdev(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        self.assertEqual(stats.variance(data), 4)
        self.assertEqual(stats.stdev(data), 2)

    def test_sample_variance(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        self.assertAlmostEqual(stats.variance(data, sample=True), 32 / 7, places=9)
        self.assertAlmostEqual(stats.stdev(data, sample=True), (32 / 7) ** 0.5, places=9)

    def test_sample_variance_needs_two_values(self):
        with self.assertRaises(EvalError):
            stats.variance([1], sample=True)
        self.assertEqual(stats.variance([1]), 0)

    def test_empty_data(self):
        for fn in (stats.mean, stats.median, stats.mode, stats.variance, stats.stdev):
            with self.subTest(fn=fn.__name__):
                with self.assertRaises(EvalError):
                    fn([])


if __name__ == "__main__":
    unittest.main()
