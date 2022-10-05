import telegram.ext


def unexpected_message_reply(update: telegram.Update, context: telegram.ext.CallbackContext):
    update.message.reply_text(text='Моей программой не предусмотрена предоставленная тобою смысловая нагрузка.\n'
                                   'Пожалуйста, напиши то, что я понимаю.')
