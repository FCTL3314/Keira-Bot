import telegram.ext


def create_keyboard_markup(context: telegram.ext.CallbackContext):
    translated_words = context.user_data['learning_words_translated']
    return telegram.ReplyKeyboardMarkup([[translated_words[i]] for i in range(len(translated_words))],
                                        one_time_keyboard=False)
