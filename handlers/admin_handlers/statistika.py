from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
# Database funk
from database_funk.users_funk import get_all_user_ids
# Filter
from filters import IsAdmin
router = Router()

@router.message(F.text == "📊 Statistika", IsAdmin())
async def statistika_handler(message: Message, state: FSMContext):
    await state.clear()
    users = await get_all_user_ids()
    count = len(users)
    await message.answer(f"📊 Statistika \n• Obunachilar soni: {count} ta \n• Faol obunachilar: aniqlanmagan \n• Tark etganlar: aniqlanmagan ")