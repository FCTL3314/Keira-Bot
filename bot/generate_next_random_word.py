import telegram.ext
import random
import configurations.config


def generate_random_word(update: telegram.Update, context: telegram.ext.CallbackContext):
    """Generates a random word and send it"""
    context.bot_data[f"ran_num: {update.message.chat_id}"] = random.randint(0, (
            configurations.config.NUMBER_OF_WORDS - 1))
    update.message.reply_text(
        text=f'{context.user_data["learning_words"][context.bot_data[f"ran_num: {update.message.chat_id}"]]}',
        disable_notification=True)
