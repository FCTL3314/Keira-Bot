import aiogram
import data
import utils

from typing import List
from string import punctuation


async def validate_words(learning_words: List[str], user_id, message: aiogram.types.Message,
                         number_of_words=data.config.NUMBER_OF_WORDS) -> bool:
    """
    Validate learning_words for correctness.
    :return: number 1 for conversation handler state.
    """
    if await is_contains_punctuation(learning_words=''.join(learning_words)):
        await utils.misc.send_message.send_words_not_accepted_message(learning_words=learning_words,
                                                                      cause='WordsContainPunctuation',
                                                                      message=message)
    elif await is_contains_numbers(learning_words=''.join(learning_words)):
        await utils.misc.send_message.send_words_not_accepted_message(learning_words=learning_words,
                                                                      cause='WordsContainNumbers',
                                                                      message=message)
    elif await is_contains_repeated_words(learning_words=learning_words):
        await utils.misc.send_message.send_words_not_accepted_message(learning_words=learning_words,
                                                                      cause='WordsRepeated',
                                                                      message=message)
    elif not len(learning_words) == number_of_words:
        await utils.misc.send_message.send_words_not_accepted_message(learning_words=learning_words,
                                                                      cause='InvalidNumberOfWords',
                                                                      message=message)
    elif await is_contains_learned_words(learning_words=learning_words, user_id=user_id):
        await utils.misc.send_message.send_words_contains_learned_words_message(message=message)
        return True
    else:
        return True


async def is_contains_punctuation(learning_words: str) -> bool:
    for symbol in learning_words:
        if symbol in punctuation:
            return True
    return False


async def is_contains_numbers(learning_words: str) -> bool:
    for symbol in learning_words:
        if symbol.isdigit():
            return True
    return False


async def is_contains_repeated_words(learning_words: List[str]) -> bool:
    words = dict.fromkeys(learning_words, 0)
    for word in learning_words:
        words[word] += 1
        if words[word] > 1:
            return True
    return False


async def is_contains_learned_words(learning_words: List[str], user_id) -> bool:
    with utils.database.postgres_database as db:
        learned_words = db.get_learned_words(user_id=user_id)
    if learned_words is None:
        return False
    else:
        for word in learning_words:
            if word in learned_words:
                return True
        return False
