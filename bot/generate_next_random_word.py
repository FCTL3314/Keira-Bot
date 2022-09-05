import telegram.ext
import random


def get_random_word(update: telegram.Update, context: telegram.ext.CallbackContext):
    """
    Generates a random word from 'context.user_data['learning_words']'
    and writes it to context.user_data['ran_num']
    """
    context.bot_data['ran_num'] = random.randint(0, 2)  # Записывает число от 0 до 2 в context.bot_data['ran_num']
    update.message.reply_text(text=f'{context.user_data["learning_words"][context.bot_data["ran_num"]]}')
    # Отправляет сообщение со случайно выбранным словом.
