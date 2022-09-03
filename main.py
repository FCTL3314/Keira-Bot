from configurations.settings import TOKEN
import telegram
import telegram.ext
import translators


def start_command(update: telegram.Update, context: telegram.ext.CallbackContext):
    """When executing the command '/start' greets the user"""
    update.message.reply_text(text=f'Привет, меня зовут {update.message.bot.first_name}.\n'
                                   'Сперва тебе нужно добавить 3 новых слова.\n'
                                   'Пример: \'/add Apple Coffee Milk\'')


def add_command(update: telegram.Update, context: telegram.ext.CallbackContext):
    """
    When executing the command '/add '3 words' adds the words after the command to contex.user_data
    as 'learning_words'
    """
    context.user_data['learning_words'] = update.message.text[4:].split()
    if len(context.user_data['learning_words']) == 3:
        update.message.reply_text(text=f'Слова приняты!')
        update.message.reply_text(text='Далее тебе нужно писать перевод слов, которые будут появляться.')
        update.message.reply_text(text=f'{context.user_data["learning_words"][0]}')
    else:
        print(len(context.user_data['learning_words']))
        update.message.reply_text(text='Ой, что-то пошло не так.\n'
                                       'Вы точно написали 3 слова ?.')


def check_answer_correctness(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Checks if the translated word is correct"""
    text = update.message.text
    word = context.user_data["learning_words"][0]
    translated_word = translators.google(query_text=word, from_language='en', to_language='ru')
    if text.lower() == translated_word.lower():
        update.message.reply_text(text='Правильно!')
    else:
        update.message.reply_text(text=f'Ошибка :3\nПравильный вариант - {translated_word}')


def main():
    print('*START*')
    updater = telegram.ext.Updater(
        token=TOKEN,
        use_context=True
    )
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.CommandHandler(command='start', callback=start_command))
    dp.add_handler(telegram.ext.CommandHandler(command='add', callback=add_command))
    dp.add_handler(telegram.ext.MessageHandler(filters=telegram.ext.Filters.text, callback=check_answer_correctness))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
