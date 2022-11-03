import aiogram
import utils


async def start_command(message: aiogram.types.Message):
    user_id = message.from_user.id
    await message.answer(text=f'✋Привет {message.from_user.first_name}! Меня зовут Кейра.\n'
                              'Я буду помогать тебе изучать английские слова. '
                              'Переводя их, ты повышаешь степень изученности слов до тех пор, '
                              'пока они не станут выученными. '
                              'Выученные слова, добавляются в твою библиотеку. '
                              'Вдобавок, я буду награждать тебя различными достижениями.',
                         disable_notification=True)
    await message.answer(
        text=f'Написав команду /progress, ты увидишь библиотеку выученных слов, а так же витрину своих достижений.',
        disable_notification=True)
    with utils.database.postgres_database as db:
        if not db.get_pioneer_achievement(user_id=user_id):
            await db.set_pioneer_achievement(user_id=user_id)
            await utils.misc.send_message.send_pioneer_achievement_received_message(message=message)


def register_start_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
