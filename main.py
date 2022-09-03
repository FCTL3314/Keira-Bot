import telegram
import telegram.ext
from configurations.settings import TOKEN


def start_command(update: telegram.Update, context: telegram.ext.CallbackContext):
    if update.message.text == '/tota':
        update.message.reply_text(text='tota')
    update.message.reply_text(text='Привет, меня зовут Keira-Bot.\n'
                                   'Сперва тебе нужно добавить 3 новых слова.\n'
                                   'Пример: \'/add Apple Coffee Milk\'')


def add_command(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.user_data['learning_words'] = update.message.text[4:].split()
    if len(context.user_data['learning_words']) == 3:
        update.message.reply_text(text=f'Слова записаны, теперь напиши перевод этого'
                                       f' слова: {context.user_data["learning_words"][0]}')
    else:
        print(len(context.user_data['learning_words']))
        update.message.reply_text(text='Ой, что-то пошло не так.\n'
                                       'Вы точно написали 3 слова ?.')


def main():
    print('*START*')
    updater = telegram.ext.Updater(
        token=TOKEN,
        use_context=True
    )
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.CommandHandler(command='start', callback=start_command))
    dp.add_handler(telegram.ext.CommandHandler(command='add', callback=add_command))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
