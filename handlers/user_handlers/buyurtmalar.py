from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
# Database funk
from database_funk.users_funk import get_orders_by_user
router = Router()

@router.message(F.text == "🔍 Buyurtmalarim")
async def buyurtmalar(message: Message):
    user_id = message.from_user.id
    orders = await get_orders_by_user(user_id)
    if not orders:
        await message.answer("Sizda hali buyurtma yo'q!")
        return
    for order in orders:
        await message.answer(f"🆔 Buyurtma raqami: {order['order_id']}\n⚡️ Xizmat nomi: {order['xizmat_nomi']}\n🔽 Miqdor: {order['amount']}\n🔗 Link: {order['link']}\n💵 Narxi: {order['narxi']} so'm\n📅 Vaqt: {order['vaqt']}\n🔍 Holati: aniqlanmagan")
    
    