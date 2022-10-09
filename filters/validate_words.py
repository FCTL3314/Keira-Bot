import aiogram
import data
import utils

from typing import List
from string import punctuation


async def validate_words(learning_words: List[str], message: aiogram.types.Message,
                         number_of_words=data.config.NUMBER_OF_WORDS) -> bool:
    """
    Validate learning_words for correctness.
    :return: number 1 for conversation handler state.
    """
    if not await check_for_punctuation(learning_words=''.join(learning_words)):
        await utils.misc.send_message.send_words_not_accepted_message(message=message, cause='WordsContainPunctuation')
    elif not await check_for_numbers(learning_words=''.join(learning_words)):
        await utils.misc.send_message.send_words_not_accepted_message(message=message, cause='WordsContainNumbers')
    elif not len(learning_words) == number_of_words:
        await utils.misc.send_message.send_words_not_accepted_message(message=message, cause='InvalidNumberOfWords')
    else:
        await utils.misc.send_message.send_words_accepted_message(message=message)
        return True


async def check_for_punctuation(learning_words: str) -> bool:
    for symbol in learning_words:
        if symbol in punctuation:
            return False
    return True


async def check_for_numbers(learning_words: str) -> bool:
    for symbol in learning_words:
        if symbol.isdigit():
            return False
    return True
