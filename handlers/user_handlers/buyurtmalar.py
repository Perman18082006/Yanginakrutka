from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
# Database funk
from database_funk.users_funk import get_orders_by_user
from database_funk.order_funk import get_order_status


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
        status = await get_order_status(order['order_id'])
        if status.get("error"):
            status_text = "❌ Xatolik"
        elif status.get("status") == "Completed":
            status_text = "✅ Bajarildi"
        elif status.get("status") == "In progress":
            status_text = "⏳ Bajarilmoqda"
        elif status.get("status") == "Partial":
            status_text = "⚠️ Qisman bajarildi"
        elif status.get("status") == "Canceled":
            status_text = "❌ Bekor qilindi"
        else:
            status_text = "❓ Aniqlanmagan"
        msg_plus = f"\n🆔 Buyurtma raqami: {order['order_id']}\n⚡️ Xizmat nomi: {order['xizmat_turi']}\n🔽 Miqdor: {order['amount']}\n🔗 Link: {order['link']}\n💵 Narxi: {order['narx']} so'm\n📅 Vaqt: {order['vaqt']}\n🔍 Holati: {status_text}\n━ ━ ━ ━ ━ ━ ━ ━ ━"
        msg += msg_plus
    await message.answer(msg, disable_web_page_preview=True)
    
    
    