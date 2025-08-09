from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def admin_tasdiqla(user_id, amount):
    return InlineKeyboardMarkup(
        inline_keyboard=[
          [
            InlineKeyboardButton(text="✅Tasdiqlash", callback_data=f"tasdiqla:{user_id}:{amount}"),
            InlineKeyboardButton(text="❌Bekor qilish", callback_data=f"bekor_qil:{user_id}")
          ]
        ])

def javob_yoz(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✏️Javob yozish", callback_data=f"javob_yoz:{user_id}")
            ]
        ]
    )


xizmat_qoshish_tasdiqla = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Tasdiqlash", callback_data="xizmat_qoshish_tasdiqla")
        ]
    ])

xizmat_tah_qosh = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕️ Xizmatlar qo'shish", callback_data="xizmat_qoshish"),
            InlineKeyboardButton(text="✏️ Xizmatlar tahrirlash", callback_data="xizmat_tahrirlash")
        ]
    ])
tahrir_ustun = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 Kategoriya", callback_data="tahrir_kategoriya"),
                InlineKeyboardButton(text="📝 Bo'lim", callback_data="tahrir_bolim")
            ],
            [
                InlineKeyboardButton(text="📝 Xizmat", callback_data="tahrir_xizmat"),
                InlineKeyboardButton(text="📝 Narx", callback_data="tahrir_narx")
            ],
            [
                InlineKeyboardButton(text="📝 Tavsif", callback_data="tahrir_tavsif")
            ]
        ]
)

api_qosh = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕️ API qo'shish", callback_data="api_qoshish")
        ]
    ])

api_tahrirla = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ API tahrirlash", callback_data="api_tahrirlash")
        ]
    ])