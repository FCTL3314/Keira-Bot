import aiogram
import data
import utils
import states


async def send_ask_for_words_message(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext,
                                     number_of_words=data.config.NUMBER_OF_WORDS):
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
             f'Пример: {await utils.misc.misc.create_words_example()}',
        disable_notification=True
    )
    await utils.misc.user_score.create_score_instance(state=state)
    await states.learn_words_steps.LearnWordsSteps.get_learning_words_state.set()


def register_set_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=send_ask_for_words_message, commands=['set'])
