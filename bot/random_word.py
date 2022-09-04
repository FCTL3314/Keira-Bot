import telegram.ext
import random


def random_word(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Generates a random word from 'context.user_data['learning_words']'"""
    context.user_data['ran_num'] = random.randint(0, 2)  # Выбирает случайное слово
    # из context.user_data["learning_words"]
    update.message.reply_text(text=f'{context.user_data["learning_words"][context.user_data["ran_num"]]}')
    # Отправляет сообщение со случайно выбранным словом.
