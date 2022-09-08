import telegram.ext
import bot


def get_translated_word(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Gets the translated word from context.user_data['learning_words_translated']"""
    translated_word = context.user_data['learning_words_translated'][context.bot_data["ran_num"]]  # Достает
    # переведенное слово из context.user_data['learning_words_translated'].
    check_answer_correctness(update=update, context=context, translated_word=translated_word)


def check_answer_correctness(update: telegram.Update, context: telegram.ext.CallbackContext, translated_word):
    """Checks the translated word entered by the user for correctness"""
    answer = update.message.text
    if answer.lower() == translated_word.lower():
        update.message.reply_text(text='Правильно!')
        bot.get_random_word(update=update, context=context)  # Вызов функции random_word для зацикливания.
    else:
        update.message.reply_text(text=f'Ошибка.\nПравильный вариант - {translated_word}')
        bot.get_random_word(update=update, context=context)  # Вызов функции random_word для зацикливания.
