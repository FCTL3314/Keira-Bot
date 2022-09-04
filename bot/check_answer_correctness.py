import telegram.ext
import translators
import bot


def check_answer_correctness(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Checks if the translated word is correct"""
    text = update.message.text
    word = context.user_data["learning_words"][context.user_data["ran_num"]]  # Слово, которое было сгенерировано
    # в def random_word при помощи context.user_data["ran_num"]
    translated_word = translators.google(query_text=word, from_language='en', to_language='ru')  # word(Переведённый)
    if text.lower() == translated_word.lower():
        update.message.reply_text(text='Правильно! :3')
        bot.random_word(update=update, context=context)  # Вызов функции random_word для зацикливания.
    else:
        update.message.reply_text(text=f'Ошибка.\nПравильный вариант - {translated_word}')
        bot.random_word(update=update, context=context)  # Вызов функции random_word для зацикливания.
