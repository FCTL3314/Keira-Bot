class Score:
    def __init__(self):
        self._score = 0

    def increment(self):
        self._score += 1

    def reset(self):
        self._score = 0

    def get_score(self):
        return self._score
