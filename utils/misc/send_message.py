import aiogram
import data
import utils
import keyboards
import random


async def send_words_not_accepted_message(cause: str, message: aiogram.types.Message):
    match cause:
        case 'InvalidNumberOfWords':
            await message.answer(
                text='Ой, что-то пошло не так:\n'
                     f'Кол-во твоих слов - {len(data.user_data[f"learning_words: {message.from_user.id}"])}.',
                disable_notification=True)
        case 'WordsContainNumbers':
            await message.answer(
                text='Ой, что-то пошло не так:\n'
                     'Видимо, в введённых тобою словах имеются цифры.',
                disable_notification=True)
        case 'WordsContainPunctuation':
            await message.answer(
                text='Ой, что-то пошло не так:\n'
                     'Видимо, в введённых тобою словах имеются пунктуационные символы.',
                disable_notification=True)


async def send_words_accepted_message(message: aiogram.types.Message):
    """Sends 'words accepted message'. And sends a random word."""
    await message.answer(text='Обработка...', disable_notification=True)
    learning_words = data.user_data[f"learning_words: {message.from_user.id}"]
    learning_words_translated = await utils.misc.other.translate_learning_words(
        message=message,
        learning_words=data.user_data[f"learning_words: {message.from_user.id}"])
    accepted_words = ''.join(
        f'{learning_words[i]} - {learning_words_translated[i]}\n' for i in range(len(learning_words)))
    await message.answer(text=f'Слова приняты:\n{accepted_words}'
                              f'Изъявив желание прекратить переводить, напиши /stop.\n'
                              f'Далее тебе необходимо переводить слова:',
                         reply_markup=keyboards.default.create_keyboard_markup.create_keyboard_markup(
                             translated_words=data.user_data[f"learning_words_translated: {message.from_user.id}"]),
                         disable_notification=True)
    await utils.misc.send_message.send_random_word_message(message=message)


async def send_random_word_message(message: aiogram.types.Message, number_of_words=data.config.NUMBER_OF_WORDS):
    """Send random generated not previous word message"""
    try:
        data.bot_data[f"ran_num: {message.from_user.id}"] = await utils.misc.other.generate_not_previous_number(
            previous_number=data.bot_data[f"ran_num: {message.from_user.id}"], message=message)
    except KeyError:
        data.bot_data[f"ran_num: {message.from_user.id}"] = await utils.misc.other.generate_not_previous_number(
            previous_number=random.randint(0, number_of_words - 1), message=message)
    learning_words = data.user_data[f"learning_words: {message.from_user.id}"]
    ran_num = data.bot_data[f"ran_num: {message.from_user.id}"]
    await message.answer(text=f'{learning_words[ran_num]}', disable_notification=True)


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
                await utils.sql.db_actions.data_base.add_learned_words(
                    learned_words=data.user_data[f"learning_words: {message.from_user.id}"],
                    message=message)
            case _:
                await message.answer(text=f'🟢Верно!', disable_notification=True)
    elif user_score.get_score() > 20:
        await message.answer(
            text=f'🟢Серия верных ответов: {data.user_data[f"user_score: {message.from_user.id}"].get_score()}!',
            disable_notification=True)


async def send_wrong_answer_message(user_score, message: aiogram.types.Message):
    if 5 <= user_score.get_score() < 15:
        ran_num = random.randint(0, 2)
        match ran_num:
            case 0:
                await message.answer(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{utils.misc.other.get_random_translated_word(message=message)}.\n'
                         f'Да, знаю. Ошибки не самое приятное чувство.',
                    disable_notification=True)
            case 1:
                await message.answer(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{utils.misc.other.get_random_translated_word(message=message)}.\n'
                         f'Без ошибок эти слова уж точно не выучить.',
                    disable_notification=True)
            case 2:
                await message.answer(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{utils.misc.other.get_random_translated_word(message=message)}.\n'
                         f'Теперь-то уж ты точно запомнишь это слово.',
                    disable_notification=True)
    elif 15 <= user_score.get_score() < 20:
        await message.answer(
            text=f'🔴Неверно.\nПравильный вариант - '
                 f'{utils.misc.other.get_random_translated_word(message=message)}.\n'
                 f'Ничего страшного, ты был почти у цели!',
            disable_notification=True)
    elif user_score.get_score() > 20:
        await message.answer(
            text=f'🔴Неверно.\nПравильный вариант - '
                 f'{utils.misc.other.get_random_translated_word(message=message)}.\n'
                 'Ничто в мире не бесконечно, как и твоя серия верных ответов.')
    else:
        await message.answer(
            text=f'🔴Неверно.\nПравильный вариант - {utils.misc.other.get_random_translated_word(message=message)}.',
            disable_notification=True)


async def send_unable_execute_stop_command_message(message: aiogram.types.Message):
    await message.answer(text='Мне нечего останавливать. Напиши /set для начала.', disable_notification=True)
