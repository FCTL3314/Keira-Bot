import telegram.ext


def start_command(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Send a message that informs the user"""
    update.message.reply_text(
        text=f'Привет {update.message.from_user.first_name}! Меня зовут {update.message.bot.first_name}.\n'
             f'Я буду помогать тебе изучать иностранные слова.\n'
             f'Сперва напиши команду /add, что бы добавить их.\n'
             f'Язык написанных тобою слов определяется автоматически.',
        disable_notification=True
    )
