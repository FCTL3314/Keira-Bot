import sqlite3
import telegram.ext

from typing import List


def db_create_user_info(update: telegram.Update):
    with sqlite3.connect('D:\\Start Menu\\Programming\\Keira-Bot\\connectors\\data\\data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT user_id FROM user_data WHERE user_id == "{update.message.from_user.id}"')
        if cur.fetchone() is None:
            cur.execute(f'INSERT INTO user_data (user_id) VALUES ({update.message.from_user.id})')


def db_add_learned_words(learned_words: List[str], update: telegram.Update):
    with sqlite3.connect('D:\\Start Menu\\Programming\\Keira-Bot\\connectors\\data\\data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {update.message.from_user.id}')
        if cur.fetchone()[0] is None:
            cur.execute(f'UPDATE user_data SET learned_words = '
                        f'"{" ".join(learned_words)}" WHERE user_id = {update.message.from_user.id}')
        else:
            cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {update.message.from_user.id}')
            learned_words_set = set(cur.fetchone()[0].split() + learned_words)
            cur.execute(f'UPDATE user_data SET learned_words = '
                        f'"{" ".join(learned_words_set)}" WHERE user_id = {update.message.from_user.id}')


def db_update_best_score(score: int, update: telegram.Update):
    with sqlite3.connect('D:\\Start Menu\\Programming\\Keira-Bot\\connectors\\data\\data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'UPDATE user_data SET best_score = {score} WHERE user_id == {update.message.from_user.id}')


def db_get_learned_words(update: telegram.Update) -> List[str]:
    with sqlite3.connect('D:\\Start Menu\\Programming\\Keira-Bot\\connectors\\data\\data.db') as conn:
        db_create_user_info(update=update)
        cur = conn.cursor()
        cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {update.message.from_user.id}')
        if cur.fetchone()[0] is not None:
            cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {update.message.from_user.id}')
            return cur.fetchone()[0].split()


def db_get_best_score(update: telegram.Update) -> int:
    with sqlite3.connect('D:\\Start Menu\\Programming\\Keira-Bot\\connectors\\data\\data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT best_score FROM user_data WHERE user_id == {update.message.from_user.id}')
        return cur.fetchone()[0]
