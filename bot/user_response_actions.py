import telegram.ext
import bot
import random
import connectors.db_actions

from typing import List


def get_random_translated_word(update: telegram.Update, context: telegram.ext.CallbackContext) -> str:
    """Gets the translated word from context.user_data['learning_words_translated']"""
    translated_word = context.user_data['learning_words_translated'][
        context.bot_data[f"ran_num: {update.message.from_user.id}"]]
    return translated_word


def check_answer_correctness(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Checks the translated word entered by the user for correctness"""
    answer = update.message.text
    if answer.lower() == get_random_translated_word(update=update, context=context).lower():
        correct_answer_response(update=update, context=context)
    else:
        wrong_answer_response(update=update, context=context)


def correct_answer_response(update: telegram.Update, context: telegram.ext.CallbackContext):
    user_score = context.user_data[f'user_score: {update.message.from_user.id}']
    user_score.increment()
    connectors.db_actions.db_update_best_score(score=user_score.get_score(), update=update)
    match user_score.get_score():
        case 5:
            update.message.reply_text(text=f'🟢5 раз подряд!\nПродолжай в том же духе!',
                                      disable_notification=True)
        case 10:
            update.message.reply_text(text=f'🟢10 раз подряд!\nТы уже на половине пути, осталось совсем ничего!',
                                      disable_notification=True)
        case 15:
            update.message.reply_text(text=f'🟢15 раз подряд!\nЕщё чуть-чуть и ты их выучишь! Я в тебя верю!',
                                      disable_notification=True)
        case 20:
            update.message.reply_text(text=f'✅Поздравляю! Ты выучил слова!\n'
                                           f'Напиши /achievements что бы посмотреть свои достижения.',
                                      disable_notification=True)
            connectors.db_actions.db_add_learned_words(
                learned_words=create_words_concatenation(update=update, context=context), update=update)
        case _ if user_score.get_score() > 20:
            update.message.reply_text(
                text=f'🟢Серия верных ответов:'
                     f' {context.user_data[f"user_score: {update.message.from_user.id}"].get_score()}!',
                disable_notification=True)
        case _:
            update.message.reply_text(text=f'🟢Верно!', disable_notification=True)
    bot.generate_random_word(update=update, context=context)


def create_words_concatenation(update: telegram.Update, context: telegram.ext.CallbackContext) -> List[str]:
    if connectors.db_actions.db_get_learned_words(update=update) is None:
        words_concatenation = context.user_data['learning_words']
    else:
        words_concatenation = context.user_data['learning_words'] + connectors.db_actions.db_get_learned_words(
            update=update)
    return words_concatenation


def wrong_answer_response(update: telegram.Update, context: telegram.ext.CallbackContext):
    reset_correct_answers_series(update=update, context=context)
    update.message.reply_text(
        text=f'🔴Неверно.\nПравильный вариант - {get_random_translated_word(update=update, context=context)}',
        disable_notification=True)
    bot.generate_random_word(update=update, context=context)


def reset_correct_answers_series(update: telegram.Update, context: telegram.ext.CallbackContext):
    user_score = context.user_data[f'user_score: {update.message.from_user.id}']
    if 10 <= user_score.get_score() < 15:
        ran_num = random.randint(0, 2)
        match ran_num:
            case 0:
                update.message.reply_text(text=f'Да, знаю. Обидно терять такую серию правильных ответов.',
                                          disable_notification=True)
            case 1:
                update.message.reply_text(text=f'Не переживай. Без ошибок эти слова явно не выучить.',
                                          disable_notification=True)
            case 2:
                update.message.reply_text(text=f'Зато теперь ты точно запомнишь это слово.',
                                          disable_notification=True)
    elif 15 <= user_score.get_score() < 20:
        update.message.reply_text(text=f'Главное не останавливайся, у тебя всё получится! Ты был почти у цели!.',
                                  disable_notification=True)

    context.user_data[f'user_score: {update.message.from_user.id}'].reset()
