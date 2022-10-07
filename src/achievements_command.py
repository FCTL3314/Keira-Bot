import aiogram
import connectors


async def send_achievements_message(message: aiogram.types.Message):
    learned_words = connectors.db_actions.data_base.get_learned_words(message=message)
    best_score = connectors.db_actions.data_base.get_best_score(message=message)
    if learned_words is None:
        await message.answer(text=f'Что-то я не могу найти слов в твоей библиотеке...')
        if best_score == 0:
            await message.answer(text=f'Твой лучший счёт так же пуст.')
        else:
            await message.answer(text=f'Однако твой лучший счёт - {best_score}')
    else:
        await message.answer(text=f'Библиотека твоих слов:\n{", ".join(learned_words)}.')
        await message.answer(text=f'Твой лучший счёт - {best_score}')


def register_achievements_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(send_achievements_message, commands=['achievements'])
