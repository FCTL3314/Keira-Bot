from aiogram.dispatcher.filters.state import StatesGroup, State


class BeginLearnWordsSteps(StatesGroup):
    get_learning_words_state = State()
    check_answer_correctness_state = State()
