import telegram.ext
import bot


def add_learning_words(update: telegram.Update, context: telegram.ext.CallbackContext):
    """
    When executing the command '/add "3 words"' adds the words after the '/add ' to contex.user_data
    as 'learning_words'
    """
    context.user_data['learning_words'] = update.message.text[4:].split()  # Создаёт
    # context.user_data['learning_words'].split() без /add
    if len(context.user_data['learning_words']) == 3:  # Проверяет кол-во введённых слов(Требуется 3)
        update.message.reply_text(text=f'Слова приняты!')
        update.message.reply_text(text='Далее тебе нужно вводить перевод слов, которые будут появляться.')
        bot.random_word(update=update, context=context)  # Вызов функции random_word для генерации случайного
        # слова из context.user_data['learning_words']
    else:
        update.message.reply_text(text='Ой, что-то пошло не так.\n'
                                       f'Кол-во ваших слов: {len(context.user_data["learning_words"])}.')
