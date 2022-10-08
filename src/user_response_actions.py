import aiogram
import src
import random
import connectors
import create_bot


def get_random_translated_word(message: aiogram.types.Message) -> str:
    """
    Gets the predetermined random translated word, using [f"ran_num: {update.message.from_user.id}"] as a
    specific user keyword.
    """
    return create_bot.user_data[f"learning_words_translated: {message.from_user.id}"][
        create_bot.bot_data[f"ran_num: {message.from_user.id}"]]


async def check_answer_correctness(message: aiogram.types.Message):
    """Checks the translated word entered by the user for correctness"""
    if message.text.lower() == get_random_translated_word(message=message).lower():
        await correct_answer_response(message=message)
    else:
        await wrong_answer_response(message=message)


async def correct_answer_response(message: aiogram.types.Message):
    user_score = create_bot.user_data[f'user_score: {message.from_user.id}']
    user_score.increment()
    if await connectors.db_actions.data_base.get_best_score(message=message) < user_score.get_score():
        await connectors.db_actions.data_base.update_best_score(score=user_score.get_score(), message=message)
    await send_correct_answer_message(user_score=user_score, message=message)
    await src.send_random_word.send_random_word(message=message)


async def send_correct_answer_message(user_score, message: aiogram.types.Message):
    if user_score.get_score() <= 20:
        match user_score.get_score():
            case 5:
                await message.answer(text=f'🟢Верно!\nУ тебя не плохо получается!',
                                     disable_notification=True)
            case 10:
                await message.answer(text=f'🟢Верно!\nТы уже на половине пути, не теряй энтузиазма!',
                                     disable_notification=True)
            case 15:
                await message.answer(text=f'🟢Верно!\nЕщё чуть-чуть и ты их выучишь! Осталось совсем ничего!',
                                     disable_notification=True)
            case 20:
                await message.answer(text=f'✅Поздравляю! Слова выучены!\n'
                                          f'Написав команду /achievements, ты увидишь библиотеку выученных слов, '
                                          f'а так же свой лучший счёт.\n'
                                          f'Далее ты можешь совершенствовать свою серию верных ответов, '
                                          f'либо написать /stop что бы перестать переводить.',
                                     disable_notification=True)
                await connectors.db_actions.data_base.add_learned_words(
                    learned_words=create_bot.user_data[f"learning_words: {message.from_user.id}"],
                    message=message)
            case _:
                await message.answer(text=f'🟢Верно!', disable_notification=True)
    elif user_score.get_score() > 20:
        await message.answer(
            text=f'🟢Серия верных ответов: '
                 f'{create_bot.user_data[f"user_score: {message.from_user.id}"].get_score()}!',
            disable_notification=True)


async def wrong_answer_response(message: aiogram.types.Message):
    user_score = create_bot.user_data[f'user_score: {message.from_user.id}']
    await send_wrong_answer_message(user_score=user_score, message=message)
    user_score.reset()
    await src.send_random_word.send_random_word(message=message)


async def send_wrong_answer_message(user_score, message: aiogram.types.Message):
    if 5 <= user_score.get_score() < 15:
        ran_num = random.randint(0, 2)
        match ran_num:
            case 0:
                await message.answer(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{get_random_translated_word(message=message)}.\n'
                         f'Да, знаю. Ошибки не самое приятное чувство.',
                    disable_notification=True)
            case 1:
                await message.answer(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{get_random_translated_word(message=message)}.\n'
                         f'Без ошибок эти слова уж точно не выучить.',
                    disable_notification=True)
            case 2:
                await message.answer(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{get_random_translated_word(message=message)}.\n'
                         f'Теперь-то уж ты точно запомнишь это слово.',
                    disable_notification=True)
    elif 15 <= user_score.get_score() < 20:
        await message.answer(
            text=f'🔴Неверно.\nПравильный вариант - '
                 f'{get_random_translated_word(message=message)}.\n'
                 f'Ничего страшного, ты был почти у цели!',
            disable_notification=True)
    elif user_score.get_score() > 20:
        await message.answer(
            text=f'🔴Неверно.\nПравильный вариант - '
                 f'{get_random_translated_word(message=message)}.\n'
                 'Ничто в мире не бесконечно, как и твоя серия верных ответов.')
    else:
        await message.answer(
            text=f'🔴Неверно.\nПравильный вариант - {get_random_translated_word(message=message)}.',
            disable_notification=True)
