from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
# Keyboards
from keyboards.users_keyboard.users_inline import build_category_keyboard, build_bolim_keyboard, build_xizmat_keyboard, add_order_kb
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
async def select_xizmat(callback: CallbackQuery, state: FSMContext):
    _, category, bolim = callback.data.split(":")
    await state.update_data(bolim=bolim, category=category)
    keyboard = await build_xizmat_keyboard(category, bolim)
    if keyboard:
        await callback.message.edit_text(f"✅O'zingizga kerakli xizmatni tanlang: ({category} → {bolim})", reply_markup=keyboard)
    else:
        await callback.message.edit_text("🚫Xizmatlar mavjud emas!")

    await callback.answer()


# Xizmat haqida ma'lumot

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

@router.callback_query(F.data == "back_xizmatlar")
async def back_to_xizmatlar(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")
    bolim = data.get("bolim")
    keyboard = await build_xizmat_keyboard(category, bolim)
    if keyboard:
        await callback.message.edit_text(f"✅O'zingizga kerakli xizmatni tanlang: ({category} → {bolim})", reply_markup=keyboard)
    else:
        await callback.message.edit_text("🚫Xizmatlar mavjud emas!")

