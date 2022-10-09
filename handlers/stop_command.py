import aiogram
import data
import states
import utils


async def stop_translate(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    await message.answer(text='Поняла, останавливаюсь...\nНапиши /set если желаешь начать заново.',
                         reply_markup=aiogram.types.reply_keyboard.ReplyKeyboardRemove(),
                         disable_notification=True)
    data.user_data[f'user_score: {message.from_user.id}'].reset()
    await state.finish()


def register_stop_command_handler(dp: aiogram.Dispatcher):
    dp.register_message_handler(utils.misc.send_message.send_unable_execute_stop_command_message, commands=['stop'])
    dp.register_message_handler(stop_translate, commands=['stop'],
                                state=states.begin_learn_words_steps.BeginLearnWordsSteps.
                                check_answer_correctness_state)
