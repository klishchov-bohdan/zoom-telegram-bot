from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    email = State()
    confirmation_code = State()
