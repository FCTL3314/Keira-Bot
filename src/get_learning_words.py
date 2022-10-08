import aiogram
import translators
import src
import configurations
import create_bot

from typing import List
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Steps(StatesGroup):
    GET_LEARNING_WORDS_STATE = State()
    CHECK_ANSWER_CORRECTNESS_STATE = State()


async def asks_for_words(message: aiogram.types.Message, number_of_words=configurations.config.NUMBER_OF_WORDS):
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
             f'Пример: {await create_input_words_example()}',
        disable_notification=True
    )
    await create_score_instance(message=message)
    await Steps.GET_LEARNING_WORDS_STATE.set()


async def create_input_words_example(number_of_words=configurations.config.NUMBER_OF_WORDS) -> str:
    """Return string with the number of words equal to configurations.settings.NUMBER_OF_WORDS."""
    words = ['Berries', 'Apple', 'Cinnamon', 'Coffee', 'Milk', 'Cookies']
    return ' '.join(words[:number_of_words])


async def create_score_instance(message: aiogram.types.Message):
    """"Creates a score instance for the specific user based on its id"""
    create_bot.user_data[f'user_score: {message.from_user.id}'] = src.user_score.UserScore()


async def get_learning_words(message: aiogram.types.Message):
    """Gets user-entered words and writes is to context dict."""
    create_bot.user_data[f"learning_words: {message.from_user.id}"] = [word.capitalize() for word in
                                                                       message.text.split()]
    if await validate_learning_words(
            learning_words=create_bot.user_data[f"learning_words: {message.from_user.id}"], message=message):
        print(f'{message.from_user.username} - {create_bot.user_data[f"learning_words: {message.from_user.id}"]}')
        await Steps.next()


async def validate_learning_words(learning_words: List[str], message: aiogram.types.Message,
                                  number_of_words=configurations.config.NUMBER_OF_WORDS) -> bool:
    """
    Validate learning_words for correctness.
    :return: number 1 for conversation handler state.
    """
    if not await check_for_numbers(learning_words=learning_words):
        await words_not_accepted(message=message, cause='WordsContainNumbers')
    elif not len(learning_words) == number_of_words:
        await words_not_accepted(message=message, cause='InvalidNumberOfWords')
    else:
        await send_words_accepted_message(message=message)
        return True


async def check_for_numbers(learning_words: List[str]) -> bool:
    for symbol in str(learning_words):
        if symbol.isdigit():
            return False
    return True


async def words_not_accepted(cause: str, message: aiogram.types.Message):
    if cause == 'InvalidNumberOfWords':
        await message.answer(
            text='Ой, что-то пошло не так:\n'
                 f'Кол-во твоих слов - {len(create_bot.user_data[f"learning_words: {message.from_user.id}"])}.',
            disable_notification=True
        )
    if cause == 'WordsContainNumbers':
        await message.answer(
            text='Ой, что-то пошло не так:\n'
                 'Видимо, в введённых тобою словах имеются цифры.',
            disable_notification=True
        )


async def send_words_accepted_message(message: aiogram.types.Message):
    """Sends 'words accepted message'. And sends a random word."""
    await message.answer(text='Обработка...', disable_notification=True)
    learning_words = create_bot.user_data[f"learning_words: {message.from_user.id}"]
    learning_words_translated = await translate_learning_words(message=message,
                                                               learning_words=create_bot.user_data[
                                                                   f"learning_words: {message.from_user.id}"])
    accepted_words = ''.join(
        f'{learning_words[i]} - {learning_words_translated[i]}\n' for i in range(len(learning_words)))
    await message.answer(text=f'Слова приняты:\n{accepted_words}'
                              f'Изъявив желание прекратить переводить, напиши /stop.\n'
                              f'Далее тебе необходимо переводить слова:',
                         reply_markup=src.create_keyboard_markup.create_keyboard_markup(
                             translated_words=create_bot.user_data[
                                 f"learning_words_translated: {message.from_user.id}"]),
                         disable_notification=True
                         )
    # bot.send_random_word.send_random_word(update=update, context=context)
    await message.answer(text='RAN NUM')


async def translate_learning_words(learning_words: List[str], message: aiogram.types.Message,
                                   from_language=configurations.config.FROM_LANGUAGE,
                                   to_language=configurations.config.TO_LANGUAGE) -> List[str]:
    create_bot.user_data[f"learning_words_translated: {message.from_user.id}"] = [
        translators.google(query_text=learning_words[word],
                           from_language=from_language,
                           to_language=to_language)
        for word in range(len(learning_words))]
    return [word.capitalize() for word in create_bot.user_data[f"learning_words_translated: {message.from_user.id}"]]


def register_start_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(asks_for_words, commands=['set'], state=None)
    dp.register_message_handler(get_learning_words, state=Steps.GET_LEARNING_WORDS_STATE)
    dp.register_message_handler(send_words_accepted_message, state=Steps.CHECK_ANSWER_CORRECTNESS_STATE)
