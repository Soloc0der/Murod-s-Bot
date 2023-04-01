from aiogram.dispatcher.filters.state import State, StatesGroup


class ShopState(StatesGroup):
    category = State()
    product = State()
    amount = State()
    cart = State()