from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
# Keyboards
from keyboards.users_keyboard.users_inline import build_category_keyboard, build_bolim_keyboard, build_xizmat_keyboard
# Database funk
from database_funk.orders_funk import get_service_name
from database_funk.order_funk import get_service_limits
router = Router()

# Boshlang‘ich tugma (kategoriya tanlash)
@router.message(F.text == "🗂 Xizmatlar")
async def select_category(message: Message):
    keyboard = await build_category_keyboard()
    if keyboard:
        await message.answer("🖇Quyidagilardan tarmoqlardan birini tanlang:", reply_markup=keyboard)
    else:
        await message.answer("🚫Xizmatlar mavjud emas!")

# Bo‘limlar chiqarish
@router.callback_query(F.data.startswith("cat:"))
async def select_bolim(callback: CallbackQuery):
    category = callback.data.split(":", 1)[1]
    keyboard = await build_bolim_keyboard(category)
    if keyboard:
        await callback.message.edit_text(f"🖇Quyidagi xizmatlardan birini tanlang: ({category})", reply_markup=keyboard)
    else:
        await callback.message.edit_text("🚫Bo‘limlar mavjud emas!")

    await callback.answer()

# Xizmatlar chiqarish
@router.callback_query(F.data.startswith("bolim:"))
async def select_xizmat(callback: CallbackQuery):
    _, category, bolim = callback.data.split(":")
    keyboard = await build_xizmat_keyboard(category, bolim)
    if keyboard:
        await callback.message.edit_text(f"✅O'zingizga kerakli xizmatni tanlang: ({category} → {bolim})", reply_markup=keyboard)
    else:
        await callback.message.edit_text("🚫Xizmatlar mavjud emas!")

    await callback.answer()


# Xizmat tanlandi
@router.callback_query(F.data.startswith("xizmat:"))
async def final_choice(callback: CallbackQuery):
    service_id = int(callback.data.split(":")[1])
    data = await get_service_limits(service_id)

    # Agar data None bo'lsa, xato xabarini ko'rsatish
    if data is None:
        await callback.message.edit_text("❌ Bu xizmat API da mavjud emas!")
        await callback.answer()
        return

    xizmat_nomi = await get_service_name(service_id)
    if xizmat_nomi is None:
        xizmat_nomi = "Noma'lum"

    min_value = data.get("min", "Noma'lum")
    max_value = data.get("max", "Noma'lum")
    narx = await get_service_narxi(service_id)
    if narx is None:
        narx = "Noma'lum"

    await callback.message.edit_text(f"""🆔Xizmat raqami: {service_id}
⚡️Xizmat nomi: {xizmat_nomi}
🔽Min: {min_value}
🔼Max: {max_value} 

💵 Narxi: {narx} so'm har 1000 tasi uchun""")
    await callback.answer()

# Ortga: bolim -> category
@router.callback_query(F.data == "back:category")
async def back_to_category(callback: CallbackQuery):
    keyboard = await build_category_keyboard()
    if keyboard:
        await callback.message.edit_text("🖇Quyidagilardan tarmoqlardan birini tanlang:", reply_markup=keyboard)
    else:
        await callback.message.edit_text("🚫Kategoriyalar mavjud emas!")
    await callback.answer()

# Ortga: xizmat -> bolim
@router.callback_query(F.data.startswith("back:bolim:"))
async def back_to_bolim(callback: CallbackQuery):
    category = callback.data.split(":")[2]
    keyboard = await build_bolim_keyboard(category)
    if keyboard:
        await callback.message.edit_text(f"🖇Quyidagi xizmatlardan birini tanlang: ({category})", reply_markup=keyboard)
    else:
        await callback.message.edit_text("🚫Bo‘limlar mavjud emas!")
    await callback.answer()