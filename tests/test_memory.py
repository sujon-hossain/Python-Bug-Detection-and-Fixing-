import unittest

from calculator.memory import Memory


class MemoryTests(unittest.TestCase):
    def test_starts_at_zero(self):
        self.assertEqual(Memory().recall(), 0)

    def test_store(self):
        m = Memory()
        m.store(42)
        self.assertEqual(m.recall(), 42)

    def test_add(self):
        m = Memory()
        m.store(10)
        m.add(5)
        self.assertEqual(m.recall(), 15)

    def test_subtract(self):
        m = Memory()
        m.store(10)
        m.subtract(3)
        self.assertEqual(m.recall(), 7)

    def test_clear(self):
        m = Memory()
        m.store(99)
        m.clear()
        self.assertEqual(m.recall(), 0)


if __name__ == "__main__":
    unittest.main()
