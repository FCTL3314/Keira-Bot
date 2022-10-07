import aiogram
import random
import configurations
import create_bot


def send_random_word(message: aiogram.types.Message, number_of_words=configurations.config.NUMBER_OF_WORDS):
    """Generates random word and send it"""
    ran_num = random.randint(0, number_of_words - 1)
    generate_non_previous_number(ran_num=ran_num, message=message)
    message.answer(
        text=f'{create_bot.user_data["learning_words"][create_bot.bot_data[f"ran_num: {message.from_user.id}"]]}',
        disable_notification=True)


def generate_non_previous_number(ran_num, message: aiogram.types.Message,
                                 number_of_words=configurations.config.NUMBER_OF_WORDS):
    """Creates a ran_num different from previous_ran_num"""
    try:
        previous_ran_num = create_bot.bot_data[f"ran_num: {message.from_user.id}"]
        while ran_num == previous_ran_num:
            ran_num = random.randint(0, number_of_words - 1)
        else:
            create_bot.bot_data[f"ran_num: {message.from_user.id}"] = ran_num
    except KeyError:
        create_bot.bot_data[f"ran_num: {message.from_user.id}"] = ran_num
