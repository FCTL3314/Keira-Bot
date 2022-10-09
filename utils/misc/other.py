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


async def create_score_instance(user_id):
    """"Creates a score instance for the specific user based on its id."""
    data.user_data[f'user_score: {user_id}'] = utils.misc.user_score.UserScore()


def console_display_user_words(message: aiogram.types.Message):
    if message.from_user.username:
        print(f'{message.from_user.username} - {data.user_data[f"learning_words: {message.from_user.id}"]}')
    else:
        print(f'{message.from_user.first_name} - {data.user_data[f"learning_words: {message.from_user.id}"]}')


async def translate_learning_words(learning_words: List[str], message: aiogram.types.Message,
                                   from_language=data.config.FROM_LANGUAGE,
                                   to_language=data.config.TO_LANGUAGE) -> List[str]:
    data.user_data[f"learning_words_translated: {message.from_user.id}"] = [translators.google(
        query_text=learning_words[word],
        from_language=from_language,
        to_language=to_language).capitalize()
                                                                            for word in range(len(learning_words))]
    return data.user_data[f"learning_words_translated: {message.from_user.id}"]


def get_random_translated_word(message: aiogram.types.Message) -> str:
    """
    Gets the predetermined random translated word, using [f"ran_num: {update.message.from_user.id}"] as a
    specific user keyword.
    """
    return data.user_data[f"learning_words_translated: {message.from_user.id}"][
        data.bot_data[f"ran_num: {message.from_user.id}"]]


async def correct_answer_response(message: aiogram.types.Message):
    user_score = data.user_data[f'user_score: {message.from_user.id}']
    user_score.increment()
    if await utils.sql.db_actions.data_base.get_best_score(message=message) < user_score.get_score():
        await utils.sql.db_actions.data_base.update_best_score(score=user_score.get_score(), message=message)
    await utils.misc.send_message.send_correct_answer_message(user_score=user_score, message=message)
    await utils.misc.send_message.send_random_word_message(message=message)


async def wrong_answer_response(message: aiogram.types.Message):
    user_score = data.user_data[f'user_score: {message.from_user.id}']
    await utils.misc.send_message.send_wrong_answer_message(user_score=user_score, message=message)
    user_score.reset()
    await utils.misc.send_message.send_random_word_message(message=message)


async def generate_not_previous_number(previous_number, message: aiogram.types.Message,
                                       number_of_words=data.config.NUMBER_OF_WORDS):
    """Creates a ran_num different from previous_ran_num"""
    ran_num = random.randint(0, number_of_words - 1)
    while ran_num == previous_number:
        ran_num = random.randint(0, number_of_words - 1)
    return ran_num
