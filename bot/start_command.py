import telegram.ext
import configurations.settings


def start_command(update: telegram.Update, context: telegram.ext.CallbackContext):
    """When executing the command '/start' introduces the user"""
    update.message.reply_text(text=f'Привет! Меня зовут {update.message.bot.first_name}.\n'
                                   f'Сперва, тебе нужно добавить {configurations.settings.NUMBER_OF_WORDS}'
                                   f' {start_command_spellings()}.\n'
                                   f'Пример: {create_example_words()}\n'
                              )


def create_example_words():
    """
    Creates the number of words equal to configurations.settings.NUMBER_OF_WORDS
     for (f'Пример: {create_example_words()}\n') in start_command functions
    """
    words = '/add '
    for i in range(configurations.settings.NUMBER_OF_WORDS):
        words += f'word{i + 1} '
    return words


def start_command_spellings():
    """
    Changes the spelling of start_command introduce
    depending on the configurations.settings.NUMBER_OF_WORDS
    """
    if 5 > configurations.settings.NUMBER_OF_WORDS > 1:
        spelling = 'изучаемых слова'
    elif configurations.settings.NUMBER_OF_WORDS == 1:
        spelling = 'изучаемое слово'
    else:
        spelling = 'изучаемых слов'
    return spelling
