import aiogram

from create_bot import bot


async def start_command(message: aiogram.types.Message):
    """Send a message that informs the user"""
    keira = await bot.get_me()
    await message.answer(
        text=f'Привет {message.from_user.first_name}! Меня зовут {keira.first_name}.',
        disable_notification=True
    )
    await message.answer(text=f'Я буду помогать тебе изучать иностранные слова.\n'
                              f'Сперва напиши команду /set, что бы установить их.\n'
                              f'Язык написанных тобою слов определяется автоматически.',
                         disable_notification=True)
    await message.answer(text=f'Слова, которые ты выучил, добавляются в твою библиотеку.\n'
                              f'Для того что бы выучить слова, тебе необходимо их верно переводить до тех пор,'
                              f' пока не появится соответствующее сообщение.',
                         disable_notification=True)
    await message.answer(
        text=f'Написав команду /achievements, ты увидишь библиотеку выученных слов, а так же свой лучший счёт.',
        disable_notification=True)


def register_start_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
