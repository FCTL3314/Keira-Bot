import aiogram
import utils
import states


async def check_translated_word_correctness(message: aiogram.types.Message):
    """Checks the translated word entered by the user for correctness"""
    if message.text.lower() == utils.misc.misc.get_random_translated_word(message=message).lower():
        await utils.misc.misc.correct_answer_response(message=message)
    else:
        await utils.misc.misc.wrong_answer_response(message=message)


def register_check_translated_word_correctness_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(check_translated_word_correctness, content_types=['text'],
                                state=states.begin_learn_words_steps.BeginLearnWordsSteps.
                                check_answer_correctness_state)
