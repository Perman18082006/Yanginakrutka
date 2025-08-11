from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
# Vaqtni olish uchun
from datetime import datetime
from zoneinfo import ZoneInfo
# TEXTLAR
from texts.user_texts import MY_BALANCE
# DATABASE FUNKSIYALAR
from database_funk.users_funk import get_user_data

router = Router()

@router.message(F.text == "👤Mening hisobim")
async def cmd_my_balance(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    # Toshkent vaqti
    vaqt = datetime.now(ZoneInfo("Asia/Tashkent")).strftime("%Y-%m-%d %H:%M:%S")
    try:
        data = await get_user_data(user_id)
        if data is None:
            await message.answer("❌ Foydalanuvchi ma'lumotlari topilmadi!")
            return
        balance = data["balance"]
        referal_count = data["referal_count"]
        order_count = 0  # Bu qismni to'g'irlash kerak
        sarflangan_summa = 0  # Bu qismni to'g'irlash kerak
        await message.answer(MY_BALANCE.format(
            user_id=user_id, balance=balance, order_count=order_count,
            referal_count=referal_count, sarflangan_summa=sarflangan_summa))
    except Exception as e:
        print(f"Xatolik: {e}")
        await message.answer("❌ Xatolik yuz berdi!")