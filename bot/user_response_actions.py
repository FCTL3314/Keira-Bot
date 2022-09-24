import telegram.ext
import bot


def get_translated_word(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Gets the translated word from context.user_data['learning_words_translated']"""
    translated_word = context.user_data['learning_words_translated'][
        context.bot_data[f'ran_num - {update.message.chat_id}']]
    check_answer_correctness(update=update, context=context, translated_word=translated_word)


def check_answer_correctness(update: telegram.Update, context: telegram.ext.CallbackContext, translated_word):
    """Checks the translated word entered by the user for correctness"""
    answer = update.message.text
    if answer.lower() == translated_word.lower():
        update.message.reply_text(text='🟢Верно!')
        bot.get_random_word(update=update, context=context)
    else:
        update.message.reply_text(text=f'🔴Неверно.\nПравильный вариант - {translated_word}')
        bot.get_random_word(update=update, context=context)
