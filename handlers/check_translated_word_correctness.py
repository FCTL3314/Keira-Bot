import aiogram
import utils
import states


async def check_translated_word_correctness(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    """Checks the translated word entered by the user for correctness"""
    async with state.proxy() as user_data:
        ran_num = user_data['ran_num']
        learning_words_translated = user_data['learning_words_translated']
    if message.text.lower() == learning_words_translated[ran_num].lower():
        await utils.misc.correct_answer_response(message=message, state=state)
    else:
        await utils.misc.wrong_answer_response(message=message, state=state)


def register_check_translated_word_correctness_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=check_translated_word_correctness, content_types=['text'],
                                state=states.learn_words.LearnWords.check_answer_correctness)
