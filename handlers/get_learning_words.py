import aiogram
import filters
import utils
import states


async def get_learning_words(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    """Gets user-entered words and writes is to context dict."""
    await state.update_data(learning_words=[word.capitalize() for word in message.text.split()])
    user_data = await state.get_data()
    if await filters.validate_words.validate_words(learning_words=user_data.get('learning_words'),
                                                   message=message,
                                                   state=state):
        utils.misc.console_display_user_words(username=message.from_user.username,
                                              first_name=message.from_user.first_name,
                                              learning_words=user_data.get('learning_words'))
        await states.learn_words_steps.LearnWordsSteps.next()


def register_get_learning_words_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=get_learning_words, content_types=['text'],
                                state=states.learn_words_steps.LearnWordsSteps.get_learning_words_state)
