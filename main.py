from configurations.settings import TOKEN
import telegram
import telegram.ext
import translators
import random


def start_command(update: telegram.Update, context: telegram.ext.CallbackContext):
    """When executing the command '/start' greets the user"""
    update.message.reply_text(text=f'Привет, меня зовут {update.message.bot.first_name}.\n'
                                   'Сперва тебе нужно добавить 3 новых слова.\n'
                                   'Пример: \'/add Apple Coffee Milk\'')
    update.message.reply_text(text='Пока я не настроил бота достаточно хорошо, ты сам контролируешь '
                                   'правильность написанных тобою слов.')


def add_learning_words(update: telegram.Update, context: telegram.ext.CallbackContext):
    """
    When executing the command '/add '3 words' adds the words after the command to contex.user_data
    as 'learning_words'
    """
    context.user_data['learning_words'] = update.message.text[4:].split()  # Создаёт
    # context.user_data['learning_words'].split() без /add
    if len(context.user_data['learning_words']) == 3:  # Проверяет кол-во введённых слов(Требуется 3)
        update.message.reply_text(text=f'Слова приняты!')
        update.message.reply_text(text='Далее тебе нужно вводить перевод слов, которые будут появляться.')
        random_word(update=update, context=context)  # Вызов функции random_word для генерации случайного слова
        # из context.user_data['learning_words']
    else:
        update.message.reply_text(text='Ой, что-то пошло не так.\n'
                                       f'Кол-во ваших слов: {len(context.user_data["learning_words"])}.')


def random_word(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Generates a random word from 'context.user_data['learning_words']'"""
    context.user_data['ran_num'] = random.randint(0, 2)  # Выбирает случайное слово
    # из context.user_data["learning_words"]
    update.message.reply_text(text=f'{context.user_data["learning_words"][context.user_data["ran_num"]]}')
    # Отправляет сообщение со случайно выбранным словом.


def check_answer_correctness(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Checks if the translated word is correct"""
    text = update.message.text
    word = context.user_data["learning_words"][context.user_data["ran_num"]]  # Слово, которое было сгенерировано
    # в def random_word при помощи context.user_data["ran_num"]
    translated_word = translators.google(query_text=word, from_language='en', to_language='ru')  # word(Переведённый)
    if text.lower() == translated_word.lower():
        update.message.reply_text(text='Правильно! :3')
        random_word(update=update, context=context)  # Вызов функции random_word для зацикливания.
    else:
        update.message.reply_text(text=f'Ошибка.\nПравильный вариант - {translated_word}')
        random_word(update=update, context=context)  # Вызов функции random_word для зацикливания.


def main():
    print('*START*')
    updater = telegram.ext.Updater(
        token=TOKEN,
        use_context=True
    )
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.CommandHandler(command='start', callback=start_command))
    dp.add_handler(telegram.ext.CommandHandler(command='add', callback=add_learning_words))
    dp.add_handler(telegram.ext.MessageHandler(filters=telegram.ext.Filters.text, callback=check_answer_correctness))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
