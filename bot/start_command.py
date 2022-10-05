import telegram.ext


def start_command(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Send a message that informs the user"""
    update.message.reply_text(
        text=f'Привет {update.message.from_user.first_name}! Меня зовут {update.message.bot.first_name}.',
        disable_notification=True
    )
    update.message.reply_text(text=f'Я буду помогать тебе изучать иностранные слова.\n'
                                   f'Сперва напиши команду /add, что бы добавить их.\n'
                                   f'Язык написанных тобою слов определяется автоматически.',
                              disable_notification=True)
    update.message.reply_text(text=f'Слова, которые ты выучил, добавляются к тебе в библиотеку.\n'
                                   f'Для того что бы выучить слова, тебе необходимо их верно переводить до тех пор,'
                                   f' пока не появится соответствующее сообщение.',
                              disable_notification=True)
    update.message.reply_text(
        text=f'Написав команду /achievements, ты увидишь библиотеку выученных слов, а так же свой лучший счёт.',
        disable_notification=True)
