import telegram.ext
import translators
import bot
import configurations.settings

WORDS, GET_WORDS = range(2)


def asks_for_words(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Asks the User to enter a 'NUMBER_OF_WORDS' words. Entry-point of the ConversationHandler."""
    update.message.reply_text(
        text=f'Введите {configurations.settings.NUMBER_OF_WORDS}'
             f' {asks_for_words_spellings()}.\n'  # В зависимости от числа слов меняет написание.
             f'Пример: {create_example_words()}'
    )
    return WORDS


def asks_for_words_spellings():
    """
    Changes the spelling of start_command introduce
    depending on the configurations.settings.NUMBER_OF_WORDS
    """
    if 5 > configurations.settings.NUMBER_OF_WORDS > 1:
        spelling = 'изучаемых иностранных слова'
    elif configurations.settings.NUMBER_OF_WORDS == 1:
        spelling = 'изучаемое иностранное слово'
    else:
        spelling = 'изучаемых иностранных слов'
    return spelling


def create_example_words():
    """
    Creates the number of words equal to configurations.settings.NUMBER_OF_WORDS
    """
    words = ''
    for i in range(configurations.settings.NUMBER_OF_WORDS):
        words += f'Word{i + 1} '
    return words


def get_learning_words(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Gets user-entered learning words and .split() it"""
    context.user_data['learning_words'] = update.message.text.split()  # Разделяет слова и записывает в
    # context.user_data['learning_words']
    if check_number_of_words(context=context):  # Если check_number_of_words - True, то принимает слова, иначе - нет.
        words_accepted(update=update, context=context)
        return GET_WORDS
    else:
        words_not_accepted(update=update, context=context)


def stop_guessing(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Exit point(fallbacks) of the ConversationHandler"""
    update.message.reply_text(text='Поняла, останавливаюсь...\nНапишите /add что бы начать заново.')
    return telegram.ext.ConversationHandler.END


def check_number_of_words(context: telegram.ext.CallbackContext):
    """Returns True if the number of entered words == NUMBER_OF_WORDS, otherwise False."""
    return len(context.user_data['learning_words']) == configurations.settings.NUMBER_OF_WORDS  # Возвращает True
    # если кол-во введенных слов == NUMBER_OF_WORDS, иначе False.


def accepted_words_visual(learning_words: list, learning_words_translated: list) -> str:
    """
    Creates a variable in which it adds the words entered by the user and their translation
    Example: Apple Coffee Milk
    Output: Apple - Яблоко\nCoffee - Кофе\nMilk - Молоко\n (Translation into Russian)
    """
    accepted_words = ''  # Пустая переменная в которую будут добавляться слово и его перевод(Apple - Яблоко\n...)
    for word in range(len(learning_words_translated)):  # Добавляет слова в accepted_words.
        accepted_words += f'{learning_words[word]} - {learning_words_translated[word]}\n'
    return accepted_words


def translate_learnings_words(context: telegram.ext.CallbackContext):
    """Translates learning_words variable"""
    learning_words_translated = []  # Пустой список в который будут добавляться переведённые(learning_words) слова.
    for word in range(len(context.user_data['learning_words'])):  # Добавляет в learning_words_translated
        # переведённые слова.
        learning_words_translated.append(translators.google(
            query_text=context.user_data['learning_words'][word],
            from_language=configurations.settings.FROM_LANGUAGE,
            to_language=configurations.settings.TO_LANGUAGE
        )
        )
    return learning_words_translated


def words_accepted(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Called if the words in the check_number_of_words function are accepted."""
    accepted_words = accepted_words_visual(
        learning_words=context.user_data['learning_words'],
        learning_words_translated=translate_learnings_words(context=context)
    )
    update.message.reply_text(
        text=f'Слова приняты:\n{accepted_words} '
             f'Если хотите остановить напишите /stop.\n'
             f'Далее необходимо вводить перевод слов:'
    )
    bot.get_random_word(update=update, context=context)  # Вызов функции random_word для генерации случайного
    # слова из context.user_data['learning_words']


def words_not_accepted(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Called if the words in the check_number_of_words function are not accepted."""
    update.message.reply_text(
        text='Ой, что-то пошло не так.\n'
             f'Кол-во ваших слов: {len(context.user_data["learning_words"])}.\n'
    )
