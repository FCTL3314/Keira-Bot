import aiogram


def create_keyboard_markup(translated_words):
    return aiogram.types.reply_keyboard.ReplyKeyboardMarkup(
        [[translated_words[i]] for i in range(len(translated_words))])
