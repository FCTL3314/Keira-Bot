import aiogram


async def unexpected_message_reply(message: aiogram.types.Message):
    await message.answer(text='Моей программой не предусмотрена предоставленная тобою смысловая нагрузка. '
                              'Пожалуйста, напиши то, что я понимаю.',
                         disable_notification=True)


def register_unexpected_message_handler(dp: aiogram.Dispatcher):
    dp.register_message_handler(unexpected_message_reply)
