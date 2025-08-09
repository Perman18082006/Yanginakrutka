from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
# Vaqtni olish uchun
from datetime import datetime
from zoneinfo import ZoneInfo
# TEXTLAR
from texts.admin_texts import USER_INFO
# DATABASE FUNKSIYALAR
from database_funk.users_funk import get_user_data

# State
from .admin_states import Foydalanuvchi_id
# Keyboard
from keyboards.admin_keyboard.admin_reply import boshqaruv
from keyboards.admin_keyboard.admin_inline import pul_qoshish
# Funk
from database_funk.users_funk import user_exists, add_balance

router = Router()

@router.message(F.text == "🧑‍💻 Foydalanuvchini boshqarish")
async def foydalanuvchi_boshqarish(message: Message, state: FSMContext):
  await state.clear()
  await message.answer("Foydalanuvchini id raqamini kiriting:", reply_markup=boshqaruv)
  await state.set_state(Foydalanuvchi_id.user_id)

@router.message(Foydalanuvchi_id.user_id)
async def foydalanuvchi_id(message: Message, state: FSMContext):
  user_id = message.text
  if not user_id.isdigit():
    await message.answer("Foydalanuvchi id raqami noto'g'ri. Iltimos, qayta urinib ko'ring.")
    return
  if not await user_exists(int(user_id)):
    await message.answer("Foydalanuvchi topilmadi. Iltimos, qayta urinib ko'ring.")
    return
  vaqt = datetime.now(ZoneInfo("Asia/Tashkent")).strftime("%Y-%m-%d %H:%M:%S")
  try:
        data = await get_user_data(user_id)
        balance = data["balance"]
        referal_count = data["referal_count"]
        order_count = 0  # Bu qismni to'g'irlash kerak
        sarflangan_summa = 0  # Bu qismni to'g'irlash kerak
        await message.answer(USER_INFO.format(
            user_id=user_id, balance=balance, order_count=order_count,
            referal_count=referal_count, sarflangan_summa=sarflangan_summa), reply_markup=pul_qoshish)
        await state.update_data(user_id=user_id)
  except Exception as e:
        print(f"Xatolik: {e}")
    
 

@router.callback_query(F.data == "pul_qoshish")
async def pul_qoshish_handler(callback: CallbackQuery, state: FSMContext):
  await callback.message.delete()
  await callback.message.answer("Pul miqdorini kiriting:")
  await state.set_state(Foydalanuvchi_id.pul_qoshish)
  await callback.answer()

@router.message(Foydalanuvchi_id.pul_qoshish)
async def pul_qoshish_money(message: Message, state: FSMContext):
  pul = message.text
  data = await state.get_data()
  user_id = data.get("user_id")
  if not pul.isdigit():
    await message.answer("Pul miqdori noto'g'ri. Iltimos, qayta urinib ko'ring.")
    return
    
  await add_balance(user_id, pul)
  await message.answer("Pul muvaffaqiyatli qo'shildi")
  await message.bot.send_message(user_id, f"Sizning hisobingizga {pul} so'm qo'shildi")
  await state.clear()