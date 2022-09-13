import telegram.ext


def unexpected_message_reply(update: telegram.Update, context: telegram.ext.CallbackContext):
    update.message.reply_text(text='Моей программой не предусмотрена предоставленная вами смысловая нагрузка. '
                                   'Пожалуйста, напишите то, что я понимаю :3')
