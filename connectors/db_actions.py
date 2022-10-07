import sqlite3
import telegram.ext

from typing import List


class DataBase:
    def __init__(self, route: str):
        self.__conn = sqlite3.connect(route, check_same_thread=False)
        self.__cur = self.__conn.cursor()

    def find_user_id_record(self, update: telegram.Update) -> bool:
        self.__cur.execute(f'SELECT user_id FROM user_data WHERE user_id == "{update.message.from_user.id}"')
        return bool(self.__cur.fetchone())

    def create_user_record(self, update: telegram.Update):
        with self.__conn:
            self.__cur.execute(f'INSERT INTO user_data (user_id) VALUES ({update.message.from_user.id})')

    def add_learned_words(self, learned_words: List[str], update: telegram.Update):
        with self.__conn:
            if not self.find_user_id_record(update=update):
                self.create_user_record(update=update)
            self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {update.message.from_user.id}')
            if self.__cur.fetchone()[0] is None:
                self.__cur.execute(f'UPDATE user_data SET learned_words = '
                                   f'"{" ".join(learned_words)}" WHERE user_id = {update.message.from_user.id}')
            self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {update.message.from_user.id}')
            learned_words_set = set(self.__cur.fetchone()[0].split() + learned_words)
            self.__cur.execute(f'UPDATE user_data SET learned_words = '
                               f'"{" ".join(learned_words_set)}" WHERE user_id = {update.message.from_user.id}')

    def update_best_score(self, score: int, update: telegram.Update):
        with self.__conn:
            if not self.find_user_id_record(update=update):
                self.create_user_record(update=update)
            self.__cur.execute(
                f'UPDATE user_data SET best_score = {score} WHERE user_id == {update.message.from_user.id}')

    def get_learned_words(self, update: telegram.Update) -> List[str]:
        with self.__conn:
            if not self.find_user_id_record(update=update):
                self.create_user_record(update=update)
            self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {update.message.from_user.id}')
            if self.__cur.fetchone()[0] is not None:
                self.__cur.execute(
                    f'SELECT learned_words FROM user_data WHERE user_id == {update.message.from_user.id}')
                return self.__cur.fetchone()[0].split()

    def get_best_score(self, update: telegram.Update) -> int:
        with self.__conn:
            if not self.find_user_id_record(update=update):
                self.create_user_record(update=update)
            self.__cur.execute(f'SELECT best_score FROM user_data WHERE user_id == {update.message.from_user.id}')
            return self.__cur.fetchone()[0]


data_base = DataBase(route=r'D:\Start Menu\Programming\Keira-Bot\connectors\data\data.db')
