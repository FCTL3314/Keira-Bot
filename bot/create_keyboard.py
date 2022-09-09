import telegram.ext


def create_keyboard(context: telegram.ext.CallbackContext):
    translated_words = context.user_data['learning_words_translated']
    reply_keyboard = []
    for i in range(len(translated_words)):
        reply_keyboard += [[]]
        reply_keyboard[i] += [translated_words[i]]
    return telegram.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
