import aiogram
import utils

from typing import List
from string import punctuation
from data.config import NUMBER_OF_WORDS


async def validate_words(learning_words: List[str], user_id, message: aiogram.types.Message,
                         number_of_words=NUMBER_OF_WORDS) -> bool:
    if await is_contains_punctuation(words=''.join(learning_words)):
        await utils.misc.send_message.send_words_not_accepted_message(learning_words=learning_words,
                                                                      cause='WordsContainPunctuation',
                                                                      message=message)
    elif await is_contains_numbers(words=''.join(learning_words)):
        await utils.misc.send_message.send_words_not_accepted_message(learning_words=learning_words,
                                                                      cause='WordsContainNumbers',
                                                                      message=message)
    elif await is_contains_repeated_words(words=learning_words):
        await utils.misc.send_message.send_words_not_accepted_message(learning_words=learning_words,
                                                                      cause='WordsRepeated',
                                                                      message=message)
    elif not len(learning_words) == number_of_words:
        await utils.misc.send_message.send_words_not_accepted_message(learning_words=learning_words,
                                                                      cause='InvalidNumberOfWords',
                                                                      message=message)
    elif not await is_word_length_allowed(words=learning_words):
        await utils.misc.send_message.send_words_not_accepted_message(learning_words=learning_words,
                                                                      cause='OneOfWordsTooLong',
                                                                      message=message)
    elif await is_contains_learned_words(words=learning_words, user_id=user_id):
        await utils.misc.send_message.send_words_contains_learned_words_message(message=message)
        return True
    else:
        return True


async def is_contains_punctuation(words: str) -> bool:
    for symbol in words:
        if symbol in punctuation:
            return True
    return False


async def is_contains_numbers(words: str) -> bool:
    for symbol in words:
        if symbol.isdigit():
            return True
    return False


async def is_contains_repeated_words(words: List[str]) -> bool:
    words = dict.fromkeys(words, 0)
    for word in words:
        words[word] += 1
        if words[word] > 1:
            return True
    return False


async def is_word_length_allowed(words: List[str]) -> bool:
    for word in words:
        if len(word) > 32:
            return False
    return True


async def is_contains_learned_words(words: List[str], user_id) -> bool:
    with utils.database.postgres_database as db:
        learned_words = await db.get_learned_words(user_id=user_id)
    if learned_words is None:
        return False
    else:
        for word in words:
            if word in learned_words:
                return True
        return False
