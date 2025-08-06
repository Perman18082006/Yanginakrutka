from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = [
    [KeyboardButton(text="🗂 Xizmatlar"), KeyboardButton(text="🔍 Buyurtmalarim")],
    [KeyboardButton(text="💰Hisob toʻldirish"), KeyboardButton(text="👤Mening hisobim")],
    [KeyboardButton(text="👥Referral"), KeyboardButton(text="☎️ Qo'llab-quvvatlash")],
]

menu = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🚫 Bekor qilish")]], resize_keyboard=True)
