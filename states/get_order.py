from aiogram.dispatcher.filters.state import State, StatesGroup


class Order_state(StatesGroup):
    full_name = State()
    phone_number = State()
    location = State()
