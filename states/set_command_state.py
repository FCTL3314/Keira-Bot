from aiogram.dispatcher.filters.state import StatesGroup, State


class SetCommandStates(StatesGroup):
    get_learning_words = State()
    check_answer_correctness = State()
