from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
# Database funk
from database_funk.users_funk import get_orders_by_user
router = Router()

@router.message(F.text == "🔍 Buyurtmalarim")
async def buyurtmalar(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    orders = await get_orders_by_user(user_id)
    if not orders:
        await message.answer("Sizda hali buyurtma yo'q!")
        return
    msg = "🔍 Buyurtmalarim:\n\n"
    for order in orders:
        msg_plus = f"\n🆔 Buyurtma raqami: {order['order_id']}\n⚡️ Xizmat nomi: {order['xizmat_turi']}\n🔽 Miqdor: {order['amount']}\n🔗 Link: {order['link']}\n💵 Narxi: {order['narx']} so'm\n📅 Vaqt: {order['vaqt']}\n🔍 Holati: aniqlanmagan\n━ ━ ━ ━ ━ ━ ━ ━ ━"
        msg += msg_plus
    await message.answer(msg, disable_web_page_preview=True)
    
    
    