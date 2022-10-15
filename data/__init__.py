import data.config

COUNTER_NUMBERS_TO_SEND_PROGRESS = [i for i in range(1, data.config.CORRECT_ANSWERS_TO_LEARN_WORDS) if
                                    i % data.config.PROGRESS_MESSAGE_SENDING_FREQUENCY == 0]
