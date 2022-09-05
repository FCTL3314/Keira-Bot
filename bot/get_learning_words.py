import telegram.ext
import translators
import bot
import configurations.settings


def get_learning_words(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Separates '/add ' from user-entered words and splits into separate words"""
    context.user_data['learning_words'] = update.message.text[4:].split()  # Отделяет /add от
    # context.user_data['learning_words'] и разделяет на отдельные слова с помощью .split()
    learning_words = context.user_data["learning_words"]
    check_number_of_words(
        update=update,
        context=context,
        learning_words=learning_words
    )


def check_number_of_words(update: telegram.Update, context: telegram.ext.CallbackContext, learning_words):
    """Checks the number of words entered by the user"""
    if len(learning_words) == configurations.settings.NUMBER_OF_WORDS:  # Проверяет кол-во введённых слов,
        # из значения переменной NUMBER_OF_WORDS в configurations\settings.py
        accepted_words = accepted_words_visual(
            learning_words=learning_words,
            learning_words_translated=translate_learnings_words(learning_words=learning_words)
        )
        words_accepted(
            update=update,
            context=context,
            accepted_words=accepted_words
        )
    else:
        words_not_accepted(
            update=update,
            learning_words=learning_words
        )


def accepted_words_visual(learning_words, learning_words_translated):
    """
    Creates a variable in which it adds the words entered by the user and their translation
    Example: /add Apple Coffee Milk
    Output: Apple - Яблоко\nCoffee - Кофе\nMilk - Молоко\n (Translation into Russian)
    """
    accepted_words = ''  # Пустая переменная в которую будут добавляться слово и его перевод(Apple - Яблоко)
    for word in range(len(learning_words_translated)):  # Добавляет слова в accepted_words.
        accepted_words += f'{learning_words[word]} - {learning_words_translated[word]}\n'
    return accepted_words


def translate_learnings_words(learning_words):
    """Translates words entered by the user"""
    learning_words_translated = []  # Пустой список в который будут добавляться переведённые(learning_words) слова.
    for word in range(len(learning_words)):  # Добавляет в learning_words_translated переведённые слова.
        learning_words_translated.append(translators.google(
            query_text=learning_words[word],
            from_language=configurations.settings.FROM_LANGUAGE,
            to_language=configurations.settings.TO_LANGUAGE
        )
        )
    return learning_words_translated


def words_accepted(update: telegram.Update, context: telegram.ext.CallbackContext, accepted_words):
    """Called if the words in the check_number_of_words function are accepted."""
    update.message.reply_text(
        text=f'Слова приняты:\n{accepted_words} '
             f'Далее необходимо вводить перевод слов:'
    )
    bot.get_random_word(
        update=update,
        context=context
    )  # Вызов функции random_word
    # для генерации случайного слова из context.user_data['learning_words']


def words_not_accepted(update: telegram.Update, learning_words):
    """Called if the words in the check_number_of_words function are not accepted."""
    update.message.reply_text(text='Ой, что-то пошло не так.\n'
                                   f'Требуемое кол-во слов: {configurations.settings.NUMBER_OF_WORDS}.\n'
                                   f'Кол-во ваших слов: {len(learning_words)}.')
