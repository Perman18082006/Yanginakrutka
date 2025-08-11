import asyncio
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

    # 1️⃣ Statuslarni parallel olish
    tasks = [get_order_status(int(order['order_id'])) for order in orders]
    statuses = await asyncio.gather(*tasks)

    # 2️⃣ Javobni formatlash
    msg_lines = ["🔍 Buyurtmalarim:"]
    for order, status in zip(orders, statuses):
        if status.get("error"):
            status_text = "❌ Xatolik"
        elif status.get("status") == "Processing":
            status_text = "⏳ Tekshiruvda"
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

        msg_lines.append(
            f"\n🆔 Buyurtma raqami: {order['order_id']}\n"
            f"⚡️ Xizmat nomi: {order['xizmat_turi']}\n"
            f"🔽 Miqdor: {order['amount']}\n"
            f"🔗 Link: {order['link']}\n"
            f"💵 Narxi: {order['narx']} so'm\n"
            f"📅 Vaqt: {order['vaqt']}\n"
            f"🔍 Holati: {status_text}\n━ ━ ━ ━ ━ ━ ━ ━ ━"
        )

    # 3️⃣ Javobni yuborish
    await message.answer("\n".join(msg_lines), disable_web_page_preview=True)
    