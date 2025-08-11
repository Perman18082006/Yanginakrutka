from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
# Database
from database_funk.orders_funk import get_categories, get_bolimlar, get_xizmatlar, get_service_by_id
# Config
from database.payment_methods import payment_methods


def payment_keyboard():
    keyboard = []
    for key, value in payment_methods.items():
        keyboard.append([InlineKeyboardButton(text=value, callback_data=f"pay:{key}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def tolov_qildim():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅️To'lov qildim", callback_data="tolov_qildim")],
        [InlineKeyboardButton(text="🔙Orqaga qaytish", callback_data="cancel")]
    ])


# Kategoriyalar keyboard
async def build_category_keyboard():
    categories = await get_categories()
    if categories:
        builder = InlineKeyboardBuilder()
        for cat in categories:
            builder.button(text=cat, callback_data=f"cat:{cat}")
        builder.button(text="⬅️ Ortga", callback_data="back")
        builder.adjust(2)
        return builder.as_markup()
    else:
        return False

# Bolimlar keyboard
async def build_bolim_keyboard(category):
    bolimlar = await get_bolimlar(category)
    if bolimlar:
        builder = InlineKeyboardBuilder()
        for bolim in bolimlar:
            builder.button(text=bolim, callback_data=f"bolim:{category}:{bolim}")
        builder.button(text="⬅️ Ortga", callback_data="back:category")
        builder.adjust(1)
        return builder.as_markup()
    else:
        return False

# Xizmatlar keyboard
async def build_xizmat_keyboard(category, bolim):
    xizmatlar = await get_xizmatlar(category, bolim)
    if xizmatlar:
        builder = InlineKeyboardBuilder()
        for service_id, name in xizmatlar:
            service_data = await get_service_by_id(service_id)
            narx = service_data["narxi"]
            builder.button(text=f"{name} - {narx}", callback_data=f"xizmat:{service_id}")
        builder.button(text="⬅️ Ortga", callback_data=f"back:bolim:{category}")
        builder.adjust(1)
        return builder.as_markup()
    else:
        return False

async def add_order_kb(service_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅️ Buyurtma berish", callback_data=f"add_order:{service_id}")],
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="back_xizmatlar")]
    ])

async def order_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅️ Tasdiqlash", callback_data="confirm_order")]
    ])