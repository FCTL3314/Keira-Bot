import telegram.ext
import random
import configurations.settings


def get_random_word(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Generates a random word and send it"""
    context.bot_data['ran_num'] = random.randint(0, (configurations.settings.NUMBER_OF_WORDS - 1))
    update.message.reply_text(
        text=f'{context.user_data["learning_words"][context.bot_data["ran_num"]]}')
