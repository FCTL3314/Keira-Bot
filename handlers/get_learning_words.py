import aiogram
import filters
import utils
import states


async def get_learning_words(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    """Gets user-entered words and writes is to context dict."""
    async with state.proxy() as user_data:
        user_data['learning_words'] = await create_learning_words_list(text=message.text, state=state)
        learning_words = user_data['learning_words']
    print(learning_words)
    if await filters.validate_words.validate_words(learning_words=learning_words, message=message, state=state):
        utils.misc.console_display_user_words(username=message.from_user.username,
                                              first_name=message.from_user.first_name,
                                              learning_words=learning_words)
        await states.learn_words_steps.LearnWordsSteps.next()


async def create_learning_words_list(text, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as user_data:
        user_data['learning_words'] = [word.capitalize() for word in text.split()]
    return user_data['learning_words']


def register_get_learning_words_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=get_learning_words, content_types=['text'],
                                state=states.learn_words_steps.LearnWordsSteps.get_learning_words_state)
