import aiogram
import filters
import utils
import states


async def get_learning_words(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    """Gets user-entered words and writes it to FSM storage."""
    async with state.proxy() as user_data:
        user_data['learning_words'] = [word.capitalize() for word in message.text.split()]
        learning_words = user_data['learning_words']
    if await filters.validate_words(learning_words=learning_words, message=message):
        utils.misc.log_user_enter_words(username=message.from_user.username, first_name=message.from_user.first_name,
                                        learning_words=learning_words)
        await message.answer(text='⏳*Обработка...*', parse_mode='Markdown', disable_notification=True)
        async with state.proxy() as user_data:
            learning_words_translated = await utils.misc.translate_learning_words(learning_words=learning_words)
            user_data['learning_words_translated'] = learning_words_translated
            await utils.misc.send_message.send_words_accepted_message(
                learning_words=learning_words,
                learning_words_translated=learning_words_translated,
                message=message)
        await utils.misc.send_message.send_random_word_message(message=message, state=state)
        await states.set_command_state.SetCommandStates.next()


def register_get_learning_words_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=get_learning_words, content_types=['text'],
                                state=states.set_command_state.SetCommandStates.get_learning_words)
