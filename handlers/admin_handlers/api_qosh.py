from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

# Json funk
from database_funk.json_funk import read_json, update_json, check_api_key
# Keyboard
from keyboards.admin_keyboard.admin_inline import api_tahrirla, api_qosh
# State
from .admin_states import API_qosh
# Config
from config import API_URL
# Filter
from filters import IsAdmin

router = Router()

@router.message(F.text == "🔑 API", IsAdmin())
async def api_qosh_tah(message: Message, state: FSMContext):
  await state.clear()
  data = await read_json()
  if data.get("API_KEY") and data.get("API_URL"):
    await message.answer(f"API URL: {data['API_URL']}\n\nAPI kalit: {data['API_KEY']}", reply_markup=api_tahrirla)
  else:
    await message.answer("API kalit va URL topilmadi. Iltimos, API kalitni va URLni kiriting.", reply_markup=api_qosh)

@router.callback_query(F.data == "api_qoshish")
async def api_qoshish(callback: CallbackQuery, state: FSMContext):
  await callback.message.delete()
  await callback.message.answer("API kalitni kiriting:")
  await state.set_state(API_qosh.api_key)
  await callback.answer()

@router.callback_query(F.data == "api_tahrirlash")
async def api_tahrirlash(callback: CallbackQuery, state: FSMContext):
  await callback.message.delete()
  await callback.message.answer("Yangi API kalitni kiriting:")
  await state.set_state(API_qosh.api_key)
  await callback.answer()


@router.message(API_qosh.api_key)
async def api_key(message: Message, state: FSMContext):
  if await check_api_key(API_URL, message.text):
    await update_json("API_KEY", message.text)
    await message.answer("API kalit muvaffaqiyatli saqlandi")
  else:
    await message.answer("API kalit noto'g'ri. Iltimos, qayta urinib ko'ring.")
    return
  await state.clear()


