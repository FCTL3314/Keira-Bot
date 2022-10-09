import aiogram
import data
import utils
import states


async def asks_for_words(message: aiogram.types.Message, number_of_words=data.config.NUMBER_OF_WORDS):
    """
    Entry-point of the ConversationHandler
    Asks the User to enter a words.
    Creates a score instance for a specific user.
    :return: number 0 for conversation handler state.
    """
    await message.answer(
        text=f'Введи {number_of_words}'
             f' {"изучаемых иностранных слова." if 5 > number_of_words > 1 else "изучаемых иностранных слов."}\n'
             f'Слова необходимо разделить пробелом и записать в одну строку.\n'
             f'Пример: {await utils.misc.other.create_words_example()}',
        disable_notification=True
    )
    await utils.misc.other.create_score_instance(message=message)
    await states.begin_learn_words_steps.BeginLearnWordsSteps.get_learning_words_state.set()


def register_set_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(asks_for_words, commands=['set'])
