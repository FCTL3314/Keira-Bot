import psycopg2

from typing import List
from data.config import PG_HOST, PG_DBNAME, PG_USER, PG_PASSWORD, PG_PORT


class PostgresDatabase:
    def __init__(self):
        self.__conn = psycopg2.connect(
            host=PG_HOST,
            dbname=PG_DBNAME,
            user=PG_USER,
            password=PG_PASSWORD,
            port=PG_PORT
        )
        self.__cur = self.__conn.cursor()
        self.connected = True

    def __enter__(self):
        if not self.connected:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connected:
            self.__cur.close()
            if isinstance(exc_val, Exception):
                self.__conn.rollback()
            else:
                self.__conn.commit()
            self.__conn.close()
            self.connected = False

    def connect(self):
        self.__conn = psycopg2.connect(
            host=PG_HOST,
            dbname=PG_DBNAME,
            user=PG_USER,
            password=PG_PASSWORD,
            port=PG_PORT
        )
        self.__cur = self.__conn.cursor()
        self.connected = True

    def create_table(self):
        self.__cur.execute("""
        CREATE TABLE IF NOT EXISTS public.user_data (
        user_id BIGINT,
        learned_words text,
        scrabble_medal boolean DEFAULT FALSE,
        PRIMARY KEY (user_id))""")

    def find_user_id_record(self, user_id: int) -> bool:
        self.__cur.execute(f'SELECT user_id FROM user_data WHERE user_id = {user_id}')
        return bool(self.__cur.fetchone())

    def create_user_id_record(self, user_id: int):
        self.__cur.execute(f'INSERT INTO user_data (user_id) VALUES ({user_id})')

    def add_learned_words(self, learned_words: List[str], user_id: int):
        if not self.find_user_id_record(user_id=user_id):
            self.create_user_id_record(user_id=user_id)
        if self.get_learned_words(user_id=user_id) is None:
            self.__cur.execute(
                f"UPDATE user_data SET learned_words = '{' '.join(set(learned_words))}' WHERE user_id = {user_id}")
        else:
            learned_words_set = set(self.get_learned_words(user_id=user_id) + learned_words)
            self.__cur.execute(
                f"UPDATE user_data SET learned_words = '{' '.join(learned_words_set)}' WHERE user_id = {user_id}")

    def get_learned_words(self, user_id: int) -> List[str]:
        if not self.find_user_id_record(user_id=user_id):
            self.create_user_id_record(user_id=user_id)
        self.__cur.execute(f'SELECT learned_words FROM user_data WHERE user_id = {user_id}')
        if self.__cur.fetchone()[0] is not None:
            self.__cur.execute(
                f"SELECT learned_words FROM user_data WHERE user_id = {user_id}")
            return self.__cur.fetchone()[0].split()

    def set_scrabble_medal(self, value, user_id: int):
        if not self.find_user_id_record(user_id=user_id):
            self.create_user_id_record(user_id=user_id)
        self.__cur.execute(f"UPDATE user_data SET scrabble_medal = {value} WHERE user_id = {user_id}")

    def get_scrabble_medal(self, user_id: int) -> bool:
        if not self.find_user_id_record(user_id=user_id):
            self.create_user_id_record(user_id=user_id)
        self.__cur.execute(f"SELECT scrabble_medal FROM user_data WHERE user_id = {user_id}")
        return self.__cur.fetchone()[0]
