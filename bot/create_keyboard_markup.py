import telegram.ext


def create_keyboard_markup(translated_words):
    return telegram.ReplyKeyboardMarkup([[translated_words[i]] for i in range(len(translated_words))])
