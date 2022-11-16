import aiogram
import data
import utils
import states


async def send_ask_for_words_message(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext,
                                     number_of_words=data.config.NUMBER_OF_WORDS):
    await message.answer(
        text=f'Введи {number_of_words}'
             f' {"изучаемых английских слова." if 4 >= number_of_words > 1 else "изучаемых английских слов."}\n'
             f'Слова необходимо разделить пробелом и записать в одну строку.\n'
             f'Пример: {await utils.misc.misc.create_words_example()}',
        disable_notification=True)
    await utils.misc.create_user_counter_instance(state=state)
    await states.learn_words.LearnWords.get_learning_words.set()


def register_set_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=send_ask_for_words_message, commands=['set'])
