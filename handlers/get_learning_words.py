import aiogram
import data
import filters
import utils
import states


async def get_learning_words(message: aiogram.types.Message):
    """Gets user-entered words and writes is to context dict."""
    data.user_data[f"learning_words: {message.from_user.id}"] = [word.capitalize() for word in message.text.split()]
    if await filters.validate_words.validate_words(
            learning_words=data.user_data[f"learning_words: {message.from_user.id}"], message=message):
        utils.misc.console_display_user_words(message=message)
        await states.begin_learn_words_steps.BeginLearnWordsSteps.next()


def register_get_learning_words_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(get_learning_words, content_types=['text'],
                                state=states.begin_learn_words_steps.BeginLearnWordsSteps.get_learning_words_state)
