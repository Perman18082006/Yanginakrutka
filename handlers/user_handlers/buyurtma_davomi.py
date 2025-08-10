from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import re

# Database funk
from database_funk.orders_funk import get_service_by_id
from database_funk.order_funk import get_service_limits, add_order
# Keyboards
from keyboards.users_keyboard.users_inline import add_order_kb, order_confirm_kb
# states
from .states import Buyurtma

router = Router()

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

    service_data = await get_service_by_id(service_id)
    if service_data is None:
        await callback.message.edit_text("❌ Xizmat topilmadi!")
        await callback.answer()
        return

    xizmat_nomi = service_data.get("xizmat_nomi", "Noma'lum")
    narx = service_data.get("narxi", "Noma'lum")
    min_value = data.get("min", "Noma'lum")
    max_value = data.get("max", "Noma'lum")

    await callback.message.edit_text(f"""🆔Xizmat raqami: {service_id}
⚡️Xizmat nomi: {xizmat_nomi}
🔽Min: {min_value}
🔼Max: {max_value} 

💵 Narxi: {narx} so'm har 1000 tasi uchun""", reply_markup=await add_order_kb(service_id))
    await callback.answer()



@router.callback_query(F.data.startswith("add_order:"))
async def add_order_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    service_id = int(callback.data.split(":")[1])
    data = await get_service_limits(service_id)
    if data is None:
        await callback.message.edit_text("❌ Bu xizmat API da mavjud emas!")
        await callback.answer()
        return

    await state.update_data(service_id=service_id)
    min = data.get("min", 0)
    max = data.get("max", 0)
    await callback.message.answer(f"✅ Xizmat miqdorini kiriting:\n\n🔽Min: {min}\n🔼Max: {max}")
    await state.set_state(Buyurtma.amount)
    await callback.answer()

@router.message(Buyurtma.amount)
async def process_amount(message: Message, state: FSMContext):
    amount = message.text
    if not amount.isdigit():
        await message.answer("❌ Miqdorni raqamda kiriting!")
        return
    data = await state.get_data()
    service_id = data.get("service_id")
    limits = await get_service_limits(service_id)
    min = limits.get("min", 0)
    max = limits.get("max", 0)
    if int(amount) < min or int(amount) > max:
        await message.answer(f"❌ Miqdor {min} dan {max} gacha bo'lishi kerak!")
        return
    await state.update_data(amount=amount)
    await message.answer("✅ Xizmat linkini kiriting:")
    await state.set_state(Buyurtma.link)


# Linkni tekshirish
def is_valid_link(link: str) -> bool:
    pattern = re.compile(r"^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/[\w\-./?%&=]*)?$")
    return bool(pattern.match(link))

@router.message(Buyurtma.link)
async def process_link(message: Message, state: FSMContext):
    link = message.text
    if not is_valid_link(link):
        await message.answer("❌ Linkni to'g'ri kiriting!")
        return
    await state.update_data(link=link)
    data = await state.get_data()
    service_id = data.get("service_id")
    amount = data.get("amount")
    service_data = await get_service_by_id(service_id)
    xizmat_nomi = service_data.get("xizmat_nomi", "Noma'lum")
    narx = service_data.get("narxi", "Noma'lum")
    await message.answer(f"""✅ Buyurtma tasdiqlash:
🆔Xizmat raqami: {service_id}
⚡️Xizmat nomi: {xizmat_nomi}
🔽Miqdor: {amount}
🔗Link: {link}
💵 Narxi: {narx} so'm har 1000 tasi uchun""", reply_markup=await order_confirm_kb(), disable_web_page_preview=True)
    await state.set_state(Buyurtma.confirm)

@router.callback_query(Buyurtma.confirm, F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    service_id = data.get("service_id")
    amount = data.get("amount")
    link = data.get("link")
    response = await add_order(service_id, link, amount)
    if response.get("order"):
        order_id = response.get("order")
        await callback.message.edit_text(f"✅ Buyurtma qabul qilindi!\n\n🆔 Buyurtma raqami: {order_id}")
    else:
        error_text = response.get("error", "Nomaʼlum xatolik yuz berdi.")
        if error_text == "neworder.error.link_duplicate":
            await callback.message.edit_text("❌ Bu link uchun buyurtma allaqachon yuborilgan. Iltimos, boshqa link kiriting yoki biroz kutib qayta urinib ko‘ring.")
        elif error_text == "not_enough_funds":
            await callback.message.edit_text("❌ API balans yetarli emas")
        else:
            await callback.message.edit_text(f"❌ Xatolik: {error_text}")

    await state.clear()
    await callback.answer()
            
