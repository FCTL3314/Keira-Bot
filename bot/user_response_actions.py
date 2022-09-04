import telegram.ext
import translators
import bot
import configurations.settings


def get_user_answer(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Gets the user's response to the given word from get_random_word function"""
    text = update.message.text  # Ответ пользователя на предоставленное ему слово
    word = context.user_data["learning_words"][context.user_data["ran_num"]]  # Достаёт сгенерированное слово из
    # функции random_num при помощи индекса context.user_data["ran_num"]
    get_translated_word(update=update, context=context, text=text, word=word)


def get_translated_word(update: telegram.Update, context: telegram.ext.CallbackContext, text, word):
    """Translates the word variable derived from the get_user_answer"""
    translated_word = translators.google(query_text=word,
                                         from_language=configurations.settings.FROM_LANGUAGE,
                                         to_language=configurations.settings.TO_LANGUAGE
                                         )  # переведённая переменная word
    check_answer_correctness(update=update, context=context, text=text, translated_word=translated_word)


def check_answer_correctness(update: telegram.Update, context: telegram.ext.CallbackContext, text, translated_word):
    """Checks the translated word entered by the user for correctness"""
    if text.lower() == translated_word.lower():
        update.message.reply_text(text='Правильно!')
        bot.get_random_word(update=update, context=context)  # Вызов функции random_word
        # для зацикливания.
    else:
        update.message.reply_text(text=f'Ошибка.\nПравильный вариант - {translated_word}')
        bot.get_random_word(update=update, context=context)  # Вызов функции random_word
        # для зацикливания.
