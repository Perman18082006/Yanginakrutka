from aiogram.fsm.state import State, StatesGroup

class Xizmat_qosh(StatesGroup):
    service_id = State()
    categoria_nomi = State()
    bolim_nomi = State()
    xizmat_nomi = State()
    narxi = State()
    tavsif = State()
    tasdiqlash = State()

class Xizmat_id(StatesGroup):
    xizmat_id = State()

class Xizmat_tahrir(StatesGroup):
    service_id = State()
    kategoriya = State()
    bolim = State()
    xizmat = State()
    narx = State()
    tavsif = State()
    tasdiqlash = State()
    delete = State()

class API_qosh(StatesGroup):
    api_url = State()
    api_key = State()

class Foydalanuvchi_id(StatesGroup):
    user_id = State()
    pul_qoshish = State()