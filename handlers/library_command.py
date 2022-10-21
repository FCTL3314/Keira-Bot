import aiogram
import utils
import states


async def send_library_message(message: aiogram.types.Message):
    with utils.database.postgres_database as db:
        learned_words = db.get_learned_words(user_id=message.from_user.id)
    if learned_words is None:
        await message.answer(text=f'❕Что-то я не могу найти слов в твоей библиотеке...',
                             disable_notification=True)
    else:
        await message.answer(text=f'📜Библиотека твоих слов:\n{", ".join(sorted(learned_words))}.',
                             disable_notification=True)


def register_library_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=send_library_message, commands=['library'])
    dp.register_message_handler(callback=send_library_message, commands=['library'],
                                state=states.learn_words_steps.LearnWordsSteps.check_answer_correctness_state)
