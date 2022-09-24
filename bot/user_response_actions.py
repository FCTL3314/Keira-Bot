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
        bot.score.increment()
        if bot.score.get_score() == 5:
            update.message.reply_text(text=f'🟢Верно 5 раз подряд!\nПродолжай в том же духе!')
            bot.get_random_word(update=update, context=context)
        elif bot.score.get_score() == 10:
            update.message.reply_text(text=f'🟢Верно 10 раз подряд!\nОтлично!')
            bot.get_random_word(update=update, context=context)
        elif bot.score.get_score() > 10:
            update.message.reply_text(text=f'🟢Верно!\nСерия верных ответов: {bot.score.get_score()}!')
            bot.get_random_word(update=update, context=context)
        else:
            update.message.reply_text(text=f'🟢Верно!')
            bot.get_random_word(update=update, context=context)
    else:
        bot.score.reset()
        update.message.reply_text(text=f'🔴Неверно.\nПравильный вариант - {translated_word}')
        bot.get_random_word(update=update, context=context)
