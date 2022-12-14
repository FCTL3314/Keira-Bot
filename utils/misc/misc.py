import random
import logging
import aiogram
import utils
import async_google_trans_new

from typing import List
from data.config import NUMBER_OF_WORDS, FROM_LANGUAGE, TO_LANGUAGE, CORRECT_ANSWERS_TO_LEARN_WORDS


async def create_words_example(number_of_words=NUMBER_OF_WORDS) -> str:
    words = ['Berries', 'Apple', 'Cinnamon', 'Coffee', 'Milk', 'Cookies']
    return ' '.join(words[:number_of_words])


async def create_achievements_text(message: aiogram.types.Message):
    achievements = list()
    with utils.database.postgres_database as db:
        if await db.get_achievement(achievement='pioneer_achievement', message=message):
            achievements.append("🌄Первопроходец - Спасибо за использование проекта, начиная с самых ранних дней!")
        if await db.get_achievement(achievement='scrabble_achievement', message=message):
            achievements.append("🎓Эрудит - Выучить свои первые слова.")
    return '\n\n● '.join(achievements)


async def translate_learning_words(learning_words: List[str]) -> List[str]:
    translator = async_google_trans_new.AsyncTranslator()
    translated_words = [await translator.translate(
        text=learning_words[word],
        lang_src=FROM_LANGUAGE,
        lang_tgt=TO_LANGUAGE) for word in range(NUMBER_OF_WORDS)]
    # Capitalize and removes last symbol from every word due to the inability to do this in the coroutine object.
    learning_words_translated = [translated_words[word].strip().capitalize() for
                                 word in range(NUMBER_OF_WORDS)]
    return learning_words_translated


async def get_random_translated_word(state: aiogram.dispatcher.FSMContext) -> str:
    """Gets the predetermined random translated word"""
    async with state.proxy() as user_data:
        ran_num = user_data['ran_num']
        learning_words_translated = user_data['learning_words_translated']
    return learning_words_translated[ran_num]


async def correct_answer_response(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as user_data:
        user_counter = user_data['user_counter']
        learning_words = user_data['learning_words']
        user_data['user_counter'].increment()
    with utils.database.postgres_database as db:
        if user_counter.get_score() == CORRECT_ANSWERS_TO_LEARN_WORDS:
            log_user_learned_words(username=message.from_user.username, first_name=message.from_user.first_name,
                                   learning_words=learning_words)
            await db.add_learned_words(words=learning_words, message=message)
            await utils.misc.send_message.send_words_learned_message(message=message)
            if not await db.get_achievement(achievement='scrabble_achievement', message=message):
                await db.set_achievement(achievement='scrabble_achievement', message=message)
                await utils.misc.send_message.send_scrabble_achievement_received_message(message=message)
            await state.finish()
        else:
            await utils.misc.send_message.send_correct_answer_message(user_counter=user_counter, message=message)
            await utils.misc.send_message.send_random_word_message(message=message, state=state)


async def wrong_answer_response(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as user_data:
        user_counter = user_data['user_counter']
        user_counter.decrement()
        await utils.misc.send_message.send_wrong_answer_message(user_counter=user_counter, message=message, state=state)
    await utils.misc.send_message.send_random_word_message(message=message, state=state)


async def generate_not_previous_number(previous_number, number_of_words=NUMBER_OF_WORDS):
    ran_num = random.randint(0, number_of_words - 1)
    while ran_num == previous_number:
        ran_num = random.randint(0, number_of_words - 1)
    return ran_num


async def create_user_counter_instance(state: aiogram.dispatcher.FSMContext):
    """"Creates a score instance for the specific user based on its id."""
    async with state.proxy() as user_data:
        user_data['user_counter'] = utils.misc.user_counter.UserCounter()


def log_user_enter_words(username, first_name, learning_words):
    if username:
        logging.info(msg=f'User {username} enter words: {learning_words}')
    else:
        logging.info(msg=f'Person {first_name} enter words: {learning_words}')


def log_user_learned_words(username, first_name, learning_words):
    if username:
        logging.info(msg=f'User {username} learned words: {learning_words}')
    else:
        logging.info(msg=f'Person {first_name} learned words: {learning_words}')
