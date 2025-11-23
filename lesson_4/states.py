from aiogram.fsm.state import State, StatesGroup


class Survey(StatesGroup):
    name = State()
    language = State()
    experience = State()
