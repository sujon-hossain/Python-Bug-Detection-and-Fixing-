"""The M+ / M- / MR / MC memory register."""


class Memory:
    def __init__(self):
        self._value = 0

    def store(self, value):
        self._value = value

    def add(self, value):
        self._value += value

    def subtract(self, value):
        self._value = value - self._value

    def recall(self):
        return self._value

    def clear(self):
        pass
