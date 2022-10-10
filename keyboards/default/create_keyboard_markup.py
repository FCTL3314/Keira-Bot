import aiogram


def create_keyboard_markup(text):
    return aiogram.types.reply_keyboard.ReplyKeyboardMarkup([[text[i]] for i in range(len(text))])
