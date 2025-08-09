from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# Keyboards
from keyboards.users_keyboard.users_reply import cancel
router = Router()

class JavobYoz(StatesGroup):
    javob = State()
  
@router.callback_query(F.data.startswith("javob_yoz:"))
async def process_javob_yoz(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split(":")[1]
    await callback.message.delete()
    await callback.message.answer(f"Foydalanuvchi {user_id} ga javob yozing:", reply_markup=cancel)
    await state.update_data(user_id=user_id)
    await state.set_state(JavobYoz.javob)
    await callback.answer()

@router.message(JavobYoz.javob)
async def process_javob(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    javob = message.text
    await message.bot.send_message(user_id, f"Admindan javob:\n\n{javob}")
    await message.answer("✅ Xabar foydalanuvchiga yuborildi!")
    await state.clear()