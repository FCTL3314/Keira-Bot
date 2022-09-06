import telegram
import telegram.ext
import bot.get_learning_words
import bot.user_response_actions
import bot.start_command

from configurations.settings import TOKEN


def main():
    print('**START**')
    updater = telegram.ext.Updater(
        token=TOKEN,
        use_context=True
    )
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.CommandHandler(
        command='start',
        callback=bot.start_command.start_command
    )
    )
    dp.add_handler(telegram.ext.ConversationHandler(
        entry_points=[
            telegram.ext.CommandHandler('add', bot.get_learning_words.asks_for_words, pass_user_data=True),
        ],
        states={
            bot.get_learning_words.WORDS: [
                telegram.ext.MessageHandler(
                    filters=telegram.ext.Filters.text & (~ telegram.ext.Filters.command),
                    callback=bot.get_learning_words.get_learning_words,
                    pass_user_data=True),
            ],
            bot.get_learning_words.GET_WORDS: [
                telegram.ext.MessageHandler(
                    filters=telegram.ext.Filters.text & (~ telegram.ext.Filters.command),
                    callback=bot.user_response_actions.get_user_answer,
                    pass_user_data=True),
            ],
        },
        fallbacks=[
            telegram.ext.CommandHandler('stop', bot.get_learning_words.stop_guessing),
        ],
    )
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
