import sqlite3

from typing import List


class Database:
    """The class is designed for the fact that its methods will be called with a context manager."""
    __LOCATION = r'D:\Start Menu\Programming\Keira-Bot\utils\sql\data\data.db'

    def __init__(self, specific_location=None):
        """
        Attributes __conn and __cur are not initialized immediately in __init__ because it will create an instant
        connection right after the class is instantiated. To correctly determine these attributes, there is a connect
        function, which is called in the __enter__ method.
        """
        self.__conn = None
        self.__cur = None
        self.__specific_location = specific_location
        self.connected = False

    def __enter__(self):
        if not self.connected:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cur.close()
        if isinstance(exc_val, Exception):  # Наследуется ли exc_val (значение исключения(если оно будет)) от Exception
            self.__conn.rollback()
        else:
            self.__conn.commit()
        self.__conn.close()
        self.connected = False

    def connect(self):
        if self.__specific_location is not None:
            self.__conn = sqlite3.connect(self.__specific_location, check_same_thread=False)
        else:
            self.__conn = self.__conn = sqlite3.connect(self.__LOCATION, check_same_thread=False)
        self.__cur = self.__conn.cursor()
        self.connected = True

    def create_table(self):
        self.__cur.execute("CREATE TABLE IF NOT EXISTS 'user_data' ('user_id' INTEGER UNIQUE, "
                           "'learned_words' TEXT, 'best_score'	INTEGER DEFAULT 0, PRIMARY KEY('user_id'))")

    def find_user_id_record(self, user_id: int) -> bool:
        self.__cur.execute(f'SELECT user_id FROM user_data WHERE user_id == "{user_id}"')
        return bool(self.__cur.fetchone())

    def create_user_record(self, user_id: int):
        self.__cur.execute(f'INSERT INTO user_data (user_id) VALUES ({user_id})')

    def add_learned_words(self, learned_words: List[str], user_id: int):
        if not self.find_user_id_record(user_id=user_id):
            self.create_user_record(user_id=user_id)
        self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {user_id}')
        if self.__cur.fetchone()[0] is None:
            self.__cur.execute(f'UPDATE user_data SET learned_words = '
                               f'"{" ".join(learned_words)}" WHERE user_id = {user_id}')
        self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {user_id}')
        learned_words_set = set(self.__cur.fetchone()[0].split() + learned_words)
        self.__cur.execute(f'UPDATE user_data SET learned_words = '
                           f'"{" ".join(learned_words_set)}" WHERE user_id = {user_id}')

    def update_best_score(self, score: int, user_id: int):
        if not self.find_user_id_record(user_id=user_id):
            self.create_user_record(user_id=user_id)
        self.__cur.execute(
            f'UPDATE user_data SET best_score = {score} WHERE user_id == {user_id}')

    def get_learned_words(self, user_id: int) -> List[str]:
        if not self.find_user_id_record(user_id=user_id):
            self.create_user_record(user_id=user_id)
        self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {user_id}')
        if self.__cur.fetchone()[0] is not None:
            self.__cur.execute(
                f'SELECT learned_words FROM user_data WHERE user_id == {user_id}')
            return self.__cur.fetchone()[0].split()

    def get_best_score(self, user_id: int) -> int:
        if not self.find_user_id_record(user_id=user_id):
            self.create_user_record(user_id=user_id)
        self.__cur.execute(f'SELECT best_score FROM user_data WHERE user_id == {user_id}')
        return self.__cur.fetchone()[0]
