import telegram.ext
import translators
import bot
import configurations.settings

from typing import List

GET_ENTERED_WORDS, TRANSLATE_ENTERED_WORDS = range(2)


def asks_for_words(update: telegram.Update, context: telegram.ext.CallbackContext) -> int:
    """Asks the User to enter a words. Entry-point of the ConversationHandler."""
    update.message.reply_text(
        text=f'Введите {configurations.settings.NUMBER_OF_WORDS}'
             f' {create_message_spelling()}.\n'  # В зависимости от числа слов меняет написание.
             f'Пример: {create_enter_words_example()}'
    )
    return GET_ENTERED_WORDS


def create_message_spelling(number_of_words=configurations.settings.NUMBER_OF_WORDS) -> str:
    """Return the string spelling depending on the configurations.settings.NUMBER_OF_WORDS."""
    if 5 > number_of_words > 1:
        spelling = 'изучаемых иностранных слова'
    else:
        spelling = 'изучаемых иностранных слов'
    return spelling


def create_enter_words_example(number_of_words=configurations.settings.NUMBER_OF_WORDS) -> str:
    """Return string with the number of words equal to configurations.settings.NUMBER_OF_WORDS."""
    words = ''
    for i in range(number_of_words):
        words += f'Word{i + 1} '
    return words


def get_learning_words(update: telegram.Update, context: telegram.ext.CallbackContext) -> int:
    """Gets user-entered learning words and .split() it."""
    context.user_data['learning_words'] = update.message.text.split()  # Получает слова, разделяет их и записывает в
    # context.user_data['learning_words']
    if not check_number_of_words(learning_words=context.user_data['learning_words']):
        words_not_accepted(update=update, context=context, cause='Invalid number of words')
    elif not check_for_numbers(learning_words=context.user_data['learning_words']):
        words_not_accepted(update=update, context=context, cause='Words contain numbers')
    else:
        words_accepted(update=update, context=context)
        return TRANSLATE_ENTERED_WORDS


def stop_conversation(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Stops the ConversationHandler."""
    update.message.reply_text(text='Поняла, останавливаюсь...\nНапишите /add что бы начать заново.')
    return telegram.ext.ConversationHandler.END


def check_number_of_words(learning_words: list, number_of_words=configurations.settings.NUMBER_OF_WORDS) -> bool:
    return len(learning_words) == number_of_words  # Возвращает True если кол-во введенных
    # слов == NUMBER_OF_WORDS, иначе False.


def check_for_numbers(learning_words: list) -> bool:
    for symbol in str(learning_words):
        if symbol.isdigit():
            return False
    return True


def accepted_words_visual(learning_words: list, learning_words_translated: list) -> str:
    """
    Creates a variable in which it adds the words entered by the user and their translation.
    :param: learning_words: User entered words.
    :param: learning_words_translated: User entered translated words.
    :return: A string with a words and their translation entered by the user.
    """
    accepted_words = ''  # Пустая переменная в которую будут добавляться слово и его перевод(Apple - Яблоко\n...)
    for word in range(len(learning_words_translated)):  # Добавляет слова в accepted_words.
        accepted_words += f'{learning_words[word]} - {learning_words_translated[word]}\n'
    return accepted_words


def words_accepted(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Sends 'words accepted message'. And generate random word from get_random_word function"""
    update.message.reply_text(text='Обработка...')
    accepted_words = accepted_words_visual(
        learning_words=context.user_data['learning_words'],
        learning_words_translated=translate_learning_words(learning_words=context.user_data['learning_words'],
                                                           context=context)
    )
    update.message.reply_text(
        text=f'Слова приняты:\n{accepted_words} '
             f'Если хотите остановить напишите /stop.\n'
             f'Далее необходимо вводить перевод слов:'
    )
    bot.get_random_word(update=update, context=context)  # Вызов функции random_word для генерации случайного
    # слова из context.user_data['learning_words']


def translate_learning_words(context: telegram.ext.CallbackContext, learning_words: List[str],
                             from_language=configurations.settings.FROM_LANGUAGE,
                             to_language=configurations.settings.TO_LANGUAGE) -> List[str]:
    """
    Translates user entered words.
    :param context:
    :param learning_words: User entered words.
    :param from_language: What language to translate from(default = auto).
    :param to_language: What language to translate(default = ru).
    :return: User entered words(translated into chosen language).
    """
    learning_words_translated = []  # Пустой список в который будут добавляться переведённые(learning_words) слова.
    for word in range(len(learning_words)):  # Добавляет в learning_words_translated переведённые слова.
        learning_words_translated.append(translators.google(
            query_text=learning_words[word],
            from_language=from_language,
            to_language=to_language
        )
        )
    context.user_data['learning_words_translated'] = learning_words_translated
    return context.user_data['learning_words_translated']


def words_not_accepted(update: telegram.Update, context: telegram.ext.CallbackContext, cause):
    """Sends 'words not accepted' message."""
    if cause == 'Invalid number of words':
        update.message.reply_text(
            text='Ой, что-то пошло не так:\n'
                 f'Кол-во ваших слов: {len(context.user_data["learning_words"])}.'
        )
    if cause == 'Words contain numbers':
        update.message.reply_text(
            text='Ой, что-то пошло не так:\n'
                 'В ваших словах содержаться цифры.'
        )
