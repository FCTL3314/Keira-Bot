import telegram.ext
import translators
import bot
import connectors.db_actions
import configurations.config

from bot import GET_LEARNING_WORDS_STATE
from bot import CHECK_ANSWER_CORRECTNESS_STATE
from typing import List


def asks_for_words(update: telegram.Update, context: telegram.ext.CallbackContext,
                   number_of_words=configurations.config.NUMBER_OF_WORDS) -> int:
    """
    Entry-point of the ConversationHandler
    Asks the User to enter a words.
    Creates a score instance for a specific user.
    :return: number 0 for conversation handler state.
    """
    update.message.reply_text(
        text=f'Введи {number_of_words}'
             f' {"изучаемых иностранных слова." if 5 > number_of_words > 1 else "изучаемых иностранных слов."}\n'
             f'Слова необходимо разделить пробелом и записать в одну строку.\n'
             f'Пример: {create_input_words_example()}',
        disable_notification=True
    )
    create_score_instance(update=update, context=context)
    return GET_LEARNING_WORDS_STATE


def create_input_words_example(number_of_words=configurations.config.NUMBER_OF_WORDS) -> str:
    """Return string with the number of words equal to configurations.settings.NUMBER_OF_WORDS."""
    words = ['Berries', 'Apple', 'Cinnamon', 'Coffee', 'Milk', 'Cookies']
    return ' '.join(words[:number_of_words])


def get_learning_words(update: telegram.Update, context: telegram.ext.CallbackContext) -> int:
    """Gets user-entered words and writes is to context dict."""
    context.user_data['learning_words'] = [word.capitalize() for word in update.message.text.split()]
    if validate_learning_words(learning_words=context.user_data['learning_words'], update=update, context=context):
        print(f'{update.message.from_user.name} - {context.user_data["learning_words"]}')
        return CHECK_ANSWER_CORRECTNESS_STATE


def validate_learning_words(learning_words: List[str], update: telegram.Update,
                            context: telegram.ext.CallbackContext,
                            number_of_words=configurations.config.NUMBER_OF_WORDS) -> bool:
    """
    Validate learning_words for correctness.
    :return: number 1 for conversation handler state.
    """
    if not check_for_numbers(learning_words=learning_words):
        words_not_accepted(update=update, context=context, cause='WordsContainNumbers')
    elif not len(learning_words) == number_of_words:
        words_not_accepted(update=update, context=context, cause='InvalidNumberOfWords')
    else:
        connectors.db_actions.db_create_user_info(update=update)
        send_words_accepted_message(update=update, context=context)
        return True


def create_score_instance(update: telegram.Update, context: telegram.ext.CallbackContext):
    """"Creates a score instance for the specific user based on its id"""
    context.user_data[f'user_score: {update.message.chat_id}'] = bot.user_score.UserScore()


def stop_conversation(update: telegram.Update, context: telegram.ext.CallbackContext):
    update.message.reply_text(text='Поняла, останавливаюсь...\nНапишите /set если желаете начать заново.',
                              reply_markup=telegram.ReplyKeyboardRemove(),
                              disable_notification=True)
    context.user_data[f'user_score: {update.message.from_user.id}'].reset()
    return telegram.ext.ConversationHandler.END


def check_for_numbers(learning_words: List[str]) -> bool:
    for symbol in str(learning_words):
        if symbol.isdigit():
            return False
    return True


def send_words_accepted_message(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Sends 'words accepted message'. And sends a random word."""
    update.message.reply_text(text='Обработка...', disable_notification=True)
    learning_words = context.user_data['learning_words']
    learning_words_translated = translate_learning_words(context=context,
                                                         learning_words=context.user_data['learning_words'])
    accepted_words = ''.join(
        f'{learning_words[i]} - {learning_words_translated[i]}\n' for i in range(len(learning_words)))
    update.message.reply_text(text=f'Слова приняты:\n{accepted_words}'
                                   f'Изъявив желание прекратить переводить, напиши /stop.\n'
                                   f'Далее тебе необходимо переводить слова:',
                              reply_markup=bot.create_keyboard_markup(
                                  translated_words=context.user_data['learning_words_translated']),
                              disable_notification=True
                              )
    bot.send_random_word(update=update, context=context)


def translate_learning_words(context: telegram.ext.CallbackContext, learning_words: List[str],
                             from_language=configurations.config.FROM_LANGUAGE,
                             to_language=configurations.config.TO_LANGUAGE) -> List[str]:
    """Translates user entered words."""
    context.user_data['learning_words_translated'] = [translators.google(query_text=learning_words[word],
                                                                         from_language=from_language,
                                                                         to_language=to_language) for word in
                                                      range(len(learning_words))]
    return [word.capitalize() for word in context.user_data['learning_words_translated']]


def words_not_accepted(update: telegram.Update, context: telegram.ext.CallbackContext, cause):
    """Sends 'words not accepted' message."""
    if cause == 'InvalidNumberOfWords':
        update.message.reply_text(
            text='Ой, что-то пошло не так:\n'
                 f'Кол-во твоих слов - {len(context.user_data["learning_words"])}.',
            disable_notification=True
        )
    if cause == 'WordsContainNumbers':
        update.message.reply_text(
            text='Ой, что-то пошло не так:\n'
                 'Видимо, в введённых тобою словах имеются цифры.',
            disable_notification=True
        )
