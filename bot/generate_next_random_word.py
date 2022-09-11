import telegram.ext
import random

import bot.create_keyboard_markup
import configurations.settings


def get_random_word(update: telegram.Update, context: telegram.ext.CallbackContext):
    """
    Generates a random word from 'context.user_data['learning_words']'
    and writes it to context.user_data['ran_num']
    """
    context.bot_data['ran_num'] = random.randint(0, (configurations.settings.NUMBER_OF_WORDS - 1))  # Записывает число
    # от 0 до (NUMBER_OF_WORDS - 1) в context.bot_data['ran_num']
    update.message.reply_text(text=f'{context.user_data["learning_words"][context.bot_data["ran_num"]]}',
                              reply_markup=bot.create_keyboard_markup(context=context))  # Отправляет сообщение со
    # случайно выбранным словом и вызывает клавиатуру для ответа.
