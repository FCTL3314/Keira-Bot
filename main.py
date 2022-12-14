import time
import logging
import aiogram
import handlers
import utils

from loader import dp
from data.config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from data.config import LOGGING_LEVEL, LOGGING_FILE_NAME, LOGGING_FILE_MODE, LOGGING_FORMAT

logging.basicConfig(level=LOGGING_LEVEL, filename=f"{LOGGING_FILE_NAME}.log", filemode=LOGGING_FILE_MODE,
                    format=LOGGING_FORMAT)

handlers.start_command.register_start_command_handlers(dp=dp)
handlers.set_command.register_set_command_handlers(dp=dp)
handlers.get_learning_words.register_get_learning_words_handlers(dp=dp)
handlers.stop_command.register_stop_command_handler(dp=dp)
handlers.progress_command.register_progress_command_handlers(dp=dp)
handlers.check_translated_word_correctness.register_check_translated_word_correctness_handlers(dp=dp)
handlers.unexpected_messages.register_unexpected_message_handlers(dp=dp)


if __name__ == "__main__":
    while True:
        try:
            aiogram.executor.start_webhook(
                dispatcher=dp,
                webhook_path=WEBHOOK_PATH,
                on_startup=utils.on_startup,
                on_shutdown=utils.on_shutdown,
                skip_updates=True,
                host=WEBAPP_HOST,
                port=WEBAPP_PORT
            )
        except Exception as log_info:
            logging.exception(msg=log_info)
            time.sleep(15)
