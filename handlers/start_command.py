import aiogram
import utils


async def start_command(message: aiogram.types.Message):
    await message.answer(text=f'✋*Привет {message.from_user.first_name}! Меня зовут Кейра.\n'
                              'Я буду помогать тебе изучать английские слова. '
                              'Переводя их, ты повышаешь степень изученности слов до тех пор, '
                              'пока они не станут выученными. '
                              'Выученные слова, добавляются в твою библиотеку. '
                              'Вдобавок, я буду награждать тебя различными достижениями.*',
                         parse_mode='Markdown',
                         disable_notification=True)
    await message.answer(
        text=f'❕Написав команду /progress, ты увидишь библиотеку выученных слов, а так же витрину своих достижений.',
        disable_notification=True)
    with utils.database.postgres_database as db:
        if not await db.get_achievement(achievement='pioneer_achievement', message=message):
            await db.set_achievement(achievement='pioneer_achievement', message=message)
            await utils.misc.send_message.send_pioneer_achievement_received_message(message=message)


def register_start_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
