import aiogram
import data
import utils.misc
import translators
import random

from typing import List


async def create_words_example(number_of_words=data.config.NUMBER_OF_WORDS) -> str:
    """Return string with the number of words equal to configurations.settings.NUMBER_OF_WORDS."""
    words = ['Berries', 'Apple', 'Cinnamon', 'Coffee', 'Milk', 'Cookies']
    return ' '.join(words[:number_of_words])


async def translate_learning_words(learning_words: List[str],
                                   state: aiogram.dispatcher.FSMContext,
                                   from_language=data.config.FROM_LANGUAGE,
                                   to_language=data.config.TO_LANGUAGE) -> List[str]:
    await state.update_data(learning_words_translated=[translators.google(
        query_text=learning_words[word],
        from_language=from_language,
        to_language=to_language).capitalize() for word in range(len(learning_words))])
    user_data = await state.get_data()
    return user_data.get('learning_words_translated')


async def get_random_translated_word(state: aiogram.dispatcher.FSMContext) -> str:
    """
    Gets the predetermined random translated word, using [f"ran_num: {update.message.from_user.id}"] as a
    specific user keyword.
    """
    user_data = await state.get_data()
    bot_data = await state.get_data()
    return user_data.get('learning_words_translated')[bot_data.get('ran_num')]


async def correct_answer_response(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    user_score = data.user_data[f'user_score: {message.from_user.id}']
    user_score.increment()
    with utils.sql.database as db:
        if db.get_best_score(user_id=message.from_user.id) < user_score.get_score():
            db.update_best_score(score=user_score.get_score(), user_id=message.from_user.id)
    await utils.misc.send_message.send_correct_answer_message(user_score=user_score, message=message)
    await utils.misc.send_message.send_random_word_message(message=message, state=state)


async def wrong_answer_response(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    user_score = data.user_data[f'user_score: {message.from_user.id}']
    await utils.misc.send_message.send_wrong_answer_message(user_score=user_score, message=message, state=state)
    user_score.reset()
    await utils.misc.send_message.send_random_word_message(message=message, state=state)


async def generate_not_previous_number(previous_number, number_of_words=data.config.NUMBER_OF_WORDS):
    """Creates a ran_num different from previous_ran_num"""
    ran_num = random.randint(0, number_of_words - 1)
    while ran_num == previous_number:
        ran_num = random.randint(0, number_of_words - 1)
    return ran_num


def console_display_user_words(username, first_name, learning_words):
    if username:
        print(f'{username} - {learning_words}')
    else:
        print(f'{first_name} - {learning_words}')
