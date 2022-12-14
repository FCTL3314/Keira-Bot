class UserCounter:
    def __init__(self):
        self._score = 0

    def get_score(self):
        return self._score

    def increment(self):
        self._score += 1

    def decrement(self):
        if self._score > 0:
            self._score -= 1

    def reset(self):
        self._score = 0
