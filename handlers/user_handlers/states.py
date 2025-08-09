from aiogram.fsm.state import State, StatesGroup

class Support(StatesGroup):
    message = State()

class Payment(StatesGroup):
    pay1 = State()
    pay2 = State()
    pay3 = State()

class Buyurtma(StatesGroup):
    amount = State()
    link = State()
    confirm = State()