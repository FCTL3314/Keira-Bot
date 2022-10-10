import aiogram
import handlers
import utils

from loader import dp


def main():
    handlers.start_command.register_start_command_handlers(dp=dp)
    handlers.set_command.register_set_command_handlers(dp=dp)
    handlers.get_learning_words.register_get_learning_words_handlers(dp=dp)
    handlers.stop_command.register_stop_command_handler(dp=dp)
    handlers.achievements_command.register_achievements_command_handlers(dp=dp)
    handlers.check_translated_word_correctness.register_check_translated_word_correctness_handlers(dp=dp)
    handlers.unexpected_messages.register_unexpected_message_handlers(dp=dp)

    aiogram.executor.start_polling(dispatcher=dp, on_startup=utils.on_startup(), skip_updates=True)


if __name__ == '__main__':
    main()
