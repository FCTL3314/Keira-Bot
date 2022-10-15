import aiogram
import states


async def send_stop_translating_message(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    await message.answer(text='Поняла, останавливаюсь...\nНапиши /set если желаешь начать заново.',
                         reply_markup=aiogram.types.reply_keyboard.ReplyKeyboardRemove(),
                         disable_notification=True)
    await state.finish()


async def send_unable_execute_stop_command_message(message: aiogram.types.Message):
    await message.answer(text='Мне нечего останавливать. Напиши /set для начала.', disable_notification=True)


def register_stop_command_handler(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=send_unable_execute_stop_command_message, commands=['stop'])
    dp.register_message_handler(callback=send_stop_translating_message, commands=['stop'],
                                state=states.learn_words_steps.LearnWordsSteps.check_answer_correctness_state)
