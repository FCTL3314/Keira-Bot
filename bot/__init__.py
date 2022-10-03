from .generate_next_random_word import generate_random_word
from .create_keyboard_markup import create_keyboard_markup
from .user_score import UserScore
from .db_actions import db_write_last_learning_words, db_get_last_learning_words

GET_ENTERED_WORDS, TRANSLATE_ENTERED_WORDS = range(2)
