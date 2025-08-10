from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
# Filter
from filters import IsAdmin
# Keyboard
from keyboards.admin_keyboard.admin_reply import admin_panel

router = Router()

@router.message(F.text == "🗄️ Boshqaruv", IsAdmin())
async def panel_handler(message: Message, state: FSMContext):
  await state.clear()
  await message.answer("Admin paneliga xush kelibsiz", reply_markup=admin_panel)