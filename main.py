import telegram
import telegram.ext
import bot.add_learning_words
import bot.user_response_actions
import bot.start_command

from configurations.settings import TOKEN


def main():
    print('*START*')
    updater = telegram.ext.Updater(
        token=TOKEN,
        use_context=True
    )
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.CommandHandler(command='start',
                                               callback=bot.start_command.start_command
                                               )
                   )
    dp.add_handler(telegram.ext.CommandHandler(command='add',
                                               callback=bot.add_learning_words.get_learning_words
                                               )
                   )
    dp.add_handler(telegram.ext.MessageHandler(filters=telegram.ext.Filters.text,
                                               callback=bot.user_response_actions.get_user_answer
                                               )
                   )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
