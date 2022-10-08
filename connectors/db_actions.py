import sqlite3
import aiogram

from typing import List


class DataBase:
    def __init__(self, route: str):
        self.__conn = sqlite3.connect(route, check_same_thread=False)
        self.__cur = self.__conn.cursor()

    def find_user_id_record(self, message: aiogram.types.Message) -> bool:
        with self.__conn:
            self.__cur.execute(f'SELECT user_id FROM user_data WHERE user_id == "{message.from_user.id}"')
        return bool(self.__cur.fetchone())

    def create_user_record(self, message: aiogram.types.Message):
        with self.__conn:
            self.__cur.execute(f'INSERT INTO user_data (user_id) VALUES ({message.from_user.id})')

    def add_learned_words(self, learned_words: List[str], message: aiogram.types.Message):
        with self.__conn:
            if not self.find_user_id_record(message=message):
                self.create_user_record(message=message)
            self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {message.from_user.id}')
            if self.__cur.fetchone()[0] is None:
                self.__cur.execute(f'UPDATE user_data SET learned_words = '
                                   f'"{" ".join(learned_words)}" WHERE user_id = {message.from_user.id}')
            self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {message.from_user.id}')
            learned_words_set = set(self.__cur.fetchone()[0].split() + learned_words)
            self.__cur.execute(f'UPDATE user_data SET learned_words = '
                               f'"{" ".join(learned_words_set)}" WHERE user_id = {message.from_user.id}')

    def update_best_score(self, score: int, message: aiogram.types.Message):
        with self.__conn:
            if not self.find_user_id_record(message=message):
                self.create_user_record(message=message)
            self.__cur.execute(
                f'UPDATE user_data SET best_score = {score} WHERE user_id == {message.from_user.id}')

    def get_learned_words(self, message: aiogram.types.Message) -> List[str]:
        with self.__conn:
            if not self.find_user_id_record(message=message):
                self.create_user_record(message=message)
            self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {message.from_user.id}')
            if self.__cur.fetchone()[0] is not None:
                self.__cur.execute(
                    f'SELECT learned_words FROM user_data WHERE user_id == {message.from_user.id}')
                return self.__cur.fetchone()[0].split()

    def get_best_score(self, message: aiogram.types.Message) -> int:
        with self.__conn:
            if not self.find_user_id_record(message=message):
                self.create_user_record(message=message)
            self.__cur.execute(f'SELECT best_score FROM user_data WHERE user_id == {message.from_user.id}')
            return self.__cur.fetchone()[0]


data_base = DataBase(route=r'D:\Start Menu\Programming\Keira-Bot\connectors\data\data.db')
