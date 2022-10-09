import aiogram
import utils
import states


async def send_achievements_message(message: aiogram.types.Message):
    learned_words = await utils.sql.db_actions.data_base.get_learned_words(message=message)
    best_score = await utils.sql.db_actions.data_base.get_best_score(message=message)
    if learned_words is None:
        await message.answer(text=f'Что-то я не могу найти слов в твоей библиотеке...',
                             disable_notification=True)
        if best_score == 0:
            await message.answer(text=f'Твой лучший счёт так же пуст.',
                                 disable_notification=True)
        else:
            await message.answer(text=f'Однако твой лучший счёт - {best_score}',
                                 disable_notification=True)
    else:
        await message.answer(text=f'Библиотека твоих слов:\n{", ".join(sorted(learned_words))}.',
                             disable_notification=True)
        await message.answer(text=f'Твой лучший счёт - {best_score}',
                             disable_notification=True)


def register_achievements_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(send_achievements_message, commands=['achievements'])
    dp.register_message_handler(send_achievements_message, commands=['achievements'],
                                state=states.begin_learn_words_steps.BeginLearnWordsSteps.
                                check_answer_correctness_state)
