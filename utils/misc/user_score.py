import data
import utils


class UserScore:
    def __init__(self):
        self._score = 0

    def get_score(self):
        return self._score

    def increment(self):
        self._score += 1

    def decrement(self):
        self._score -= 1

    def reset(self):
        self._score = 0


async def create_score_instance(user_id):
    """"Creates a score instance for the specific user based on its id."""
    data.user_data[f'user_score: {user_id}'] = utils.misc.user_score.UserScore()
