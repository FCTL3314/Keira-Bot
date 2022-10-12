import aiogram
import filters
import utils
import states


async def get_learning_words(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    """Gets user-entered words and writes it to FSM storage."""
    async with state.proxy() as user_data:
        user_data['learning_words'] = [word.capitalize() for word in message.text.split()]
        learning_words = user_data['learning_words']
    if await filters.validate_words.validate_words(learning_words=learning_words, message=message):
        utils.misc.console_display_user_words(username=message.from_user.username,
                                              first_name=message.from_user.first_name,
                                              learning_words=learning_words)
        await utils.misc.send_message.send_words_accepted_message(learning_words=learning_words,
                                                                  message=message,
                                                                  state=state)
        await states.learn_words_steps.LearnWordsSteps.next()


def register_get_learning_words_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=get_learning_words, content_types=['text'],
                                state=states.learn_words_steps.LearnWordsSteps.get_learning_words_state)
