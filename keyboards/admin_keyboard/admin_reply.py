from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = [
    [KeyboardButton(text="🗂 Xizmatlar"), KeyboardButton(text="🔍 Buyurtmalarim")],
    [KeyboardButton(text="💰Hisob toʻldirish"), KeyboardButton(text="👤Mening hisobim")],
    [KeyboardButton(text="👥Referral"), KeyboardButton(text="☎️ Qo'llab-quvvatlash")],
    [KeyboardButton(text="🗄️ Boshqaruv")]
]

admin_menu = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⚙️ Asosiy sozlamalar")],
        [
            KeyboardButton(text="📊 Statistika"),
            KeyboardButton(text="✉️ Xabar yuborish")
        ],
        [
            KeyboardButton(text="🔐 Majbur obuna kanallar")
        ],
        [
            KeyboardButton(text="💳 To'lov tizimlar"),
            KeyboardButton(text="🔑 API")
        ],
        [
            KeyboardButton(text="🧑‍💻 Foydalanuvchini boshqarish")
        ],
        [
            KeyboardButton(text="🛠️ Xizmatlarni tah/qosh"),
            KeyboardButton(text="📈 Buyurtmalar")
        ],
        [KeyboardButton(text="⏪ Orqaga")]
    ],
    resize_keyboard=True
)

boshqaruv = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗄️ Boshqaruv")
        ]
    ],
    resize_keyboard=True)