import aiogram
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
        self._connected = True

    def __enter__(self):
        if not self._connected:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connected:
            self.__cur.close()
            if isinstance(exc_val, Exception):
                self.__conn.rollback()
            else:
                self.__conn.commit()
            self.__conn.close()
            self._connected = False

    def connect(self):
        self.__conn = psycopg2.connect(
            host=PG_HOST,
            dbname=PG_DBNAME,
            user=PG_USER,
            password=PG_PASSWORD,
            port=PG_PORT
        )
        self.__cur = self.__conn.cursor()
        self._connected = True

    async def create_tables(self):
        self.__cur.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
        user_id BIGINT PRIMARY KEY,
        user_name varchar(32));
        
        CREATE TABLE IF NOT EXISTS learned_words (
        user_id bigint REFERENCES user_data(user_id) ON DELETE CASCADE,
        word varchar(32));
        
        CREATE TABLE IF NOT EXISTS achievements (
        user_id bigint REFERENCES user_data(user_id) ON DELETE CASCADE,
        scrabble_achievement bool DEFAULT FALSE,
        pioneer_achievement bool DEFAULT FALSE)
        """)

    async def is_user_exist(self, message: aiogram.types.Message) -> bool:
        user_id = message.from_user.id
        self.__cur.execute(f"""SELECT user_id FROM user_data WHERE user_id = {user_id}""")
        return bool(self.__cur.fetchone())

    async def create_user_rows(self, message: aiogram.types.Message):
        user_id = message.from_user.id
        user_name = message.from_user.username
        if user_name:
            self.__cur.execute(f"""
            INSERT INTO user_data (user_id, user_name) VALUES ({user_id}, '{user_name}');
            INSERT INTO achievements (user_id) VALUES ({user_id})
            """)
        else:
            self.__cur.execute(f"""
            INSERT INTO user_data (user_id) VALUES ({user_id});
            INSERT INTO achievements (user_id) VALUES ({user_id})
            """)

    async def add_learned_words(self, words: List[str], message: aiogram.types.Message):
        user_id = message.from_user.id
        if not await self.is_user_exist(message=message):
            await self.create_user_rows(message=message)
        learned_words = await self.get_learned_words(message=message)
        for word in words:
            if not learned_words or word not in learned_words:
                self.__cur.execute(f"""INSERT INTO learned_words (user_id, word) VALUES ({user_id}, '{word}')""")

    async def get_learned_words(self, message: aiogram.types.Message) -> List[str]:
        user_id = message.from_user.id
        if not await self.is_user_exist(message=message):
            await self.create_user_rows(message=message)
        self.__cur.execute(f"""SELECT word FROM learned_words WHERE user_id = {user_id}""")
        words_tuple = self.__cur.fetchall()
        if words_tuple:
            result = [word[0] for word in words_tuple]
            return result

    async def set_achievement(self, message: aiogram.types.Message, achievement: str, value=True):
        user_id = message.from_user.id
        if not await self.is_user_exist(message=message):
            await self.create_user_rows(message=message)
        self.__cur.execute(f"""UPDATE achievements SET {achievement} = {value} WHERE user_id = {user_id}""")

    async def get_achievement(self, achievement: str, message: aiogram.types.Message) -> bool:
        user_id = message.from_user.id
        if not await self.is_user_exist(message=message):
            await self.create_user_rows(message=message)
        self.__cur.execute(f"""SELECT {achievement} FROM achievements WHERE user_id = {user_id}""")
        return self.__cur.fetchone()[0]
