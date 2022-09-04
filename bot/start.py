import telegram.ext


def start_command(update: telegram.Update, context: telegram.ext.CallbackContext):
    """When executing the command '/start' greets the user"""
    update.message.reply_text(text=f'Привет, меня зовут {update.message.bot.first_name}.\n'
                                   'Сперва тебе нужно добавить 3 новых слова.\n'
                                   'Пример: \'/add Apple Coffee Milk\'')
    update.message.reply_text(text='Пока я не настроил бота достаточно хорошо, ты сам контролируешь '
                                   'правильность написанных тобою слов.')
