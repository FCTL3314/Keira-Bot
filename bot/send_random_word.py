import telegram.ext
import random
import configurations


def send_random_word(update: telegram.Update, context: telegram.ext.CallbackContext,
                     number_of_words=configurations.config.NUMBER_OF_WORDS):
    """Generates random word and send it"""
    ran_num = random.randint(0, number_of_words - 1)
    generate_non_previous_number(ran_num=ran_num, update=update, context=context)
    update.message.reply_text(
        text=f'{context.user_data["learning_words"][context.bot_data[f"ran_num: {update.message.from_user.id}"]]}',
        disable_notification=True)


def generate_non_previous_number(ran_num, update: telegram.Update, context: telegram.ext.CallbackContext,
                                 number_of_words=configurations.config.NUMBER_OF_WORDS):
    """Creates a ran_num different from previous_ran_num"""
    try:
        previous_ran_num = context.bot_data[f"ran_num: {update.message.from_user.id}"]
        while ran_num == previous_ran_num:
            ran_num = random.randint(0, number_of_words - 1)
        else:
            context.bot_data[f"ran_num: {update.message.from_user.id}"] = ran_num
    except KeyError:
        context.bot_data[f"ran_num: {update.message.from_user.id}"] = ran_num
