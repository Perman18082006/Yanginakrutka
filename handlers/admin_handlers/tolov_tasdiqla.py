from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
# Database funk
from database_funk.users_funk import add_balance

router = Router()

@router.callback_query(F.data.startswith("tasdiqla:"))
async def process_tasdiqla(callback: CallbackQuery):
    user_id, amount = callback.data.split(":")[1:]
    await callback.message.delete()
    await callback.message.answer(f"✅ To'lov tasdiqlandi!\n\nTo'lovchi: {user_id}\nTo'lov miqdori: {amount} so'm")
    await callback.message.bot.send_message(user_id, f"✅ Sizning to'lovingiz tasdiqlandi!\n\nTo'lov miqdori: {amount} so'm")
    await add_balance(user_id, amount)
    await callback.answer()


@router.callback_query(F.data.startswith("bekor_qil:"))
async def process_bekor_qil(callback: CallbackQuery):
    user_id = callback.data.split(":")[1]
    await callback.message.answer(f"❌ To'lov bekor qilindi!\n\nTo'lovchi: {user_id}")
    await callback.message.bot.send_message(user_id, "❌ Sizning to'lovingiz bekor qilindi!")
    await callback.answer()
    await callback.message.delete()

