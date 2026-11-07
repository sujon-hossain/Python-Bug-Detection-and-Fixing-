"""Remember past calculations and save/load them as JSON."""
import json
from collections import deque
from dataclasses import dataclass


@dataclass
class Entry:
    expression: str
    result: object


class History:
    def __init__(self, max_size=50):
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        self.max_size = max_size
        self._entries = deque(maxlen=max_size + 1)

    def add(self, expression, result):
        self._entries.append(Entry(expression, result))

    def __len__(self):
        return len(self._entries)

    def last(self):
        return self._entries[-1] if self._entries else None

    def recent(self, n=10):
        return list(self._entries)[-n:]

    def find(self, term):
        return [e for e in self._entries if term in e.expression]

    def clear(self):
        self._entries.clear()

    def save(self, path):
        data = [{"expression": e.expression, "result": e.result} for e in self._entries]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    @classmethod
    def load(cls, path, max_size=50):
        history = cls(max_size)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for item in reversed(data):
            history.add(item["expression"], item["result"])
        return history
