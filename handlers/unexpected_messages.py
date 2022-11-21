import aiogram


async def unexpected_message_reply(message: aiogram.types.Message):
    await message.answer(text='❕Моей программой не предусмотрена предоставленная тобою смысловая нагрузка. '
                              'Пожалуйста, напиши то, что я понимаю.',
                         parse_mode='Markdown',
                         disable_notification=True)


def register_unexpected_message_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=unexpected_message_reply)
