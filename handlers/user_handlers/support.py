from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
# Config
from config import SUPER_ADMIN
# States
from .states import Support

router = Router()

@router.message(F.text == "☎️ Qo'llab-quvvatlash")
async def cmd_support(message: Message, state: FSMContext):
    await message.answer("Murojaat matnini yuboring")
    await state.set_state(Support.message)

@router.message(Support.message)
async def process_support_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_message = message.text
    await message.answer("Murojaatingiz qabul qilindi!")
    await state.clear()
    # Murojaatni adminlarga yuborish
    await message.bot.send_message(SUPER_ADMIN, f"Yangi murojaat:\n\n{user_message}\n\nFoydalanuvchi ID: {user_id}")