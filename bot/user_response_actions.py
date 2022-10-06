import telegram.ext
import bot
import random
import connectors.db_actions


def get_random_translated_word(update: telegram.Update, context: telegram.ext.CallbackContext) -> str:
    """
    Gets the predetermined random translated word, using [f"ran_num: {update.message.from_user.id}"] as a
    specific user keyword.
    """
    return context.user_data['learning_words_translated'][context.bot_data[f"ran_num: {update.message.from_user.id}"]]


def check_answer_correctness(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Checks the translated word entered by the user for correctness"""
    if update.message.text.lower() == get_random_translated_word(update=update, context=context).lower():
        correct_answer_response(update=update, context=context)
    else:
        wrong_answer_response(update=update, context=context)


def correct_answer_response(update: telegram.Update, context: telegram.ext.CallbackContext):
    user_score = context.user_data[f'user_score: {update.message.from_user.id}']
    user_score.increment()
    if connectors.db_actions.db_get_best_score(update=update) < user_score.get_score():
        connectors.db_actions.db_update_best_score(score=user_score.get_score(), update=update)
    send_correct_answer_message(user_score=user_score, update=update, context=context)
    bot.send_random_word(update=update, context=context)


def send_correct_answer_message(user_score, update: telegram.Update, context: telegram.ext.CallbackContext):
    if user_score.get_score() <= 20:
        match user_score.get_score():
            case 5:
                update.message.reply_text(text=f'🟢Верно!\nУ тебя не плохо получается!',
                                          disable_notification=True)
            case 10:
                update.message.reply_text(text=f'🟢Верно!\nТы уже на половине пути, не теряй энтузиазма!',
                                          disable_notification=True)
            case 15:
                update.message.reply_text(text=f'🟢Верно!\nЕщё чуть-чуть и ты их выучишь! Осталось совсем ничего!',
                                          disable_notification=True)
            case 20:
                update.message.reply_text(text=f'✅Поздравляю! Слова выучены!\n'
                                               f'Написав команду /achievements, ты увидишь библиотеку выученных слов, '
                                               f'а так же свой лучший счёт.\n'
                                               f'Далее ты можешь совершенствовать свою серию верных ответов, '
                                               f'либо написать /stop что бы перестать переводить.',
                                          disable_notification=True)
                connectors.db_actions.db_add_learned_words(learned_words=context.user_data['learning_words'],
                                                           update=update)
            case _:
                update.message.reply_text(text=f'🟢Верно!', disable_notification=True)
    elif user_score.get_score() > 20:
        update.message.reply_text(
            text=f'🟢Серия верных ответов: '
                 f'{context.user_data[f"user_score: {update.message.from_user.id}"].get_score()}!',
            disable_notification=True)


def wrong_answer_response(update: telegram.Update, context: telegram.ext.CallbackContext):
    user_score = context.user_data[f'user_score: {update.message.from_user.id}']
    send_wrong_answer_message(user_score=user_score, update=update, context=context)
    user_score.reset()
    bot.send_random_word(update=update, context=context)


def send_wrong_answer_message(user_score, update: telegram.Update, context: telegram.ext.CallbackContext):
    if 5 <= user_score.get_score() < 15:
        ran_num = random.randint(0, 2)
        match ran_num:
            case 0:
                update.message.reply_text(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{get_random_translated_word(update=update, context=context)}.\n'
                         f'Да, знаю. Ошибки не самое приятное чувство.',
                    disable_notification=True)
            case 1:
                update.message.reply_text(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{get_random_translated_word(update=update, context=context)}.\n'
                         f'Без ошибок эти слова уж точно не выучить.',
                    disable_notification=True)
            case 2:
                update.message.reply_text(
                    text=f'🔴Неверно.\nПравильный вариант - '
                         f'{get_random_translated_word(update=update, context=context)}.\n'
                         f'Теперь-то уж ты точно запомнишь это слово.',
                    disable_notification=True)
    elif 15 <= user_score.get_score() < 20:
        update.message.reply_text(
            text=f'🔴Неверно.\nПравильный вариант - '
                 f'{get_random_translated_word(update=update, context=context)}.\n'
                 f'Ничего страшного, ты был почти у цели!',
            disable_notification=True)
    elif user_score.get_score() > 20:
        update.message.reply_text(
            text=f'🔴Неверно.\nПравильный вариант - '
                 f'{get_random_translated_word(update=update, context=context)}.\n'
                 'Ничто в мире не бесконечно, как и твоя серия верных ответов.')
    else:
        update.message.reply_text(
            text=f'🔴Неверно.\nПравильный вариант - {get_random_translated_word(update=update, context=context)}.',
            disable_notification=True)
