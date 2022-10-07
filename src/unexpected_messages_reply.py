import aiogram


def unexpected_message_reply(message: aiogram.types.Message):
    message.answer(text='Моей программой не предусмотрена предоставленная тобою смысловая нагрузка.\n'
                        'Пожалуйста, напиши то, что я понимаю.')
