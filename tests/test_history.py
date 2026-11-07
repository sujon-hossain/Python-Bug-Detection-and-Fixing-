import os
import tempfile
import unittest

from calculator.history import History


def filled(n, max_size=50):
    h = History(max_size)
    for i in range(1, n + 1):
        h.add(f"{i}+{i}", i * 2)
    return h


class HistoryTests(unittest.TestCase):
    def test_add_len_last(self):
        h = History()
        self.assertEqual(len(h), 0)
        self.assertIsNone(h.last())
        h.add("1+1", 2)
        self.assertEqual(len(h), 1)
        self.assertEqual(h.last().expression, "1+1")
        self.assertEqual(h.last().result, 2)

    def test_capacity_is_respected(self):
        h = filled(5, max_size=3)
        self.assertEqual(len(h), 3)
        self.assertEqual([e.expression for e in h.recent(10)], ["3+3", "4+4", "5+5"])

    def test_invalid_size(self):
        with self.assertRaises(ValueError):
            History(0)

    def test_recent(self):
        h = filled(5)
        self.assertEqual([e.expression for e in h.recent(2)], ["4+4", "5+5"])
        self.assertEqual(len(h.recent(100)), 5)

    def test_recent_zero_and_negative(self):
        h = filled(3)
        self.assertEqual(h.recent(0), [])
        self.assertEqual(h.recent(-1), [])

    def test_find_is_case_insensitive(self):
        h = History()
        h.add("sqrt(4)", 2)
        h.add("1+1", 2)
        self.assertEqual([e.expression for e in h.find("SQRT")], ["sqrt(4)"])
        self.assertEqual(len(h.find("zzz")), 0)

    def test_clear(self):
        h = filled(3)
        h.clear()
        self.assertEqual(len(h), 0)

    def test_save_and_load_roundtrip(self):
        h = filled(4)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "h.json")
            h.save(path)
            loaded = History.load(path)
        self.assertEqual([(e.expression, e.result) for e in loaded.recent(10)],
                         [(e.expression, e.result) for e in h.recent(10)])

    def test_load_respects_max_size_keeping_newest(self):
        h = filled(5)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "h.json")
            h.save(path)
            loaded = History.load(path, max_size=2)
        self.assertEqual([e.expression for e in loaded.recent(10)], ["4+4", "5+5"])


if __name__ == "__main__":
    unittest.main()
