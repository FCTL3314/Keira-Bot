import aiogram
import data
import utils
import keyboards
import random


async def send_words_accepted_message(learning_words, message: aiogram.types.Message,
                                      state: aiogram.dispatcher.FSMContext):
    """Sends 'words accepted message'. And sends a random word."""
    await message.answer(text='Обработка...', disable_notification=True)
    learning_words_translated = await utils.misc.translate_learning_words(learning_words=learning_words, state=state)
    accepted_words = ''.join(
        f'{learning_words[i]} - {learning_words_translated[i]}\n' for i in range(len(learning_words)))
    await message.answer(text=f'Слова приняты:\n{accepted_words}'
                              f'Изъявив желание прекратить переводить, напиши /stop.\n'
                              f'Далее тебе необходимо переводить слова:',
                         reply_markup=keyboards.default.create_keyboard_markup.create_keyboard_markup(
                             text=learning_words_translated),
                         disable_notification=True)
    await utils.misc.send_message.send_random_word_message(message=message, state=state)


async def send_words_not_accepted_message(learning_words, cause: str, message: aiogram.types.Message):
    match cause:
        case 'InvalidNumberOfWords':
            await message.answer(
                text='Ой, что-то пошло не так:\n'
                     f'Кол-во твоих слов - {len(learning_words)}.',
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


async def send_random_word_message(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext,
                                   number_of_words=data.config.NUMBER_OF_WORDS):
    """Send random generated not previous word message"""
    async with state.proxy() as user_data:
        try:
            user_data['ran_num'] = await utils.misc.generate_not_previous_number(previous_number=user_data['ran_num'])
        except KeyError:
            user_data['ran_num'] = random.randint(0, number_of_words - 1)
        bot_data = await state.get_data()
        learning_words = bot_data.get('learning_words')
        ran_num = user_data['ran_num']
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
            case _:
                await message.answer(text=f'🟢Верно!', disable_notification=True)
    elif user_score.get_score() > 20:
        await message.answer(
            text=f'🟢Серия верных ответов: {user_score.get_score()}!', disable_notification=True)


async def send_wrong_answer_message(user_score, message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if 5 <= user_score.get_score() < 15:
        ran_case = random.randint(0, 2)
        match ran_case:
            case 0:
                await message.answer(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{await utils.misc.get_random_translated_word(state=state)}.\n'
                         f'Да, знаю. Ошибки не самое приятное чувство.',
                    disable_notification=True)
            case 1:
                await message.answer(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{await utils.misc.get_random_translated_word(state=state)}.\n'
                         f'Без ошибок эти слова уж точно не выучить.',
                    disable_notification=True)
            case 2:
                await message.answer(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{await utils.misc.get_random_translated_word(state=state)}.\n'
                         f'Теперь-то уж ты точно запомнишь это слово.',
                    disable_notification=True)
    elif 15 <= user_score.get_score() < 20:
        await message.answer(
            text=f'🔴Неверно.\nПравильный вариант - '
                 f'{await utils.misc.get_random_translated_word(state=state)}.\n'
                 f'Ничего страшного, ты был почти у цели!',
            disable_notification=True)
    elif user_score.get_score() > 20:
        await message.answer(
            text=f'🔴Неверно.\nПравильный вариант - '
                 f'{await utils.misc.get_random_translated_word(state=state)}.\n'
                 'Ничто в мире не бесконечно, как и твоя серия верных ответов.')
    else:
        await message.answer(
            text=f'🔴Неверно.\nПравильный вариант - {utils.misc.get_random_translated_word(state=state)}.',
            disable_notification=True)
