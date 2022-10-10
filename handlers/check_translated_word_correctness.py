import aiogram
import utils
import states


async def check_translated_word_correctness(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    """Checks the translated word entered by the user for correctness"""
    user_data = await state.get_data()
    bot_data = await state.get_data()
    if message.text.lower() == user_data.get('learning_words_translated')[bot_data.get('ran_num')].lower():
        await utils.misc.correct_answer_response(message=message, state=state)
    else:
        await utils.misc.wrong_answer_response(message=message, state=state)


def register_check_translated_word_correctness_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=check_translated_word_correctness, content_types=['text'],
                                state=states.learn_words_steps.LearnWordsSteps.check_answer_correctness_state)
