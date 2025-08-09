from aiogram import Router, F
from aiogram.types import Message
# Database funk
from database_funk.users_funk import get_all_user_ids
router = Router()

@router.message(F.text == "📊 Statistika")
async def statistika_handler(message: Message):
    users = await get_all_user_ids()
    count = len(users)
    await message.answer(f"📊 Statistika \n• Obunachilar soni: {count} ta \n• Faol obunachilar: aniqlanmagan \n• Tark etganlar: aniqlanmagan ")