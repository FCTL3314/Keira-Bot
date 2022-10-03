import sqlite3
import telegram.ext


def db_write_last_learning_words(learning_words, update: telegram.Update):
    with sqlite3.connect('sqlite:///../data/data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT user_id FROM user_data WHERE user_id = "{update.message.from_user.id}"')
        if cur.fetchone() is None:
            cur.execute(f'INSERT INTO user_data (user_id, last_learning_words)'
                        f' VALUES ({update.message.from_user.id}, "{" ".join(learning_words)}")')
        else:
            cur.execute(f'UPDATE user_data SET last_learning_words = "{" ".join(learning_words)}" '
                        f'WHERE user_id = {update.message.from_user.id}')


def db_get_last_learning_words(update: telegram.Update):
    with sqlite3.connect('sqlite:///../data/data.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT last_learning_words FROM user_data WHERE user_id = "{update.message.from_user.id}"')
        return ''.join(cur.fetchone()).split()
