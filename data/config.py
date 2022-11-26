import os
import logging


TOKEN = os.getenv('TOKEN')

WEBHOOK_HOST = f'https://'
WEBHOOK_PATH = f'/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 8000))

PG_HOST = os.getenv('PG_HOST')
PG_DBNAME = os.getenv('PG_DBNAME')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT', 5432)

NUMBER_OF_WORDS = 5  # max 6
CORRECT_ANSWERS_TO_LEARN_WORDS = 20
PROGRESS_MESSAGE_SENDING_FREQUENCY = 5  # not more than CORRECT_ANSWERS_TO_LEARN_WORDS
COUNTER_NUMBERS_TO_SEND_PROGRESS = [i for i in range(1, CORRECT_ANSWERS_TO_LEARN_WORDS) if
                                    i % PROGRESS_MESSAGE_SENDING_FREQUENCY == 0]

FROM_LANGUAGE = 'eu'
TO_LANGUAGE = 'ru'

LOGGING_LEVEL = logging.INFO
LOGGING_FILE_NAME = "log"
LOGGING_FILE_MODE = 'w'
LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
