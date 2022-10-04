import sqlite3
import telegram.ext


def db_add_learned_words(learned_words, update: telegram.Update):
    with sqlite3.connect('D:\\Start Menu\\Programming\\Keira-Bot\\connectors\\data\\data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT user_id FROM user_data WHERE user_id == "{update.message.from_user.id}"')
        if cur.fetchone() is None:
            cur.execute(f'INSERT INTO user_data (user_id, learned_words)'
                        f' VALUES ({update.message.from_user.id}, "{" ".join(learned_words)}")')
        else:
            cur.execute(f'UPDATE user_data SET learned_words = "{" ".join(learned_words)}" '
                        f'WHERE user_id = {update.message.from_user.id}')


def db_update_best_score(score, update: telegram.Update):
    with sqlite3.connect('D:\\Start Menu\\Programming\\Keira-Bot\\connectors\\data\\data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT best_score FROM user_data WHERE user_id == "{update.message.from_user.id}"')
        if cur.fetchone()[0] < score:
            cur.execute(f'UPDATE user_data SET best_score = {score} WHERE user_id == "{update.message.from_user.id}"')


def db_get_learned_words(update: telegram.Update):
    with sqlite3.connect('D:\\Start Menu\\Programming\\Keira-Bot\\connectors\\data\\data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT learned_words FROM user_data WHERE user_id == {update.message.from_user.id}')
        return ''.join(cur.fetchone()).split()


def db_get_best_score(update: telegram.Update):
    with sqlite3.connect('D:\\Start Menu\\Programming\\Keira-Bot\\connectors\\data\\data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT best_score FROM user_data WHERE user_id == {update.message.from_user.id}')
        return cur.fetchone()[0]
