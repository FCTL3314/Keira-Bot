import aiogram
import utils
import states


async def send_stop_translating_message(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    await message.answer(text='✅*Остановлено.*\nНапиши /set если желаешь начать заново.',
                         parse_mode='Markdown',
                         reply_markup=aiogram.types.reply_keyboard.ReplyKeyboardRemove(),
                         disable_notification=True)
    await state.finish()


def register_stop_command_handler(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=utils.misc.send_message.send_unable_execute_stop_command_message,
                                commands=['stop'])
    dp.register_message_handler(callback=send_stop_translating_message, commands=['stop'],
                                state=states.set_command_state.SetCommandStates.check_answer_correctness)
